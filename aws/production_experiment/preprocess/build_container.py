import boto3
import docker

def main():
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    region = boto3.Session().region_name
    ecr_repository = 'sagemaker-processing-container'
    tag = ':latest'
    processing_repository_uri = '{}.dkr.ecr.{}.amazonaws.com/{}'.format(
        account_id, region, ecr_repository + tag)
    ecr_client = boto3.client('ecr')
    # Create ECR repository and push docker image
    # f'docker build -t {ecr_repository} docker'.split()
    """
    aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com
    aws ecr create-repository --repository-name $ecr_repository
    docker tag {ecr_repository + tag} $processing_repository_uri
    docker push $processing_repository_uri
    """


if __name__ == '__main__':
    main()
