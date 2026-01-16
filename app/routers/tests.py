from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.data import utils
from app.helpers.fetcher import fetch_json


router = APIRouter(prefix="/tests", tags=["api-controller"])


@router.get("")
async def get_test(testid: Optional[str] = Query(None, description="Test ID to fetch (optional)")):

    if testid == None:
        return utils.TEST_IDENTIFIERS

    if testid not in utils.TEST_IDENTIFIERS:
        raise HTTPException(status_code=404, detail="Test not found")

    return await fetch_json(testid)