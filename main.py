from datetime import date
from typing import Optional
from uuid import UUID
from xml.sax.handler import feature_namespace_prefixes

# Python
from uuid import UUID
from datetime import date
from datetime import datetime
#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    
class UserLogin(UserBase):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64)

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    birth_date: Optional[date] = Field(default=None)

class Tweet(BaseModel):
    twit_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256)
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

# Path Operations
@app.get(
    path="/",    
)
def home():
    return {"Twitter API": "It's working!"}

## Users

@app.post(
    path="/signup",
    response_model=User,
    status_code=
)
## Tweets
