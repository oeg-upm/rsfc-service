from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from data import utils
from helpers.fetcher import fetch_json

router = APIRouter(prefix="/benchmarks", tags=["api-controller"])


@router.get("/")
async def get_benchmark(benchmark_id: Optional[str] = Query(None, description="Benchmark ID")):
    
    if benchmark_id == None:
        return utils.BENCHMARK_IDENTIFIERS

    if benchmark_id not in utils.BENCHMARK_IDENTIFIERS:
        raise HTTPException(status_code=400, detail="Benchmark ID not valid")

    return await fetch_json(benchmark_id)