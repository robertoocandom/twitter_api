# Python
from email import contentmanager, message
from http.client import HTTPException
import json
from os import remove
from unittest import result
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List
import uuid


#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import Body, FastAPI, Path, Form
from fastapi import status, HTTPException

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

class LogIn(BaseModel):
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

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

class UserRegister(User):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64)

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256)
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Path Operations (End Points)

## Users

### Register a User
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    SingUp

    This path operations register a User in the app

    - Parameters:
        - Request body parameter
            - user: UserRegister

    - Returns a json with the basic user information:
        - user_id: UUID
        - email: EmailStr
        - Firt_name: str
        - last_name: str
        - birth_date: datatime
    """
    
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(email: EmailStr = Form(..., example="Lorena@example.com"), password: str = Form(..., example="ClvdeLorena")):
    pass
    """
    This path operations login a user in the app

    - Parameters:
        - email : EmailStr
        - password : str

    - Returns a LoginOut model with username and message
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        data = json.loads(f.read())
        for users in data:
            if email == users['email'] and password == password['password']:
                return LogIn(email=email)
            else:
                return LogIn(email=email, message="!!Wrong Credentials!!, please check! and try again!")
                

### Show all Users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    This path operations shows all users in the app

    - Parameters:
        -

    - Returns a json list with all users in the app with the following keys:
        - user_id: UUID
        - email: EmailStr
        - Firt_name: str
        - last_name: str
        - birth_date: datatime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user(user_id: UUID = Path(
    ...,
    title="User ID",
    descripcion="This is the user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
):
    """
    This path operations shows a user in the app

    - Parameters:
        - user_id: UUID

    - Returns the information od an user:
        - user_id: UUID
        - email: EmailStr
        - Firt_name: str
        - last_name: str
        - birth_date: datatime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(user_id)
        for data in results:
            if data['user_id'] == id:
                return data
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user doesn't exist!")


### Delete a User
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id: UUID = Path(
    ..., 
    title="User ID",
    description="This is the user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa6", message="User Deleted successfully!!")):
    """
    This path operations to Delete a user in the app

    - Parameters:
        - user_id: UUID

    - Returns user data Deleted
        
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(user_id)
        for data in results:
            if data['user_id'] == id:
                results.remove(data)
                with open("users.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return data, message
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user doesn't exist!")
    

### Update a User
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(user_id: UUID = Path(
    ...,
    title="User ID",
    detail="This is the user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa9",
    message="User Updated Successfully!"),
    user: UserRegister = Body(...)):   
    """
    Update User

    This is the Path Operations update an user in the app

    - Parameters:
        - User_ID: UUID
        - Request a body parameter:
            - user: User --> A user model with user_id, email, first name, last name, birth date and password.

    - Returns User Model with user_id, email, first name, last name, birth date, If the User doesn't exist, the path return the exception 404. 
    """
    user_id = str(user_id)
    user_dict = user.dict()
    user.dict["user_id"] = str(user.dict["user_id"])
    user.dict["birth_date"] = str(user.dict["birth_date"])
    
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(user_id)
        for user in results:
            if user['user_id'] == id:
                results[results.index(user)] = user_dict
                with open("users.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="!This user_id doesn't exist!") 

## Tweets
### Show all Tweets

@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
    )
def home():
    """
    This path operations shows all tweets in the app

    - Parameters:
        -

    - Returns a json list with all tweets in the app with the following keys:
        - twit_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a Tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a tweet

    This path operations post a tweet in the app

    - Parameters:
        - Request body parameter
            - tweet: UserRegister

    - Returns a json with the basic tweet information:
        - twit_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """    
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])

        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a Tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a Tweet",
    tags=["Tweets"]
)
def show_a_tweet(tweet_id: UUID = Path(...,
    title="Tweet ID",
    description="This is a Tweet",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa8")
    ):
    
    """
    This path operations shows a Tweet in the app

    - Parameters:
        - Tweet_id: UUID

    - Returns all information about a specific tweet:
        - user_id: UUID
        - email: EmailStr
        - Firt_name: str
        - last_name: str
        - birth_date: datatime
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(tweet_id)
        for data in results:
            if data['tweet_id'] == id:
                return data
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This Tweet doesn't exist!")    

### Delete a Tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
    tags=["Tweets"]
)
def delete_a_tweet(
    tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="This is a Tweet",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa8")):
    """
    Delete Tweet

    This Path operation delete a Tweet

    - Parameters:
        - tweet_id : UUID

    Returns Tweet data Deleted
    """
    
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(tweet_id)
        for data in results:
            if data['tweet_id'] == id:
                results.remove(data)
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return data
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This tweet doesn't exist!!")


### Update a Tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    tags=["Tweets"]
)
def update_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="This is the Tweet ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa7"
    ),
    content: str = Form(...,
    min_length=1,
    max_length=256,
    title="Tweet Content Updated",
    description="This is the content o the tweet updated"
    )):
    """
    Update Tweet

    This path operation update a tweet information

    - Parameters:
        - tweet_id: UUID
        - content: str
        - created_at: datatime
        - updated_at: datetime
        - by: user: User
    """
    tweet_id = str(tweet_id)
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        for tweet in results:
            if tweet["tweet_id"] == tweet_id:
                tweet['content'] = content
                tweet["updated_at"] = str(datetime.now())
                print(tweet)
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.loads(results))
                    return tweet
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="!This tweet_id doesn't exist!")

