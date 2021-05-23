import boto3
import docker
from base64 import b64decode

def main():
    ## constants
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    region = boto3.Session().region_name
    ecr_repository = 'sagemaker-processing-container'
    tag = ':latest'
    processing_repository_uri = '{}.dkr.ecr.{}.amazonaws.com/{}'.format(
        account_id, region, ecr_repository + tag)
    ## ecr
    ecr_client = boto3.client('ecr')
    auth_response = ecr_client.get_authorization_token(registryIds=[account_id])
    auth_token = ['authorizationData']['authorizationToken']
    ecr_username, ecr_password = b64decode(auth).split(':')
    repo_response = ecr_client.create_repository(repositoryName=ecr_repository)
    
    ##docker
    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    docker_client.images.build() ## todo
    docker_client.login(username=ecr_username, password=ecr_password, registry=f'{account_id}.dkr.ecr.{region}.amazonaws.com')
    docker_client.tag()
    docker_client.push(processing_repository_uri)
    # Create ECR repository and push docker image
    # f'docker build -t {ecr_repository} docker'.split()
    """
    aws ecr get-login-password --region {region} | 
    docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com
    aws ecr create-repository --repository-name $ecr_repository
    docker tag {ecr_repository + tag} $processing_repository_uri
    docker push $processing_repository_uri
    """


if __name__ == '__main__':
    main()
