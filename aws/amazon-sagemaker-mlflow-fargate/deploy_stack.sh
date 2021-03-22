#!/usr/bin/env bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
npm install -g aws-cdk@1.65.0
aws configure
## needs to run aws configure and set up IAM user with several access policies before the following will work; needs docker as well and potentially needs to be outside sagemaker studio
ACCOUNT_ID=$(aws sts get-caller-identity --query Account | tr -d '"')
AWS_REGION=$(aws configure get region)

cdk bootstrap aws://${ACCOUNT_ID}/${AWS_REGION}
cdk deploy --parameters ProjectName=mlflow --require-approval never