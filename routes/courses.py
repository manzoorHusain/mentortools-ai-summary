# Author: Manzoor Hussain

import os
from datetime import datetime, timedelta
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Header, status
from openai import OpenAI
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import AsyncSessionLocal
from models import User, Course
from schemas import CourseOut, CourseCreate, CourseUpdate, SummaryUpdate

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/courses/", response_model=List[CourseOut])
async def get_courses(db: AsyncSession = Depends(get_db)) -> List[Course]:
    result = await db.execute(select(Course))
    courses = result.scalars().all()

    return list(courses)


@router.post("/courses/", response_model=CourseOut)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)) -> Course:
    # Check if user exists
    result = await db.execute(select(User).where(User.id == course.user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(
        select(Course).where(
            Course.course_title == course.course_title,
            Course.user_id == course.user_id
        )
    )
    existing_course = result.scalar_one_or_none()
    if existing_course:
        raise HTTPException(status_code=404, detail="Course already found")

    new_course = Course(
        user_id=course.user_id,
        course_title=course.course_title,
        course_description=course.course_description
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    return new_course


@router.get("/courses/{course_id}", response_model=CourseOut)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)) -> Course:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    return course


@router.put("/courses/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course_update: CourseUpdate, db: AsyncSession = Depends(get_db)) -> Course:
    result = await db.execute(select(Course).where(Course.id == course_id))
    existing_course = result.scalar_one_or_none()
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_update.course_title is not None:
        existing_course.course_title = course_update.course_title

    if course_update.course_description is not None:
        existing_course.course_description = course_update.course_description

    if course_update.status is not None:
        existing_course.status = course_update.status

    await db.commit()
    await db.refresh(existing_course)
    return existing_course


@router.delete("/courses/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    await db.delete(course)
    await db.commit()

    return {"message": f"Course with id {course_id} deleted successfully."}


# API key check function
async def verify_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )


@router.post("/generate_summary/{course_id}", response_model=CourseOut, dependencies=[Depends(verify_api_key)])
async def generate_summary_endpoint(course_id: int, db: AsyncSession = Depends(get_db)) -> Course:
    # 1. Get course
    result = await db.execute(select(Course).where(Course.id == course_id))
    existing_course: Course = result.scalar_one_or_none()

    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found.")

    if existing_course.ai_summary:
        return existing_course

    user_id = existing_course.user_id

    # 2. Calculate rate-limit window (last 1 hour)
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)

    # 3. Count AI summaries generated in the last hour
    result = await db.execute(
        select(func.count()).select_from(Course).where(
            and_(
                Course.user_id == user_id,
                Course.ai_summary.isnot(None),
                Course.created_at >= one_hour_ago
            )
        )
    )

    summary_count = result.scalar_one()  # Get count value

    if summary_count >= 3:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: You can only generate 3 summaries per hour."
        )

    # 4. Generate AI summary
    course_ai_summary = await generate_summary(existing_course.course_description)

    # 5. Update course
    existing_course.ai_summary = course_ai_summary
    existing_course.status = "completed"

    await db.commit()
    await db.refresh(existing_course)

    return existing_course


async def generate_summary(description: str, model: str = "gpt-4") -> str:
    # models: gpt-4, gpt-3.5-turbo
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes online courses."},
            {"role": "user", "content": f"Summarize this course: {description}"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content


@router.put("/courses/{course_id}/summary", response_model=CourseOut)
async def update_summary(course_id: int, summary_update: SummaryUpdate, db: AsyncSession = Depends(get_db)) -> Course:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    course.ai_summary = summary_update.ai_summary
    course.status = "finalized"  # Optional: mark it as reviewed/final

    await db.commit()
    await db.refresh(course)

    return course
