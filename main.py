import os
os.system('pip install pyrogram tgcrypto')

import asyncio
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "24956321"))
API_HASH = os.environ.get("API_HASH", "your_api_hash")

app = Client(
    "tastar_bot",
    api_id=API_ID,
    api_hash=API_HASH
)

@app.on_message(filters.command("تستر", prefixes="."))
async def tastar_cmd(client, message):
    await message.reply("⚡ **تم تفعيل نظام التستر بنجاح!**\n\nالقائمة جاهزة والتحكم كامل معك يا غالي.")

async def main():
    await app.start()
    print("Bot is running successfully!")
    await asyncio.gather(*(asyncio.Event().wait() for _ in range(1)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
