import os
from telethon import TelegramClient

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

client = TelegramClient("session_name", API_ID, API_HASH)

async def main():
    print("Bot is running!")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
        
