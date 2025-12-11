from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import benchmarks, metrics, tests, assess
from helpers import docker_executor


@asynccontextmanager
async def lifespan(app: FastAPI):

    #Startup
    print("Initializing app...")

    await docker_executor.pull_docker_image()

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

app.include_router(benchmarks.router, prefix="/benchmarks", tags=["api-controller"])
app.include_router(metrics.router, prefix="/metrics", tags=["api-controller"])
app.include_router(tests.router, prefix="/tests", tags=["api-controller"])
app.include_router(assess.router, prefix="/assess", tags=["api-controller"])
