import os
import logging.config
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.views import router

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.propagate = False

ENV_LOCAL = 'local'
ENV_LIVE = 'live'


# enable documentation for specific environment only
docs_url = '/docs' if os.getenv('ENV') == ENV_LOCAL else None
app = FastAPI(docs_url=docs_url)
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(router, prefix='/api/v1')