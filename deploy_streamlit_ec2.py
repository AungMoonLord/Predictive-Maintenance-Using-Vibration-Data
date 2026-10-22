"""Deploy the exact Streamlit Dashboard (Frontend + Backend) to AWS EC2."""
import os
import sys
import time
import zipfile
from pathlib import Path
import boto3

REGION = "ap-southeast-1"
BUCKET = "mechagent-data-667815597331-ap-southeast-1"
S3_KEY = "app/mechagent-streamlit-app.zip"
SG_ID = "sg-01a4c5b2aa82e3604"
SUBNET_ID = "subnet-0c28e5aad7f22d137"
AMI_ID = "ami-049bbddb5a446b3f4"  # Amazon Linux 2023 x86_64

def create_app_zip(zip_path="mechagent-streamlit-app.zip"):
    print("Packaging application files for AWS...")
    base = Path(".")
    include_dirs = ["demo", "src", "agent", "artifacts/model", "real_dataset_from_lab/CWRU"]
    include_files = ["requirements.txt"]

    # Also include sample XJTU-SY files
    xjtu_samples = list(Path("real_dataset_from_lab/XJTU-SY").rglob("*.csv"))[:50]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in include_files:
            p = base / f
            if p.exists():
                zf.write(p, p.relative_to(base))
                
        for d in include_dirs:
            dp = base / d
            if dp.exists():
                for root, dirs, files in os.walk(dp):
                    if "__pycache__" in root or ".venv" in root:
                        continue
                    for file in files:
                        fp = Path(root) / file
                        zf.write(fp, fp.relative_to(base))

        for xp in xjtu_samples:
            zf.write(xp, xp.relative_to(base))

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"Created {zip_path} ({size_mb:.2f} MB)")
    return zip_path


def deploy():
    s3 = boto3.client("s3", region_name=REGION)
    ec2 = boto3.client("ec2", region_name=REGION)

    zip_file = create_app_zip()

    # Upload to S3
    print(f"Uploading to s3://{BUCKET}/{S3_KEY}...")
    s3.upload_file(zip_file, BUCKET, S3_KEY)

    # Generate presigned URL valid for 7 days
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": S3_KEY},
        ExpiresIn=604800
    )
    print("Generated presigned S3 URL.")

    # User data script
    user_data = f"""#!/bin/bash
exec > /var/log/user-data.log 2>&1
echo "=== MechAgent Streamlit Cloud Setup ==="
dnf update -y
dnf install -y python3.11 python3.11-pip unzip iptables-services

# Port forwarding 80 -> 8501
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8501
service iptables save || true

mkdir -p /home/ec2-user/mechagent
cd /home/ec2-user/mechagent

echo "Downloading application..."
curl -s -L -o app.zip "{presigned_url}"
unzip -q -o app.zip

echo "Setting up Python virtualenv..."
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install streamlit plotly requests pandas reportlab markdown scipy boto3
pip install transformers torch --extra-index-url https://download.pytorch.org/whl/cpu

cat << 'EOF' > /etc/systemd/system/streamlit.service
[Unit]
Description=MechAgent Streamlit Dashboard
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/mechagent
Environment="PATH=/home/ec2-user/mechagent/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="MECHAGENT_API=https://jynfhl5nc9.execute-api.ap-southeast-1.amazonaws.com"
ExecStart=/home/ec2-user/mechagent/.venv/bin/streamlit run demo/dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

chown -R ec2-user:ec2-user /home/ec2-user/mechagent
systemctl daemon-reload
systemctl enable streamlit
systemctl start streamlit
echo "=== Setup Complete! Streamlit Service Active ==="
"""

    # Terminate any existing instance to ensure fresh clean deploy
    instances = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Name", "Values": ["MechAgent-Streamlit-Dashboard"]},
            {"Name": "instance-state-name", "Values": ["running", "pending"]}
        ]
    )["Reservations"]

    if instances and instances[0]["Instances"]:
        for inst in instances[0]["Instances"]:
            old_id = inst["InstanceId"]
            print(f"Terminating previous instance: {old_id}...")
            ec2.terminate_instances(InstanceIds=[old_id])
        print("Waiting for instance to terminate...")
        time.sleep(10)

    print("Launching fresh EC2 instance (t3.small) in ap-southeast-1...")
    run_res = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType="t3.small",
        MinCount=1,
        MaxCount=1,
        SubnetId=SUBNET_ID,
        SecurityGroupIds=[SG_ID],
        UserData=user_data,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "MechAgent-Streamlit-Dashboard"},
                    {"Key": "Project", "Value": "MechAgent"}
                ]
            }
        ]
    )
    inst_id = run_res["Instances"][0]["InstanceId"]
    print(f"Instance launched: {inst_id}. Waiting for running state...")
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[inst_id])

    # Associate Static Elastic IP for permanent global access
    eip_alloc = "eipalloc-0523aa5bb9d5f1129"
    try:
        ec2.associate_address(InstanceId=inst_id, AllocationId=eip_alloc)
        pub_ip = "47.128.181.97"
        print(f"Associated Static Elastic IP: {pub_ip}")
    except Exception as e:
        print(f"Could not associate Elastic IP ({e}), querying dynamic IP...")
        desc = ec2.describe_instances(InstanceIds=[inst_id])
        pub_ip = desc["Reservations"][0]["Instances"][0].get("PublicIpAddress", "")

    print("\n==========================================")
    print(f"Streamlit Dashboard EC2 Instance Running!")
    print(f"Public IP: {pub_ip}")
    print(f"Streamlit Direct URL: http://{pub_ip}:8501")
    print(f"HTTP Standard URL:   http://{pub_ip}")
    print("Waiting for Streamlit service to finish setup (~90s)...")
    
    import requests
    start_wait = time.time()
    ready = False
    while time.time() - start_wait < 300:
        try:
            r = requests.get(f"http://{pub_ip}:8501/_stcore/health", timeout=3)
            if r.status_code == 200:
                ready = True
                print("Streamlit service is HEALTHY and READY!")
                break
        except Exception:
            pass
        try:
            r = requests.get(f"http://{pub_ip}:8501", timeout=3)
            if r.status_code == 200:
                ready = True
                print("Streamlit HTTP 200 OK received!")
                break
        except Exception:
            pass
        time.sleep(10)
        print(f"Waiting for Streamlit startup... ({int(time.time() - start_wait)}s elapsed)")
    
    if ready:
        print("\n==========================================")
        print("DEPLOYMENT VERIFIED SUCCESSFUL!")
        print(f"Access the exact dashboard at: http://{pub_ip}:8501")
        print("==========================================\n")
    else:
        print("\nNote: Service initialization is still in progress; check http://" + pub_ip + ":8501 in a minute.\n")
    return pub_ip

if __name__ == "__main__":
    deploy()
