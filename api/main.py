import os
import logging.config
from joblib import load
from typing import Dict, Any

from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse

from app.utils.helpers import get_latest_ml_pipeline_version, convert_item_to_df, save_prediction
from app.models import Item
from app.scripts.training import ML_PIPELINES_PATH


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.propagate = False

ENV_LOCAL = 'local'
ENV_LIVE = 'live'

CACHE: Dict[str, Any] = {}

# enable documentation for specific environment only
docs_url = '/docs' if os.getenv('ENV') == ENV_LOCAL else None
app = FastAPI(docs_url=docs_url)

@app.get('/health')
def health_check():
    content = {
        'Server status': 'Ok',
        'DB Connection': 'Ok'
    }
    try:
        ml_pipeline_version = get_latest_ml_pipeline_version()
    except Exception:
        content['DB Connection'] = 'DB unavailable'
        return JSONResponse(content=content)

    if os.path.isfile(os.path.join(ML_PIPELINES_PATH, f'pipeline_{ml_pipeline_version}.pickle')):
        content['ML_Pipeline'] = 'Ok' if os.getenv('ENV') == ENV_LIVE else ml_pipeline_version
    else:
        content['ML_Pipeline'] = 'ML pipeline unavailable'

    return JSONResponse(content=content)

@app.post('/predict')
async def predict(item: Item, response: Response):
    pipeline_version = get_latest_ml_pipeline_version()

    if CACHE.get('ml_pipeline_version', None) != pipeline_version:
        try:
            ml_pipeline = load(os.path.join(ML_PIPELINES_PATH, f'pipeline_{pipeline_version}.pickle'))
            CACHE['ml_pipeline'] = ml_pipeline
            CACHE['ml_pipeline_version'] = pipeline_version
        except FileNotFoundError:
            logger.error(f'The ML pipeline version {pipeline_version} doesnt not exist')
            response.status_code = status.HTTP_404_NOT_FOUND
            content = {
                'status': 'The model was not found',
            }
            return JSONResponse(
                content = content,
                status_code=status.HTTP_404_NOT_FOUND
            )
    df = convert_item_to_df(item)
    prediction = CACHE['ml_pipeline'].predict(df)[0]
    await save_prediction(df.values.tolist()[0] + [prediction, pipeline_version])
    content = {
        'prediction': prediction
    }
    return JSONResponse(content=content)