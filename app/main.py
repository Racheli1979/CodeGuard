from importlib import reload

import uvicorn
from fastapi import FastAPI
from app.routes import analyze, alerts

app = FastAPI()

app.include_router(analyze.router)
app.include_router(alerts.router)

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='localhost', port=8000)
