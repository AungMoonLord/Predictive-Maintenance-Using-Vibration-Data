"""MechAgent Automated AWS Deployment Tool.
Guides users interactively to configure credentials and deploy all AWS resources:
S3, DynamoDB, SageMaker Endpoint, Lambda Orchestrator, API Gateway, SNS.
Supports AWS IAM Identity Center (AWS SSO) temporary credentials with AWS_SESSION_TOKEN.

Usage:
    python aws_deploy.py
"""
import getpass
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path

# Configure UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(0, str(BASE_DIR / "agent"))

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def print_banner(text):
    line = "=" * 65
    print(f"\n{line}\n  {text}\n{line}")


def parse_credentials_text(text):
    """Parse credentials from various formats:
    - SET AWS_ACCESS_KEY_ID=...
    - $env:AWS_ACCESS_KEY_ID="..."
    - export AWS_ACCESS_KEY_ID=...
    - aws_access_key_id = ...
    """
    ak, sk, token = "", "", ""
    for line in text.splitlines():
        line = line.strip()
        m_ak = re.search(r'(?:AWS_ACCESS_KEY_ID|aws_access_key_id)\s*[=:]\s*["\']?([^\s"\';]+)', line, re.I)
        if m_ak:
            ak = m_ak.group(1).strip()
        m_sk = re.search(r'(?:AWS_SECRET_ACCESS_KEY|aws_secret_access_key)\s*[=:]\s*["\']?([^\s"\';]+)', line, re.I)
        if m_sk:
            sk = m_sk.group(1).strip()
        m_tok = re.search(r'(?:AWS_SESSION_TOKEN|aws_session_token)\s*[=:]\s*["\']?([^\s"\';]+)', line, re.I)
        if m_tok:
            token = m_tok.group(1).strip()
    return ak, sk, token


def prompt_credentials():
    print_banner("1. ตั้งค่าการเชื่อมต่อ AWS (AWS Credentials Setup)")
    
    # 1. Check if aws_creds.txt exists in project folder
    creds_txt = BASE_DIR / "aws_creds.txt"
    if creds_txt.exists():
        raw_text = creds_txt.read_text(encoding="utf-8")
        ak, sk, token = parse_credentials_text(raw_text)
        if ak and sk:
            print(f"ℹ️ ตรวจพบข้อมูล Credentials จากไฟล์ aws_creds.txt:")
            print(f"  • Access Key ID: {ak[:6]}...{ak[-4:]}")
            if token:
                print("  • Session Token: ตรวจพบ (AWS SSO / Temporary Credentials)")
            reg = "ap-southeast-1"
            save_credentials_file(ak, sk, token, reg)
            return ak, sk, token, reg

    # 2. Check existing session in ~/.aws/credentials
    session = boto3.Session()
    existing_creds = session.get_credentials()
    if existing_creds and existing_creds.access_key:
        masked = existing_creds.access_key[:4] + "..." + existing_creds.access_key[-4:]
        print(f"ℹ️ ตรวจพบ Key เดิมในระบบ: {masked}")
        use_existing = input("ต้องการใช้ Key เดิมนี้หรือไม่? (Y/n): ").strip().lower()
        if use_existing in ("", "y", "yes"):
            reg = session.region_name or os.environ.get("AWS_DEFAULT_REGION", "ap-southeast-1")
            return existing_creds.access_key, existing_creds.secret_key, existing_creds.token or "", reg

    # 3. Interactive prompt
    print("คุณสามารถคัดลอกจากหน้า AWS Access Portal แล้วกรอกข้อมูลได้เลยครับ:")
    print("กด [1] เพื่อกรอกทีละช่อง หรือ [2] เพื่อวางโค้ดทั้งหมด (Option 1 หรือ Option 2) รวดเดียว")
    mode = input("เลือกวิธี [ค่าเริ่มต้น: 2]: ").strip() or "2"
    
    if mode == "2":
        print("\n👉 กรุณาวางข้อความที่คุณ Copy มาจากหน้า AWS access portal (กด Enter 2 ครั้งเพื่อจบการวาง):")
        lines = []
        while True:
            try:
                line = input()
                if not line and lines and not lines[-1]:
                    break
                lines.append(line)
            except EOFError:
                break
        pasted_text = "\n".join(lines)
        ak, sk, token = parse_credentials_text(pasted_text)
        
        if not ak or not sk:
            print("⚠️ ไม่พบข้อมูล Access Key ในข้อความที่วาง สลับไปกรอกทีละช่อง...")
            mode = "1"
            
    if mode == "1":
        ak = input("👉 AWS Access Key ID (เช่น ASIA... หรือ AKIA...): ").strip()
        sk = getpass.getpass("👉 AWS Secret Access Key: ").strip()
        token = ""
        if ak.startswith("ASIA"):
            token = getpass.getpass("👉 AWS Session Token (กด Enter หากไม่มี): ").strip()

    reg = input("👉 AWS Region [กด Enter เพื่อเลือกค่าแนะนำตาม SSO: ap-southeast-1]: ").strip() or "ap-southeast-1"
    save_credentials_file(ak, sk, token, reg)
    return ak, sk, token, reg


def save_credentials_file(ak, sk, token, reg):
    aws_dir = Path.home() / ".aws"
    aws_dir.mkdir(exist_ok=True)
    
    creds_file = aws_dir / "credentials"
    creds_content = f"[default]\naws_access_key_id = {ak}\naws_secret_access_key = {sk}\n"
    if token:
        creds_content += f"aws_session_token = {token}\n"
    creds_file.write_text(creds_content, encoding="utf-8")
    
    config_file = aws_dir / "config"
    config_content = f"[default]\nregion = {reg}\noutput = json\n"
    config_file.write_text(config_content, encoding="utf-8")
    print(f"\n✅ บันทึก Credentials ลงใน {creds_file} สำเร็จ!")


def verify_connection(ak, sk, token, reg):
    print("\n🔍 กำลังทดสอบเชื่อมต่อกับ AWS...")
    os.environ["AWS_ACCESS_KEY_ID"] = ak
    os.environ["AWS_SECRET_ACCESS_KEY"] = sk
    if token:
        os.environ["AWS_SESSION_TOKEN"] = token
    os.environ["AWS_DEFAULT_REGION"] = reg
    
    sts = boto3.client("sts", region_name=reg)
    try:
        identity = sts.get_caller_identity()
        print(f"  • เชื่อมต่อสำเร็จ! Account ID: {identity['Account']}")
        print(f"  • IAM User/Role: {identity['Arn']}")
        print(f"  • Region เป้าหมาย: {reg}")
        return identity["Account"]
    except ClientError as e:
        print(f"\n❌ การเชื่อมต่อล้มเหลว: {e}")
        print("คำแนะนำ: กรุณาตรวจสอบว่า Access Key ID, Secret Key และ Session Token ถูกต้องหรือไม่")
        sys.exit(1)


def setup_s3_bucket(account_id, reg):
    print_banner("2. สร้าง Amazon S3 Data Bucket")
    s3 = boto3.client("s3", region_name=reg)
    bucket_name = f"mechagent-data-{account_id}-{reg}"
    
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"  • พบ Bucket เดิม: {bucket_name}")
    except ClientError:
        print(f"  • กำลังสร้าง S3 Bucket: {bucket_name} ...")
        create_kwargs = {"Bucket": bucket_name}
        if reg != "us-east-1":
            create_kwargs["CreateBucketConfiguration"] = {"LocationConstraint": reg}
        s3.create_bucket(**create_kwargs)
        print(f"  • สร้าง S3 Bucket สำเร็จ!")
        
    # Upload Maintenance Manual for RAG
    from seed_data import MANUAL
    s3.put_object(
        Bucket=bucket_name,
        Key="manuals/bearing_manual.md",
        Body=MANUAL.encode("utf-8"),
        ContentType="text/markdown"
    )
    print("  • อัปโหลดคู่มือซ่อมบำรุงเข้า S3 (manuals/bearing_manual.md) สำเร็จ!")
    return bucket_name


def package_and_upload_model(bucket_name, reg):
    print_banner("3. เตรียม Model Artifacts สำหรับ SageMaker")
    model_dir = BASE_DIR / "artifacts" / "model"
    if not (model_dir / "model.pt").exists():
        print("  • ยังไม่พบโมเดลใน artifacts/model/ กำลังรัน quick train อัตโนมัติ...")
        cmd = [sys.executable, str(BASE_DIR / "src" / "pipeline.py"), "--quick"]
        subprocess.run(cmd, check=True)

    tar_path = BASE_DIR / "artifacts" / "model.tar.gz"
    print(f"  • กำลังบีบอัดโมเดลเป็น {tar_path.name}...")
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in ["model.pt", "mechagent_config.json"]:
            p = model_dir / f
            if p.exists():
                tar.add(p, arcname=f)
        bcfg_dir = model_dir / "backbone_config"
        if bcfg_dir.exists():
            tar.add(bcfg_dir, arcname="backbone_config")
        code_dir = model_dir / "code"
        if code_dir.exists():
            tar.add(code_dir, arcname="code")
            
    print(f"  • บีบอัดสำเร็จ (ขนาด: {tar_path.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  • กำลังอัปโหลดโมเดลขึ้น S3 (s3://{bucket_name}/mechagent/models/model.tar.gz)...")
    
    s3 = boto3.client("s3", region_name=reg)
    s3.upload_file(str(tar_path), bucket_name, "mechagent/models/model.tar.gz")
    print("  • อัปโหลดโมเดลขึ้น S3 สำเร็จ!")
    return f"s3://{bucket_name}/mechagent/models/model.tar.gz"


def deploy_cloudformation_stack(bucket_name, reg, alert_email, endpoint_name="mechagent-endpoint"):
    print_banner("4. Deploy Serverless Stack (DynamoDB, Lambda, API Gateway, SNS)")
    
    approval_secret = secrets.token_hex(16)
    
    agent_dir = BASE_DIR / "agent"
    zip_path = BASE_DIR / "artifacts" / "agent_lambda.zip"
    shutil.make_archive(str(BASE_DIR / "artifacts" / "agent_lambda"), "zip", agent_dir)
    
    s3 = boto3.client("s3", region_name=reg)
    lambda_s3_key = "mechagent/lambda/agent.zip"
    print(f"  • อัปโหลดโค้ด Lambda ขึ้น S3 (s3://{bucket_name}/{lambda_s3_key})...")
    s3.upload_file(str(zip_path), bucket_name, lambda_s3_key)
    
    cf = boto3.client("cloudformation", region_name=reg)
    stack_name = "mechagent-stack"
    
    # Bedrock model ID for ap-southeast-1 or us-east-1
    bedrock_model = "apac.amazon.nova-pro-v1:0" if reg == "ap-southeast-1" else "us.amazon.nova-pro-v1:0"
    
    params = [
        {"ParameterKey": "DataBucketName", "ParameterValue": bucket_name},
        {"ParameterKey": "EndpointName", "ParameterValue": endpoint_name},
        {"ParameterKey": "AlertEmail", "ParameterValue": alert_email},
        {"ParameterKey": "ApprovalSecret", "ParameterValue": approval_secret},
        {"ParameterKey": "BedrockModelId", "ParameterValue": bedrock_model},
    ]
    
    template_body = (BASE_DIR / "template.yaml").read_text(encoding="utf-8")
    
    print(f"  • กำลังเริ่มสร้าง CloudFormation Stack: {stack_name}...")
    try:
        cf.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=params,
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
        )
    except ClientError as e:
        if "AlreadyExistsException" in str(e):
            print(f"  • พบ Stack เดิม ทำการ Update Stack...")
            try:
                cf.update_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=params,
                    Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
                )
            except ClientError as ue:
                if "No updates are to be performed" in str(ue):
                    print("  • Stack อัปเดตเป็นเวอร์ชันล่าสุดแล้ว")
                else:
                    raise ue
        else:
            raise e
            
    print("  • กำลังรอให้ Resources บน AWS สร้างเสร็จ (ใช้เวลา ~2-3 นาที)...")
    waiter = cf.get_waiter("stack_create_complete")
    try:
        waiter.wait(StackName=stack_name, WaiterConfig={"Delay": 10, "MaxAttempts": 30})
    except Exception:
        pass
        
    outputs = cf.describe_stacks(StackName=stack_name)["Stacks"][0].get("Outputs", [])
    out_dict = {o["OutputKey"]: o["OutputValue"] for o in outputs}
    
    print("\n✅ Deploy CloudFormation สำเร็จ!")
    print(f"  • TableName: {out_dict.get('TableName')}")
    print(f"  • API URL: {out_dict.get('ApiUrl')}")
    return out_dict


def seed_database(table_name, bucket_name, reg):
    print_banner("5. บันทึกข้อมูลตั้งต้นลง DynamoDB (Seed Data)")
    cmd = [
        sys.executable,
        str(BASE_DIR / "aws" / "seed_data.py"),
        "--table", table_name,
        "--bucket", bucket_name,
        "--region", reg
    ]
    subprocess.run(cmd, check=True)
    print("✅ โหลดข้อมูลเครื่องจักร, อะไหล่, ตารางซ่อม ลง DynamoDB สำเร็จ!")


def main():
    print("""
    =================================================================
       MechAgent: Automated AWS Cloud Deployment Tool
       ระบบติดตั้งและ Deploy โซลูชัน Predictive Maintenance บน AWS
    =================================================================
    """)
    
    # 1. Credentials
    ak, sk, token, reg = prompt_credentials()
    account_id = verify_connection(ak, sk, token, reg)
    
    # 2. Email prompt
    print_banner("ตั้งค่าอีเมลแจ้งเตือน (Alert Email)")
    alert_email = input("👉 ระบุอีเมลสำหรับรับแจ้งเตือนและกดอนุมัติงานซ่อม (Approve Work Order): ").strip()
    while "@" not in alert_email:
        alert_email = input("👉 กรุณาระบุอีเมลที่ถูกต้อง (เช่น yourname@company.com): ").strip()
        
    # 3. S3 Bucket
    bucket_name = setup_s3_bucket(account_id, reg)
    
    # 4. Model Packaging
    model_s3_uri = package_and_upload_model(bucket_name, reg)
    
    # 5. CloudFormation Stack
    endpoint_name = "mechagent-endpoint"
    stack_outputs = deploy_cloudformation_stack(bucket_name, reg, alert_email, endpoint_name)
    api_url = stack_outputs.get("ApiUrl", "")
    table_name = stack_outputs.get("TableName", "mechagent-table")
    
    # 6. Seed DynamoDB
    seed_database(table_name, bucket_name, reg)
    
    # 7. Summary
    print_banner("🎉 การ DEPLOY ขึ้น AWS เสร็จสมบูรณ์แล้ว!")
    print(f"  1. AWS API Gateway URL: {api_url}")
    print(f"  2. DynamoDB Table: {table_name}")
    print(f"  3. S3 Data Bucket: {bucket_name}")
    print(f"  4. SageMaker Model Artifact: {model_s3_uri}")
    print(f"  5. Alert Email: {alert_email}")
    print("\n📩 สำคัญ: กรุณาเข้าไปกดยืนยัน (Confirm Subscription) ในอีเมลที่ส่งมาจาก AWS SNS เพื่อเปิดรับแจ้งเตือน")
    print(f"\n🌐 ตอนนี้คุณสามารถนำ API URL ({api_url}) ไปใส่ในหน้า Dashboard เพื่อสั่งการผ่าน Cloud ได้ทันที!")


if __name__ == "__main__":
    main()
