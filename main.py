# Author: Manzoor Hussain

from fastapi import FastAPI
from routes.users import router as users_router
from routes.courses import router as courses_router

app = FastAPI()

# Register the router
app.include_router(users_router)
app.include_router(courses_router)
