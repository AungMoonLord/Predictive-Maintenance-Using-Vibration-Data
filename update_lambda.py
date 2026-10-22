import io
import zipfile
from pathlib import Path
import boto3

def update():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. agent/ files at root of zip
        agent_dir = Path("agent")
        for f in agent_dir.rglob("*"):
            if "__pycache__" not in f.parts and f.is_file():
                zf.write(f, f.relative_to(agent_dir))
                
        # 2. src/ folder
        for f in Path("src").rglob("*"):
            if "__pycache__" not in f.parts and f.is_file():
                zf.write(f, f)
                
        # 3. mcp_servers/ folder
        for f in Path("mcp_servers").rglob("*"):
            if "__pycache__" not in f.parts and f.is_file():
                zf.write(f, f)
                
        # 4. data/ database
        db_file = Path("data/mechagent.db")
        if db_file.exists():
            zf.write(db_file, "data/mechagent.db")
                
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
