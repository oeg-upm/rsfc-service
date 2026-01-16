import subprocess
from app.data import utils
import tempfile
import os
import json


async def pull_docker_image():

    print("Pulling RSFC Docker image")
    
    subprocess.run(
        ["docker", "pull", utils.RSFC_DOCKER_IMAGE],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("Image pulled succesfully")


async def run_assessment(resource_identifier, test_id):
    
    print("Running RSFC container")
    
    tempdir = tempfile.mkdtemp()

    try:

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v", f"{tempdir}:/rsfc/rsfc_output",
            utils.RSFC_DOCKER_IMAGE,
            "--repo",
            resource_identifier,
            "--ftr"
        ]
        
        if test_id != None:
            test_id = test_id.rstrip("/").split("/")[-1]
            cmd.extend(["--id", test_id])

        subprocess.run(cmd, capture_output=True, text=True)
        
        files = os.listdir(tempdir)
        if len(files) != 1:
            print("Error: RSFC did not generate any output files")
            raise

        report_path = os.path.join(tempdir, files[0])
        with open(report_path) as f:
            report = json.load(f)
        
        return report


    except Exception as e:
        raise Exception(f"Error while running the container: {e}")
