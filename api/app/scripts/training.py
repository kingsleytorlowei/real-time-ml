import numpy as np
import pandas as pd
from os import path
import logging.config

from sklearn.datasets import load_boston
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge

from ..utils.helpers import save_ml_pipeline_version

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

SEED = 42
np.random.seed(SEED)

ML_PIPELINES_PATH = 'ml_pipelines/'


def build_pipeline(features_numerical: list, features_categorical: list) -> Pipeline:
    transformer_numerical = StandardScaler()
    transformer_categorical = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(transformers=[('scaler', transformer_numerical, features_numerical),
                                                   ('ohe', transformer_categorical, features_categorical)])

    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', Ridge(random_state=SEED))])
    return pipeline


def get_data():
    boston = load_boston()
    x, y, features = boston.data, boston.target, boston.feature_names
    df = pd.DataFrame(data=x, columns=features)
    return df, y

def train() -> Pipeline:
    df, y = get_data()
    features_categorical = ['CHAS', 'RAD']
    features_numerical =  ['INDUS', 'TAX', 'RM', 'CRIM', 'DIS', 'PTRATIO', 'LSTAT', 'AGE', 'ZN', 'B', 'NOX']
    logger.info(f'Training data: {df.shape}')
    pipeline = build_pipeline(features_numerical, features_categorical)
    logger.info('ML build successful')

    pipeline.fit(df, y)
    logger.info('new ML model trained')
    return pipeline