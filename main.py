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

import asyncio
import os
from telethon import events

# ملاحظة: تأكد أن client معرف عندك مسبقاً في بداية ملفك (مثل: client = TelegramClient(...))

@client.on(events.NewMessage(outgoing=True, pattern=r'\.بدء_تسطير'))
async def start_tastar_process(event):
    chat = await event.get_chat()
    
    # الخطوة 1: طلب السرعة بين الرسائل
    await event.edit("⚡ **خطوة 1:** كم تبي السرعة بين كل رسالة والثانية؟ (اكتب الرقم بالثواني، مثلاً: `3`):")
    try:
        speed_msg = await client.conversation(chat).wait_event(
            events.NewMessage(from_users=event.sender_id, outgoing=True),
            timeout=30
        )
        delay = float(speed_msg.raw_text.strip())
    except asyncio.TimeoutError:
        return await event.respond("⏳ انتهى الوقت ولم ترد، تم إلغاء العملية.")

    # الخطوة 2: طلب عدد الأسطر في كل رسالة
    await event.edit("📝 **خطوة 2:** كم سطر تبي تنزل في الرسالة الواحدة؟ (مثلاً: `2`):")
    try:
        lines_msg = await client.conversation(chat).wait_event(
            events.NewMessage(from_users=event.sender_id, outgoing=True),
            timeout=30
        )
        lines_count = int(lines_msg.raw_text.strip())
    except asyncio.TimeoutError:
        return await event.respond("⏳ انتهى الوقت ولم ترد، تم إلغاء العملية.")

    # الخطوة 3: طلب يوزر الحساب المستهدف
    await event.edit("🎯 **خطوة 3:** عطني يوزر الحساب المستهدف (مثلاً: `@username`):")
    try:
        target_msg = await client.conversation(chat).wait_event(
            events.NewMessage(from_users=event.sender_id, outgoing=True),
            timeout=30
        )
        target_user = target_msg.raw_text.strip()
    except asyncio.TimeoutError:
        return await event.respond("⏳ انتهى الوقت ولم ترد، تم إلغاء العملية.")

    # قراءة ملف الأسطر
    filename = 'texts.txt'
    if not os.path.exists(filename):
        return await event.respond("❌ يا طويل العمر ما لقيت ملف `texts.txt`، تأكد إنه مرفوع في المستودع!")

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # قراءة الأسطر وتنظيف المسافات الزائدة
            all_lines = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        return await event.respond(f"❌ حدث خطأ أثناء قراءة الملف: {e}")

    if not all_lines:
        return await event.respond("❌ ملف الأسطر فاضي يالذيب!")

    await event.respond(f"🚀 أبشر، جاري بدء التسطير في شات: {target_user}\nالسرعة: {delay} ثانية | عدد الأسطر بالرسالة: {lines_count}")

    # حلقة إرسال الأسطر بالشات المستهدف بالترتيب
    i = 0
    while i < len(all_lines):
        # دمج الأسطر حسب العدد اللي حددته
        chunk = all_lines[i:i + lines_count]
        text_to_send = "\n".join(chunk)
        
        try:
            await client.send_message(target_user, text_to_send)
        except Exception as e:
            await event.respond(f"❌ صار خطأ أثناء الإرسال: {e}")
            break
            
        i += lines_count
        await asyncio.sleep(delay)

    await event.respond("✅ **تم الانتهاء من إرسال جميع الأسطر بنجاح!**")
