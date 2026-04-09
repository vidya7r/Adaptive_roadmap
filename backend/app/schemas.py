from pydantic import BaseModel
from typing import Dict

class SubtopicBase(BaseModel):
    title: str
    description: str

class SubtopicCreate(SubtopicBase):
    topic_id: int

class SubtopicResponse(SubtopicBase):
    id: int

    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

class SubmitAnswers(BaseModel):
    topic_id: int
    answers: Dict[str, str]

class SubmitSubtopicAnswers(BaseModel):
    subtopic_id: int
    answers: Dict[str, str]