from fastapi import APIRouter, HTTPException, Path
from typing import Optional
from data import utils
from helpers.fetcher import fetch_json


router = APIRouter(prefix="/metrics", tags=["api-controller"])

@router.get("/{metric_id}")
async def get_metric(metric_id: Optional[str] = Path(None, description="Metric ID to fetch (optional)")):
    
    if metric_id is None:
        return utils.METRIC_IDENTIFIERS

    if metric_id not in utils.METRIC_IDENTIFIERS:
        raise HTTPException(status_code=400, detail="Metric ID not valid")

    return await fetch_json(metric_id)