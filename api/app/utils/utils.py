import os
import psycopg2
import logging 
from configparser import ConfigParser, BasicInterpolation

logger = logging.getLogger(__name__)

class EnvInterpolation(BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)

def get_config_params(config_path: str, section: str):
    config = ConfigParser(interpolation=EnvInterpolation())
    config.read(config_path)
    return config[section]

def execute_query(query: str, data=None, config_file='config.ini', config_section='postgres_db'):
    db_params = get_config_params(config_file, config_section)
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        if 'select' in query.lower():
            cursor.execute(query)
            return cursor.fetchall()
        else:
            cursor.execute(query, data)
            connection.commit
    except Exception as e:
        logger.error('Error while connecting to PostgreSQL', e)
    finally:
        if connection:
            cursor.close()
            connection.close()