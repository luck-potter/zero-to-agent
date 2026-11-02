from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)
    language: str = "en"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello/{name}")
def say_hello(name: str, language: str = "en"):
    if language == "en":
        return {"message": f"Hello, {name}!"}
    return {"message": f"你好，{name}！"}

@app.post("/questions")
def read_questions(question: QuestionRequest):
    return {"question": question.question, "language": question.language}