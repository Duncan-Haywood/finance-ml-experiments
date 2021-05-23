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
    
    ## todo: into (classes? functions?) and write tests for how they work.
    
    ## init client, build docker image and create ecr repository
    ecr_client = boto3.client('ecr')
    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    docker_client.images.build() ## todo
    epo_response = ecr_client.create_repository(repositoryName=ecr_repository)

    
    ## authentication for docker
    auth_response = ecr_client.get_authorization_token(registryIds=[account_id])
    auth_token = ['authorizationData']['authorizationToken']
    ecr_username, ecr_password = b64decode(auth).split(':')
    docker_client.login(username=ecr_username, password=ecr_password, registry=f'{account_id}.dkr.ecr.{region}.amazonaws.com')

    ## docker tag and push to ecr repo
    docker_client.tag() ## todo
    docker_client.push(processing_repository_uri) ## todo      
    ## todo: implement below in sdk python
    """
    docker build -t {ecr_repository} docker
    aws ecr get-login-password --region {region} | 
    docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com
    aws ecr create-repository --repository-name $ecr_repository
    docker tag {ecr_repository + tag} $processing_repository_uri
    docker push $processing_repository_uri
    """


if __name__ == '__main__':
    main()
