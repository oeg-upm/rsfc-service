from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import benchmarks, metrics, tests, assess
from app.helpers import docker_executor


async def initialize_services():
    try:
        await docker_executor.pull_docker_image()
    except Exception as e:
        print(f"Error initializing services: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):

    #Startup
    print("Initializing app...")
    await initialize_services()
    print("App initialized correctly.")
    yield
    #Shutdown
    print("Closing app...")


origins = [
    "https://rsfc.linkeddata.es"
]

app = FastAPI(
    title="RSFC API service",
    description="RSFC API service",
    version="1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [benchmarks, metrics, tests, assess]:
    app.include_router(router.router)
