from .worker import app
from os import path

from celery.utils.log import get_task_logger
from app.scripts.training import train, logger, ML_PIPELINES_PATH
from datetime import datetime
from joblib import dump
from app.utils.helpers import save_ml_pipeline_version
from celery.decorators import periodic_task
from datetime import timedelta

celery_log = get_task_logger(__name__)

@app.task(name='boston_housing.train_model')
def train_model():
    pipeline = train()
    new_version = datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
    dump(pipeline, path.join(ML_PIPELINES_PATH, f'pipeline_{new_version}.joblib'))
    logger.info(f'The new pipeline "{new_version}" was successfully saved.')
    save_ml_pipeline_version(new_version)
    logger.info(f'machine learning  pipeline successfully saved to database')



@periodic_task(run_every=timedelta(hours=6))
def refresh_ml_model():
    train_model()