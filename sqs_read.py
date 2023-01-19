import json
from user_logins_data import UserLoginsData
from helper import docker_exec_with_retry, apply_mask

sqs_container_name = 'localstack_SQS'
sqs_docker_image = "fetchdocker/data-takehome-localstack:latest"
sqs_command = "awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue"
sqs_docker_ports = {'4566/tcp': ('127.0.0.1', 4566)}
sqs_command_tag = "SQS READ"


# creates data object from SQS response
def create_data_object(sqs_response):
    sqs_output = sqs_response._asdict()['output']
    response_body = json.loads(json.loads(sqs_output)['Messages'][0]['Body'])
    user_id = response_body['user_id']
    app_version = response_body['app_version']
    device_type = response_body['device_type']
    ip = response_body['ip']
    locale = response_body['locale']
    device_id = response_body['device_id']
    masked_ip = apply_mask(ip)
    masked_device_id = apply_mask(device_id)
    print("Creating UserLoginData object")
    user_login_data = UserLoginsData(user_id, device_type, masked_ip, masked_device_id, locale,
                                     int(app_version.split('.')[0]))
    print("User login object created successfully")
    return user_login_data


# spin up SQS container
def get_sqs_data(sqs_container):
    sqs_response = docker_exec_with_retry(sqs_container, sqs_command, sqs_command_tag)
    user_login_data = create_data_object(sqs_response)
    return user_login_data
