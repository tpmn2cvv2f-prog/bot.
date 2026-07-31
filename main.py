import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events

# --- سيرفر وهمي لتلبية شرط Render للبورتات ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_web_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# بدء السيرفر الوهمي في خيط منفصل (Background Thread)
threading.Thread(target=run_web_server, daemon=True).start()

# --- إعدادات بوت تيليجرام ---
API_ID = int(os.getenv("API_ID", "30172280"))
API_HASH = os.getenv("API_HASH", "73840f7b0c5ae24eda44b42e6baf0a38")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8755414330:AAFL8-4XWATAK2JqZOjMGeFgXogKgTW4-lw")

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    await event.respond("أهلاً بك! البوت يعمل الآن بنجاح على رندر 🚀")

print("البوت والسيرفر الوهمي يعملان الآن...")
client.run_until_disconnected()
.
بنجاح!**")
