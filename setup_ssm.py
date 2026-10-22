import boto3
import json

iam = boto3.client('iam')
role_name = 'EC2-SSM-Streamlit-Role'

assume_role_doc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    role = iam.get_role(RoleName=role_name)
    print("Role exists:", role['Role']['Arn'])
except Exception:
    role = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_doc)
    )
    print("Created role:", role['Role']['Arn'])
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
    )
    print("Attached AmazonSSMManagedInstanceCore")

try:
    prof = iam.get_instance_profile(InstanceProfileName=role_name)
    print("Profile exists")
except Exception:
    iam.create_instance_profile(InstanceProfileName=role_name)
    iam.add_role_to_instance_profile(InstanceProfileName=role_name, RoleName=role_name)
    print("Created instance profile and added role")

# Now associate with instance i-0c416aadbbcc3cce7
ec2 = boto3.client('ec2', region_name='ap-southeast-1')
try:
    assoc = ec2.associate_iam_instance_profile(
        IamInstanceProfile={'Name': role_name},
        InstanceId='i-0c416aadbbcc3cce7'
    )
    print("Associated instance profile with i-0c416aadbbcc3cce7:", assoc['IamInstanceProfileAssociation']['AssociationId'])
except Exception as e:
    print("Association status/error:", e)
