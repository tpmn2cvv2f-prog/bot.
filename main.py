import os
from telethon import TelegramClient

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
phone = os.environ.get("TG_PHONE")

# تمرير الجوال للـ client يمنعه من طلب input()
client = TelegramClient("session_name", api_id, api_hash)


async def main():
  await client.start(phone=phone)
  print("Bot is running successfully!")


with client:
  client.loop.run_until_complete(main())
