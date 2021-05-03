"""
runs script train_val_test_split on an ec2 instance as a sagemaker processing job
"""
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
import sagemaker
import boto3
## locations and vars
BUCKET = sagemaker.Session().default_bucket()
INPUT_FOLDER = 'stock-data-raw-csv'
OUTPUT_FOLDER = 'DEMO-xgboost-as-a-built-in-algo'
ROLE_ARN = sagemaker.get_execution_role()
## image uri code
ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')
REGION = boto3.Session().region_name
ECR_REPOSITORY = 'sagemaker-processing-container'
TAG = ':latest'
IMAGE_URI = '{}.dkr.ecr.{}.amazonaws.com/{}'.format(ACCOUNT_ID, REGION, ECR_REPOSITORY + TAG)
## call processing job
script_processor = ScriptProcessor(command=['python3'],
                image_uri=IMAGE_URI,
                role=ROLE_ARN,
                instance_count=1,
                instance_type='ml.m5.xlarge')

script_processor.run(code='train_val_test_split.py',
                    inputs=[ProcessingInput(
                        source=f's3://{BUCKET}/{INPUT_FOLDER}/',
                        destination='/opt/ml/processing/input')],
                    outputs=[ProcessingOutput(source='/opt/ml/processing/output/train',
                                              destination=f's3://{BUCKET}/{OUTPUT_FOLDER}/train'),
                        ProcessingOutput(source='/opt/ml/processing/output/validation',
                                         destination=f's3://{BUCKET}/{OUTPUT_FOLDER}/validation'),
                        ProcessingOutput(source='/opt/ml/processing/output/test',
                                         destination=f's3://{BUCKET}/{OUTPUT_FOLDER}/test')])
