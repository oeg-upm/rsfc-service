

# RSFC API Service

A REST API to call RSFC (Research Software FAIRness Checks) via requests.

## API endpoints

- GET /benchmarks/{benchmarkid}
- GET /metrics/{metricid}
- GET /tests/{testid}
- POST /assess/test/{test_identifier}

# Requirements

The API was developed using Python 3.12.0

Dependencies are available in the requirements.txt file located in the root of the repository

# Install from Github

Simply clone this repository

```
git clone https://github.com/oeg-upm/rsfc-service.git
```

## Usage

**Note**: We have an available service deployed online that accepts requests. To use it, just change the http://localhost:8000 url for https://rsfc.linkeddata.es

Preferably in a virtual environment and in the root directory of the project, run the following to run the app:

```
uvicorn app.main:app
```

The application will try to pull the docker image for RSFC, which is strictly necessary. Said image can be found on [DockerHub](https://hub.docker.com/r/amonterodx/rsfc)

After the preparations are done, you can perform requests to the API. Here are some examples:

- Fetch a benchmark using its id

```
curl -G "http://localhost:8000/benchmarks?benchmarkid=https://w3id.org/rsfc/benchmark/FAIR4RS" \
  -H "Accept: application/ld+json"

```

- Fetch a metric using its id

```
curl -G "http://localhost:8000/metrics?metricid=https://w3id.org/everse/i/indicators/software_has_license" \
  -H "Accept: application/ld+json"
```

- Fetch a test using its id

```
curl -G "http://localhost:8000/tests?testid=https://w3id.org/rsfc/test/RSFC-01-1" \
  -H "Accept: application/ld+json"

```

- Perform an assessment on a repository for a certain test

**Note**: The use of a Github token is mandatory for this request.

```
curl -X POST "http://localhost:8000/assess/test/RSFC-13-1" \
  -H "Content-Type: application/json" \
  -d '{
    "resource_identifier": "https://github.com/oeg-upm/rsfc"
  }'
```