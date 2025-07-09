from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ImageResult(Base):
    __tablename__ = "image_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    predicted_label = Column(String, nullable=False)
    class_index = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
