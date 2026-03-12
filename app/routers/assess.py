from fastapi import APIRouter, Path, HTTPException, Header
from app.models import ResourceAssessmentRequest
from app.data import utils
from app.helpers import docker_executor, render_template

router = APIRouter(prefix="/assess", tags=["api-controller"])


@router.post("/test/{test_identifier:path}")
async def post_test_assessment(test_identifier: str = Path(..., description="Identifier of the test to run"), body: ResourceAssessmentRequest = ...):
    if test_identifier not in utils.TEST_IDENTIFIERS and test_identifier not in utils.TEST_SHORTIDS:
        raise HTTPException(status_code=404, detail="Test not found")
    else:
        if test_identifier in utils.TEST_IDENTIFIERS:
            test_identifier = test_identifier.rstrip("/").rsplit("/", 1)[-1]

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
    
    
@router.post("/scoringAlgorithm")
async def post_test_assessment(body: ResourceAssessmentRequest = ...):

    try:
        assessment = await docker_executor.run_assessment(body.resource_identifier, None)
        
        test_results = assessment["hadMember"]
        total_tests = len(test_results)
        passed_tests = sum(1 for test in test_results if test["value"] == "true")
        score = round((passed_tests/total_tests)*100)
        log = f"Since you passed {passed_tests}/{total_tests} tests, your score is {score}%"
        
        return render_template.render_benchmark_score(score=score, log=log, checks=test_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))