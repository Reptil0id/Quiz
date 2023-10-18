from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import List
from sqlalchemy.exc import IntegrityError
import httpx

DATABASE_URL = "postgresql://myuser:mypassword@postgres:5432/mydatabase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    answer_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class QuestionRequest(BaseModel):
    questions_num: int

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    answer_text: str
    created_at: datetime

@app.post("/get_questions/", response_model=List[QuestionResponse])
async def get_questions(question_request: QuestionRequest):
    async with httpx.AsyncClient() as client:
        count = question_request.questions_num
        questions = []

        db = SessionLocal()

        while len(questions) < count:
            response = await client.get("https://jservice.io/api/random?count=1")
            data = response.json()

            if data:
                question_text = data[0]["question"]
                answer_text = data[0]["answer"]
                existing_question = db.query(Question).filter_by(question_text=question_text).first()

                if not existing_question:
                    question = Question(question_text=question_text, answer_text=answer_text)
                    try:
                        db.add(question)
                        db.commit()
                        db.refresh(question)
                        questions.append(question)
                    except IntegrityError:
                        db.rollback()

        db.close()
        return questions

@app.get("/get_question/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int):
    db = SessionLocal()
    question = db.query(Question).filter_by(id=question_id).first()
    db.close()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    question_response = QuestionResponse(
        id=question.id,
        question_text=question.question_text,
        answer_text=question.answer_text,
        created_at=question.created_at
    )

    return question_response

@app.get("/list_questions/", response_model=List[QuestionResponse])
def list_questions():
    db = SessionLocal()
    questions = db.query(Question).all()
    db.close()
    
    questions_response = [
        QuestionResponse(
            id=question.id,
            question_text=question.question_text,
            answer_text=question.answer_text,
            created_at=question.created_at
        )
        for question in questions
    ]
    
    return questions_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
