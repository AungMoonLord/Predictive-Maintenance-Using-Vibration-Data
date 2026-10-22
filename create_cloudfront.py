import time
import boto3

def create_cf():
    cf = boto3.client("cloudfront")
    origin_domain = "ec2-47-128-181-97.ap-southeast-1.compute.amazonaws.com"
    origin_id = "MechAgent-Streamlit-EC2"

    distribution_config = {
        "CallerReference": f"mechagent-cf-{int(time.time())}",
        "Comment": "MechAgent AI Dashboard CloudFront Distribution",
        "Enabled": True,
        "Origins": {
            "Quantity": 1,
            "Items": [
                {
                    "Id": origin_id,
                    "DomainName": origin_domain,
                    "CustomOriginConfig": {
                        "HTTPPort": 80,
                        "HTTPSPort": 443,
                        "OriginProtocolPolicy": "http-only",
                        "OriginSslProtocols": {
                            "Quantity": 1,
                            "Items": ["TLSv1.2"],
                        },
                        "OriginReadTimeout": 60,
                        "OriginKeepaliveTimeout": 5,
                    },
                }
            ],
        },
        "DefaultCacheBehavior": {
            "TargetOriginId": origin_id,
            "ViewerProtocolPolicy": "redirect-to-https",
            "AllowedMethods": {
                "Quantity": 7,
                "Items": ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"],
                "CachedMethods": {
                    "Quantity": 2,
                    "Items": ["GET", "HEAD"],
                },
            },
            "CachePolicyId": "4135ea2d-6df8-44a3-9df3-4b5a84be39ad",  # Managed-CachingDisabled
            "OriginRequestPolicyId": "216adef6-5c7f-47e4-b989-5492eafa07d3",  # Managed-AllViewer
            "Compress": True,
        },
        "PriceClass": "PriceClass_All",
    }

    print("Creating CloudFront Distribution...")
    res = cf.create_distribution(DistributionConfig=distribution_config)
    dist_id = res["Distribution"]["Id"]
    domain_name = res["Distribution"]["DomainName"]
    status = res["Distribution"]["Status"]
    print(f"Created Distribution successfully!")
    print(f"Distribution ID: {dist_id}")
    print(f"Domain Name: https://{domain_name}")
    print(f"Status: {status}")
    return dist_id, domain_name

if __name__ == "__main__":
    create_cf()
