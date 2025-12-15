from fastapi import APIRouter, Query, HTTPException, Path
from typing import Optional
from models import ResourceAssessmentRequest
from data import utils
from helpers import docker_executor

router = APIRouter(prefix="/assess", tags=["api-controller"])

@router.post("/{test_id}")
async def post_test_assessment(test_id: str = Path(..., description="Identifier of the test to run"), body: ResourceAssessmentRequest = ...):

    if test_id != None and test_id not in utils.TEST_IDENTIFIERS:
        raise HTTPException(status_code=400, detail="Test ID not valid")
    
    resource_id = body.resource_identifier
    
    try:
        result = await docker_executor.run_assessment(resource_id)
        return {
            "test_id": test_id,
            "resource_identifier": resource_id,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))