from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import time

app = FastAPI(title="NIRVAHA API", version="0.1.0")

class DriverState(BaseModel):
    state: str  # ATTENTIVE | DROWSY | DISTRACTED
    score: float
    metrics: Dict[str, float]
    ts: float

CURRENT = DriverState(state="ATTENTIVE", score=0.0, metrics={}, ts=time.time())

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/state", response_model=DriverState)
def get_state():
    return CURRENT

@app.post("/state", response_model=DriverState)
def set_state(ds: DriverState):
    global CURRENT
    CURRENT = ds
    return CURRENT
