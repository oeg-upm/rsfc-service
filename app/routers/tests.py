from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from data import utils
from helpers.fetcher import fetch_json


router = APIRouter(prefix="/tests", tags=["api-controller"])


@router.get("/")
async def get_test(test_id: Optional[str] = Query(None, description="Test ID to fetch (optional)")):

    if test_id == None:
        return utils.TEST_IDENTIFIERS

    if test_id not in utils.TEST_IDENTIFIERS:
        raise HTTPException(status_code=400, detail="Test ID not valid")

    return await fetch_json(test_id)