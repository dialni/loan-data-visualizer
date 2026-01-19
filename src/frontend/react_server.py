import requests
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from time import sleep

timeframe = []

# This cache guarantees 100% uptime
async def UpdateCacheScheduler():
    global timeframe
    while True:
        try:
            resp = requests.get("http://ldr-backend:80/get-timeframe", timeout=5).json()
            timeframe = resp
            print("Frontend cache has been updated.")
            await asyncio.sleep(86000) # 1 day delay between updates
        except:
            sleep(3)

# Creates scheduler task on app start
@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.sleep(5)
    print("Starting UpdateCacheScheduler...")
    asyncio.create_task(UpdateCacheScheduler())
    yield


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

app.mount("/assets", StaticFiles(directory="publish/assets"), name="assets")

templates = Jinja2Templates(directory="publish/pages")

@app.get("/get-timeframe")
def GetTimeframe():
    global timeframe
    return JSONResponse(jsonable_encoder(timeframe))

@app.get("/")
def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return """User-agent: *\nAllow: /"""
