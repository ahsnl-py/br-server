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
    def service(timeout_s, attempt):
        try:
            trial = attempt - 1

            if trial >= 0:
                response = requests.get(API_URL['EXPO'], timeout=timeout_s)
                if response.status_code == 200: 
                    return res.append(response.json()['time'])
                elif response.status_code == 429:
                    raise HTTPException(status_code=429, detail="EXPO API has too many request!")
                else:
                    raise HTTPException(status_code=404, detail="Item are not found.")
            return None    
            
        except Timeout as ex:
            logger.warning(f"Exception raised: {ex}. Attempt %d" % trial)
            service(timeout_s, trial)                

    service(float((timeoutms if timeoutms > 0 else 300)/1000), 3)
    if len(res) == 0:
        raise HTTPException(status_code=408, detail="Attempt limit exceeded.")
    return {"Time": res[0]}
