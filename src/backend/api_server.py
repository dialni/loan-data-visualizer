import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from loan_data_visualizer import TimeframeData

# Local object to maintain timeframe data
timeframecache = TimeframeData()

# Self-contained scheduler to clear and update timeframe data every day.
# Responses from this server are delayed during execution, but that is acceptable for this service.
async def UpdateCacheScheduler():
    global timeframecache
    while True:
        await asyncio.sleep(60) # 1 day delay
        print("Updating cache...")
        timeframecache.UpdateTimeframeData()

# Creates scheduler task on app start
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting UpdateCacheScheduler...")
    asyncio.create_task(UpdateCacheScheduler())
    yield

app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

# Public endpoint for getting data in cache
@app.get("/get-timeframe")
def GetTimeframe():
    global timeframecache
    return JSONResponse(jsonable_encoder(timeframecache.GetCache()))