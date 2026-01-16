from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.data import utils
from app.helpers.fetcher import fetch_json

router = APIRouter(prefix="/benchmarks", tags=["api-controller"])


@router.get("")
async def get_benchmark(benchmarkid: Optional[str] = Query(None, description="Benchmark ID")):
    
    if benchmarkid == None:
        return utils.BENCHMARK_IDENTIFIERS

    if benchmarkid not in utils.BENCHMARK_IDENTIFIERS:
        raise HTTPException(status_code=404, detail="Benchmark not found")

    return await fetch_json(benchmarkid)