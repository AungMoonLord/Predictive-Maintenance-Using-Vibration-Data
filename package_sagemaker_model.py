import tarfile
import os
from pathlib import Path
import boto3

model_dir = Path("artifacts/model")
tar_path = Path("model.tar.gz")

print("Packaging artifacts/model into model.tar.gz...")
with tarfile.open(tar_path, "w:gz") as tar:
    for item in model_dir.iterdir():
        tar.add(item, arcname=item.name)

size_mb = tar_path.stat().st_size / (1024 * 1024)
print(f"Created model.tar.gz ({size_mb:.2f} MB)")

s3 = boto3.client("s3", region_name="ap-southeast-1")
bucket = "mechagent-data-667815597331-ap-southeast-1"
key = "mechagent/model.tar.gz"

print(f"Uploading to s3://{bucket}/{key}...")
s3.upload_file(str(tar_path), bucket, key)
print("Uploaded model.tar.gz to S3 successfully!")
