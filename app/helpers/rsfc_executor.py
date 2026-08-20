import asyncio
import tempfile
import os
import json
import shutil


async def run_assessment(resource_identifier, test_id):
    github_token = None
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../config.json")

    if os.path.isfile(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
                github_token = config.get("github_token")
        except Exception as e:
            print(f"Warning: could not read config.json ({e}), proceeding without github token")

    print(f"Running RSFC assessment for: {resource_identifier}")

    tempdir = tempfile.mkdtemp()

    try:
        cmd = [
            "rsfc",
            "--repo", resource_identifier,
            "--ftr"
        ]

        if test_id is not None:
            cmd.extend(["--id", test_id])

        if github_token:
            cmd.extend(["-t", github_token])

        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=tempdir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode().strip() or stdout.decode().strip()
            raise RuntimeError(f"RSFC process failed with code {process.returncode}: {error_msg}")

        output_dir = os.path.join(tempdir, "rsfc_output")
        report_path = os.path.join(output_dir, "rsfc_assessment.json")

        if not os.path.exists(report_path):
            existing_files = os.listdir(tempdir)
            raise RuntimeError(
                f"rsfc_assessment.json not found in {output_dir}. "
                f"Contents of tempdir: {existing_files}"
            )

        with open(report_path, "r") as f:
            report = json.load(f)

        return report

    except Exception as e:
        raise Exception(f"Error while running RSFC assessment: {e}")

    finally:
        shutil.rmtree(tempdir, ignore_errors=True)