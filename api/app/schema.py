from sqlalchemy.orm import declarative_base
import datetime
from pytz import timezone
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy import Column, Integer, String,Float, DateTime
UTC = timezone('UTC')

def time_now():
    return datetime.now(UTC)

class MLPipeline(Base):
    __tablename__ = 'ml_pipeline'

    id = Column(Integer, primary_key=True)
    pipeline_version = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return self.id

class Predictions(Base):
    __tablename__  = 'predictions'
    id=Column(Integer, primary_key=True)
    crim = Column(Float)
    zn = Column(Float)
    indus = Column(Float)
    chas = Column(Integer)
    nox = Column(Float)
    rm = Column(Float)
    age = Column(Float)
    dis = Column(Float)
    rad = Column(Integer)
    tax = Column(Float)
    ptratio = Column(Float)
    b = Column(Float)
    lstat = Column(Float)
    