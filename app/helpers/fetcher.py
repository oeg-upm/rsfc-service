import requests
from fastapi import HTTPException

async def fetch_json(url):
    try:
        response = requests.get(url, headers={"Accept": "application/ld+json"})

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")
        elif response.status_code == 403:
            raise HTTPException(status_code=403, detail="Forbidden")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Not found")
        elif response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail="Error fetching resource")

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {e}")