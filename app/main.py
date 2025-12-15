from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import benchmarks, metrics, tests, assess
from helpers import docker_executor


@asynccontextmanager
async def lifespan(app: FastAPI):

    #Startup
    print("Initializing app...")

    try:
        await docker_executor.pull_docker_image()
    except Exception:
        print("Error pulling docker image")
        raise

    print("App initialized correctly.")
    yield

    #Shutdown
    print("Closing app...")


app = FastAPI(
    title="RSFC API service",
    description="RSFC API service",
    version="1.0",
    lifespan=lifespan
)

app.include_router(benchmarks.router, tags=["api-controller"])
app.include_router(metrics.router, tags=["api-controller"])
app.include_router(tests.router, tags=["api-controller"])
app.include_router(assess.router, tags=["api-controller"])
