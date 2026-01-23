from fastapi import APIRouter, Path, HTTPException
from app.models import ResourceAssessmentRequest
from app.data import utils
from app.helpers import docker_executor

router = APIRouter(prefix="/assess", tags=["api-controller"])


@router.post("/test/{test_identifier:path}")
async def post_test_assessment(test_identifier: str = Path(..., description="Identifier of the test to run"), body: ResourceAssessmentRequest = ...):
    if test_identifier not in utils.TEST_IDENTIFIERS:
        raise HTTPException(status_code=404, detail="Test not found")

    try:
        return await docker_executor.run_assessment(body.resource_identifier, test_identifier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test/{test_identifier:path}")
async def get_test_assessment(
    test_identifier: str = Path(..., description="Dummy method for browser GET petition")
):
    return {
        "message": "This endpoint only accepts POST requests.",
        "example": "curl -X POST \"https://rsfc.linkeddata.es/assess/test/RSFC-13-1\" "
                   "-H \"Content-Type: application/json\" "
                   "-d '{\"resource_identifier\": \"https://github.com/oeg-upm/rsfc\"}'"
    }