from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from models import ResourceAssessmentRequest
import requests
import rdflib
from data import utils


app = FastAPI(title="RSFC API documentation", description="RSFC API documentation", version="1.0")


@app.post("/assess/test/{test_identifier}", tags=["api-controller"])
async def post_test_assessment(test_identifier: str = Path(..., description="Identifier of the test to run"), body: ResourceAssessmentRequest = ...):

    pass

@app.get("/benchmarks", tags=["api-controller"])
async def get_benchmarks(benchmark_id: Optional[str] = Query(None, description="Optional benchmark ID")):
    
    if benchmark_id == None:
        return utils.BENCHMARK_IDENTIFIERS

    try:
        if benchmark_id not in utils.BENCHMARK_IDENTIFIERS:
            raise HTTPException(status_code=400, detail="Benchmark ID not valid")
        
        else:
        
            response = requests.get(benchmark_id, headers={"Accept": "application/ld+json"})
            #Pasar esto a JSON-LD y FTR

            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized")
            elif response.status_code == 403:
                raise HTTPException(status_code=403, detail="Forbidden")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Benchmark not found")
            elif response.status_code >= 400:
                raise HTTPException(status_code=response.status_code, detail="Error fetching benchmark")

            return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to benchmark URL: {e}")

@app.get("/metrics", tags=["api-controller"])
async def get_metrics(metric_id: Optional[str] = Query(None, description="Optional metric ID")):
    
    if metric_id == None:
            return utils.METRIC_IDENTIFIERS
    
    try:
        if metric_id not in utils.METRIC_IDENTIFIERS:
            raise HTTPException(status_code=400, detail="Metric ID not valid")
        
        else:
        
            response = requests.get(metric_id, headers={"Accept": "application/ld+json"})
            #Pasar esto a FTR

            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized")
            elif response.status_code == 403:
                raise HTTPException(status_code=403, detail="Forbidden")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Metric not found")
            elif response.status_code >= 400:
                raise HTTPException(status_code=response.status_code, detail="Error fetching metric")

            return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to metric URL: {e}")

@app.get("/tests", tags=["api-controller"])
async def get_tests(test_id: Optional[str] = Query(None, description="Optional test ID")):
    
    if test_id == None:
            return utils.TEST_IDENTIFIERS
    
    try:
        if test_id not in utils.TEST_IDENTIFIERS:
            raise HTTPException(status_code=400, detail="Test ID not valid")
        
        else:
            
            response = requests.get(test_id, headers={"Accept": "application/ld+json"})
            #Pasar esto a FTR

            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized")
            elif response.status_code == 403:
                raise HTTPException(status_code=403, detail="Forbidden")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Metric not found")
            elif response.status_code >= 400:
                raise HTTPException(status_code=response.status_code, detail="Error fetching metric")

            return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to metric URL: {e}")