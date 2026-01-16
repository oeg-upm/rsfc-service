

# RSFC API Service

A REST API to call RSFC (Research Software FAIRness Checks) via requests.

## API endpoints

- GET /benchmarks/{benchmarkid}
- GET /metrics/{metricid}
- GET /tests/{testid}
- POST /assess/test/{test_identifier}


## Usage

Preferably in a virtual environment and inside the app/ directory, run the following to run the app:

```
uvicorn main:app
```

**Note**: The application will try to pull the docker image for RSFC, which is strictly necessary.

After the preparations are done, you can perform requests to the API. Here are some examples:

- Fetch a benchmark using its id

```
curl -G "http://localhost:8000/benchmarks/benchmarkid=https://w3id.org/rsfc/benchmark/FAIR4RS" \
  -H "Accept: application/ld+json"

```

- Fetch a metric using its id

```
curl -G "http://localhost:8000/metrics/metricid=https://w3id.org/everse/i/indicators/software_has_license" \
  -H "Accept: application/ld+json"
```

- Fetch a test using its id

```
curl -G "http://localhost:8000/tests/testid=https://w3id.org/rsfc/test/RSFC-01-1" \
  -H "Accept: application/ld+json"

```

- Perform an assessment on a repository for a certain test

```
curl -X POST "http://localhost:8000/assess/test/https://w3id.org/rsfc/test/RSFC-13-1" \
  -H "Content-Type: application/json" \
  -d '{
    "resource_identifier": "https://github.com/oeg-upm/rsfc"
  }'
```

