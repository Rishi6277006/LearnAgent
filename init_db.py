from sqlalchemy import create_engine
from backend.models.models import Base

engine = create_engine('sqlite:///learnagent.db')
Base.metadata.create_all(engine)