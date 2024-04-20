import docker
import os
import sys

if "DOCKER_REGISTRY" not in  os.environ.keys():
    print("The environment variable DOCKER_REGISTRY shall be set to the Docker Hub repository with export command")
    sys.exit(1)
elif len(sys.argv) != 3:
    print(f"""The goal of this script is to push Docker images to a Docker Hub repository defined by the DOCKER_REGISTRY variable.

Usage: python3 {sys.argv[0]} username password
- username: Docker Hub username
- password: Docker Hub password""")
    sys.exit(1)
    
try:
    client = docker.from_env()
except Exception as err:
    print(f"Impossible to get Docker environment:\n\n {err}")
    sys.exit(1)

username, password = sys.argv[1:]
repository = os.environ["DOCKER_REGISTRY"]

try:
    response = client.login(username=username, password=password)
except Exception as err:
    print(f"Failed to get Docker Hub identification with username and password:\n\n{repr(err)}")
    sys.exit(1)

pushed = False
for image in client.images.list():
    if repository in image.tags[0]:  # to avoid MariaDB
        for line in client.images.push(f'{image.tags[0]}', stream=True, decode=True):
            print(line)
            pushed = True
    else:
        print(f"{repository} not found in {image.tags[0]}")

if pushed:
    print("Images pushed.\n")
else:
    print("No image pushed.\n")
