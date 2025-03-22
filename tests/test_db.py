# Author: Manzoor Hussain

import asyncio
import sys
from database import engine


async def test_connection() -> None:
    try:
        async with engine.begin() as conn:
            print("✅ Successfully connected to the PostgreSQL database.")
    except Exception as e:
        print("❌ Connection failed:", e)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_connection())
