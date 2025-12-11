from fastapi import APIRouter, Query, HTTPException, Path
from typing import Optional
from data import utils
from helpers.fetcher import fetch_json

router = APIRouter(prefix="/benchmarks", tags=["api-controller"])

@router.get("/{benchmark_id}")
async def get_benchmark(benchmark_id: Optional[str] = Path(None, description="Benchmark ID to fetch (optional)")):
    
    if benchmark_id is None:
        return utils.BENCHMARK_IDENTIFIERS

    if benchmark_id not in utils.BENCHMARK_IDENTIFIERS:
        raise HTTPException(status_code=400, detail="Benchmark ID not valid")

    return await fetch_json(benchmark_id)