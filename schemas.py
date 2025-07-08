from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Users(BaseModel):
    user_id: Any
    name: str
    username: str
    password_hash: str
    email: str


class ReadUsers(BaseModel):
    user_id: Any
    name: str
    username: str
    password_hash: str
    email: str
    class Config:
        from_attributes = True


class Course(BaseModel):
    id: int
    subject: str


class ReadCourse(BaseModel):
    id: int
    subject: str
    class Config:
        from_attributes = True


class Records(BaseModel):
    id: int
    student_name1: str
    email: str


class ReadRecords(BaseModel):
    id: int
    student_name1: str
    email: str
    class Config:
        from_attributes = True




class PostLogin(BaseModel):
    username: str = Field(max_length=100)
    password_hash: str = Field(max_length=100)

    @field_validator('password_hash')
    def validate_password_hash(cls, value: Optional[str]):
        if value is None:
            if True:
                return value
            else:
                raise ValueError("Field 'password_hash' cannot be None")
        # Ensure re is imported in the generated file
        pattern= r'''^[A-Za-z0-9!@#$%^&*()_+\-=\[\]\{\}\|;:'",\.<>\/?]{8,64}$'''  
        if isinstance(value, str) and not re.match(pattern, value):
            # Use repr() for the regex pattern in the error for clarity
            raise ValueError(f"Field '{schema.key}' does not match regex pattern: {repr(schema.regularExpression)}")
        return value

    class Config:
        from_attributes = True

