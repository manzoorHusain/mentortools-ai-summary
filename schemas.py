# Author: Manzoor Hussain

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Request: Create User
class UserCreate(BaseModel):
    name: str
    email: EmailStr


# Response: Read User
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# Request: Create Course
class CourseCreate(BaseModel):
    user_id: int
    course_title: str
    course_description: str


# Response: Read Course
class CourseOut(BaseModel):
    id: int
    user_id: int
    course_title: str
    course_description: str
    ai_summary: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class CourseUpdate(BaseModel):
    course_title: Optional[str] = None
    course_description: Optional[str] = None
    status: Optional[str] = None


class SummaryUpdate(BaseModel):
    ai_summary: str
