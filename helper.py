import docker
import time
import hashlib
from docker.errors import NotFound, ContainerError, ImageNotFound, APIError


# Delete a docker container in case it's running
def delete_container(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
        print(f"Container {container_name} deleted.")
    except NotFound as e:
        print(f"Container {container_name} does not exist. {e}")


def run_detached_container(docker_image, container_name, ports):
    client = docker.from_env()
    container = None
    try:
        container = client.containers.run(
            docker_image,
            detach=True,
            name=container_name,
            ports=ports)
    except (ContainerError, ImageNotFound, APIError) as e:
        print(f"Error while running {container_name} docker container. {e}")
    return container


def docker_exec_with_retry(docker_container, docker_command, command_tag):
    max_attempts = 10
    attempt = 0
    response = None
    while True:
        try:
            attempt += 1
            response = docker_container.exec_run(docker_command)
            if response.exit_code == 0:
                print(f"{command_tag} command succeeded.")
                break
            else:
                print(f"{command_tag} command failed.")
                raise Exception(f"{command_tag} command failed.")
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt >= max_attempts:
                print("Maximum number of attempts reached.")
                break
            else:
                print("Waiting for 5 seconds before retrying.")
                time.sleep(5)
    return response


def apply_mask(string_id):
    return hashlib.sha256(string_id.encode()).hexdigest()
