import asyncio
import os

from dotenv import load_dotenv


# Load environment variables from .env
try:
    load_dotenv()
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
except Exception as e:
    print(f"Auth error: Details: {e}") 

async def main() -> None:
    print("Hello!")

if __name__ == "__main__":
    asyncio.run(main())
