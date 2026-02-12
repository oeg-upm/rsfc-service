from fastapi import APIRouter, Path, HTTPException, Header
from app.models import ResourceAssessmentRequest
from app.data import utils
from app.helpers import docker_executor, render_template

router = APIRouter(prefix="/assess", tags=["api-controller"])


@router.post("/test/{test_identifier:path}")
async def post_test_assessment(test_identifier: str = Path(..., description="Identifier of the test to run"), body: ResourceAssessmentRequest = ..., authorization: str = Header(..., description="Bearer GitHub token")):
    if test_identifier not in utils.TEST_IDENTIFIERS:
        raise HTTPException(status_code=404, detail="Test not found")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    github_token = authorization.split(" ", 1)[1]

    if not github_token:
        raise HTTPException(status_code=401, detail="Empty token")

    try:
        return await docker_executor.run_assessment(body.resource_identifier, test_identifier, github_token)
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
    
    
@router.post("/benchmarkScore")
async def post_test_assessment(body: ResourceAssessmentRequest = ..., authorization: str = Header(..., description="Bearer GitHub token")):


    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    github_token = authorization.split(" ", 1)[1]

    if not github_token:
        raise HTTPException(status_code=401, detail="Empty token")

    try:
        assessment = await docker_executor.run_assessment(body.resource_identifier, None, github_token)
        
        test_results = assessment["hadMember"]
        
        total_tests = len(test_results)

        passed_tests = sum(1 for test in test_results if test["value"] == "true")

        score = passed_tests / total_tests
        
        log = f"Since you passed {passed_tests}/{total_tests} tests, your score is {score}"
        
        benchmark_id = utils.RSFC_BENCHMARK_ID
        
        return render_template.render_benchmark_score(benchmark_id=benchmark_id, score=score, log=log)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))