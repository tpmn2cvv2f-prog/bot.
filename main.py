import os
from telethon import TelegramClient, events

# جلب المتغيرات البيئية من رندر
API_ID = int(os.getenv("API_ID", "30172280"))
API_HASH = os.getenv("API_HASH", "73840f7b0c5ae24eda44b42e6baf0a38")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8755414330:AAFL8-4XWATAK2JqZOjMGeFgXogKgTW4-lw")

# تهيئة العميل باستخدام توكن البوت حصرياً لتجنب طلبات التيرمنال
client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    await event.respond("أهلاً بك! البوت يعمل الآن بنجاح على رندر 🚀")

print("البوت يعمل الآن ويستمع للأحداث...")
client.run_until_disconnected()
