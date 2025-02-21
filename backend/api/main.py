from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.models.models import User, engine  # Import your SQLAlchemy models
from backend.agents.agent import generate_lesson  # Import your lesson generation function
from langchain_openai import ChatOpenAI
import json
import os

# Initialize the FastAPI app
app = FastAPI()

# Pydantic model for user creation
class UserCreate(BaseModel):
    name: str
    email: str

# Create database tables if they don't exist
from backend.models.models import Base  # Import your declarative base
Base.metadata.create_all(bind=engine)

@app.post("/users/")
def create_user(user: UserCreate):
    db = Session(bind=engine)
    try:
        # Check if the user already exists
        existing_user = db.query(User).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Create a new user
        new_user = User(name=user.name, email=user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Return the user data, including the ID
        return {"id": new_user.id, "name": new_user.name, "email": new_user.email}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with this email already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to verify user email (for login)
@app.get("/users/")
def get_user(email: str):
    db = Session(bind=engine)
    try:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user_id": user.id, "name": user.name, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lesson/")
def get_lesson(topic: str, level: str = "Beginner", preference: str = "Theoretical", user_id: int = None):
    try:
        lesson_content = generate_lesson(topic, level, preference)

        # Award points for completing the lesson
        if user_id:
            db = Session(bind=engine)
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                user.total_points += 10  # Award 10 points for completing a lesson
                db.commit()

        return {"topic": topic, "content": lesson_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
openai_api_key = os.getenv("OPENAI_API_KEY")
