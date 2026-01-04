from fastapi import FastAPI, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from loan_data_visualizer import UpdateTimeframeData
from os import getenv
from dotenv import load_dotenv

class ChallengeCode(BaseModel):
    code: str

if not load_dotenv('.env'):
    raise SystemExit("api_server.py could not open .env, exiting...")

if getenv("API_SERVER_CHALLENGECODE") == None:
    raise SystemExit("API_SERVER_CHALLENGECODE not set, exiting...")

app = FastAPI(docs_url=None, redoc_url=None)

# Public endpoint for getting data in cache
@app.get("/get-timeframe")
def GetTimeframe():
    try: app.state.timeframeCache != None
    except AttributeError: return JSONResponse(jsonable_encoder([]))    
    return JSONResponse(jsonable_encoder(app.state.timeframeCache))

# Private method for starting data caching
def StartUpdateTimeframeJob():
    '''Background job to create a new Timeframe'''
    print(f"Lock state: {app.state.timeframeLock}")
    app.state.timeframeCache = UpdateTimeframeData()
    app.state.timeframeLock = False
    print(f"Lock state: {app.state.timeframeLock}")

# Public endpoint for starting the data caching, if the correct password is provided.
# This is intended to be used with a cronjob to start at certain times of the day,
@app.post("/update-timeframe")
def UpdateTimeframe(challengeCode: ChallengeCode, background_tasks: BackgroundTasks):
    try: app.state.timeframeLock != None
    except AttributeError:
        app.state.timeframeLock = False
        app.state.timeframeCache = []
    if challengeCode.code != getenv("API_SERVER_CHALLENGECODE"):
        return Response("403\n", 403)
    if app.state.timeframeLock == True:
        return Response("409\n", 409)
    app.state.timeframeLock = True
    background_tasks.add_task(StartUpdateTimeframeJob)
    return Response("202\n", 202)