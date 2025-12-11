#Debe pullear la imagen de dockerhub y despues correrla (fijarse en resqui)

import docker

client = docker.from_env()

def docker_executor(url: str, test_id: str = None):

    command = f"--url {url}"
    if test_id:
        command += f" --test_id {test_id}"
    
    # Lanza el contenedor
    container = client.containers.run(
        "nombre_de_tu_imagen_docker",
        command=command,
        detach=True,
        remove=True
    )
    
    # Espera a que termine y recoge logs
    result = container.logs(stdout=True, stderr=True)
    return result.decode('utf-8')
