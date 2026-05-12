from app.core.database import engine
from app.models.user import User
from app.models.processing_log import ProcessingLog

from app.core.database import Base

Base.metadata.create_all(bind=engine)

print("Database tables created")