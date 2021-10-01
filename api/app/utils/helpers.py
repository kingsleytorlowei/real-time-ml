import pandas as pd

from .utils import execute_query
from ..models import Item

def get_latest_ml_pipeline_version() -> str:
    return execute_query('''
        SELECT pipeline_version
        FROM ml_pipeline
        ORDER BY created_at DESC
        LIMIT 1
    ''')[0][0]

def save_ml_pipeline_version(model_version: str) -> None:
    execute_query('INSERT INTO ml_pipeline (pipeline_version) VALUES(%s)', (model_version,))

async def save_prediction(row: list) -> None:
    query ='''
        INSERT INTO predictions (
            crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat, prediction, pipeline_version
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
    execute_query(query, row)

def convert_item_to_df(item: Item) -> pd.DataFrame:
    items = {}
    for key, value in item.dict().items():
        items[key] = [value]
    return pd.DataFrame(items)