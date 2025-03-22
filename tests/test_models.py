# Author: Manzoor Hussain

import asyncio
from database import AsyncSessionLocal
from models import User


async def test_user_insert() -> None:
    async with AsyncSessionLocal() as session:
        user = User(name="Test User", email="test@example.com")
        session.add(user)
        await session.commit()
        print("✅ Test user added.")


if __name__ == "__main__":
    asyncio.run(test_user_insert())
