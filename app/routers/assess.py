from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.models import ResourceAssessmentRequest
from app.data import utils
from app.helpers import docker_executor

router = APIRouter(prefix="/assess", tags=["api-controller"])


@router.post("/")
async def post_assessment(body: ResourceAssessmentRequest, test_id: Optional[str] = Query(None, description="Identifier of the test to run")):
    
    if not body.resource_identifier:
        raise HTTPException(status_code=400, detail="Resource_identifier is required")

    if test_id is not None and test_id not in utils.TEST_IDENTIFIERS:
        raise HTTPException(status_code=400, detail="Test ID not valid")

    resource_id = body.resource_identifier

    try:
        result = await docker_executor.run_assessment(resource_id, test_id)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
