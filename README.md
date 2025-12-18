

# RSFC API Service

A REST API to call RSFC (Research Software FAIRness Checks) via requests.

## API endpoints

GET /benchmarks/{benchmark_id}
GET /metrics/{metric_id}
GET /tests/{test_id}
POST /assess/{repo_url}/{test_id}


## Usage

Preferably in a virtual environment and inside the app/ directory, run the following to run the app:

```
uvicorn main:app
```