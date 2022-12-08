from fastapi import FastAPI, HTTPException
from requests.exceptions import Timeout
import logging
import json
import os
import requests
import logging


app = FastAPI()
logger = logging.getLogger("uvicorn")
API_URL = {
    'EXPO': 'https://exponea-engineering-assignment.appspot.com/api/work' 
}

@app.get("/api/smart/{timeoutms}")
async def smart_api(timeoutms: int):
    res = []
    timeout_s = float((timeoutms if timeoutms > 0 else 300)/1000)
    for _ in range(3):
        try:
            response = requests.get(API_URL['EXPO'], timeout=timeout_s)
            if response.status_code == 200: 
                res.append(response.json()['time'])
                break
            elif response.status_code == 429:
                raise HTTPException(status_code=429, detail="EXPO API has too many request!")
            else:
                raise HTTPException(status_code=500, detail="Internal Server Error")

        except Timeout as ex:
            raise HTTPException(status_code=408, detail="Timeout has been raised.")

    if len(res) ==  0:
        raise HTTPException(status_code=404, detail="Item are not found.")
    return {"Time": res[0]}
