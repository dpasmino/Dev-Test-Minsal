from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Schema for phone numbers
class Phone(BaseModel):
    number: str
    citycode: str
    countrycode: str

# Schema for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phones: List[Phone]

# Schema for user output
class UserOut(BaseModel):
    username: str
    email: EmailStr
    id: str
    created: str
    modified: str
    last_login: str
    token: str
    isactive: bool