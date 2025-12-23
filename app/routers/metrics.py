from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.data import utils
from app.helpers.fetcher import fetch_json


router = APIRouter(prefix="/metrics", tags=["api-controller"])



@router.get("/")
async def get_metric(metric_id: Optional[str] = Query(None, description="Metric ID to fetch")):
    
    if metric_id == None:
        return utils.METRIC_IDENTIFIERS

    if metric_id not in utils.METRIC_IDENTIFIERS:
        raise HTTPException(status_code=400, detail="Metric ID not valid")

    return await fetch_json(metric_id)