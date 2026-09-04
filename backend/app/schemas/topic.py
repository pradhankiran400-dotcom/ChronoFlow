from datetime import datetime
from pydantic import BaseModel
from app.database.base import Base

class TopicCreate(BaseModel):
    name:str
    description : str|None =None

class TopicUpdate(BaseModel):
    name:str|None = None
    description : str|None = None

class TopicResponse(BaseModel):
    id:int
    name:str
    description : str|None = None
    created_at:datetime


    class Config:
        form_attributes = True