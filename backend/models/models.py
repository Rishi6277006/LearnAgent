from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define the database engine
engine = create_engine('sqlite:///learnagent.db')

# Base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    total_points = Column(Integer, default=0)  # Total points earned by the user

class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    difficulty = Column(String)

class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    score = Column(Integer, default=0)  # Quiz score for the lesson
    completed_at = Column(DateTime)  # Timestamp of completion