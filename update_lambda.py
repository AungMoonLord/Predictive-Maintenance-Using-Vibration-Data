import io
import zipfile
from pathlib import Path
import boto3

def update():
    agent_dir = Path("agent")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in agent_dir.rglob("*"):
            if "__pycache__" not in f.parts and f.is_file():
                arcname = f.relative_to(agent_dir)
                zf.write(f, arcname)
                
    zip_bytes = buf.getvalue()
    print(f"Created Lambda zip: {len(zip_bytes)} bytes ({len(zip_bytes)/(1024):.1f} KB)")
    
    lam = boto3.client("lambda", region_name="ap-southeast-1")
    res = lam.update_function_code(
        FunctionName="mechagent-stack-agent",
        ZipFile=zip_bytes
    )
    print("Lambda update submitted. Status:", res.get("LastUpdateStatus", "InProgress"))
    print("Function ARN:", res["FunctionArn"])

if __name__ == "__main__":
    update()
