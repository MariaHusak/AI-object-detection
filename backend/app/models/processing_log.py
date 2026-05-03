from sqlalchemy import Column, Integer, Float, ForeignKey
from app.core.database import Base


class ProcessingLog(Base):
    __tablename__ = "processing_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    processing_time = Column(Float)
    accuracy = Column(Float)
