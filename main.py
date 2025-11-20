import asyncio
import os

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

try:
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
    ODP_APP_TOKEN = os.environ["ODP_APP_TOKEN"]
except Exception as e:
    print(f"Auth error: Details: {e}") 

async def main() -> None:
    print("Hello!")

if __name__ == "__main__":
    asyncio.run(main())
