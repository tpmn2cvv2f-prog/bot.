import os
from telethon import TelegramClient

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

client = TelegramClient("bot_session", api_id, api_hash)

async def main():
    await client.start(bot_token=bot_token)
    print("Bot is running successfully!")

with client:
    client.loop.run_until_complete(main())
