import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# ضع بيانات حسابك هنا أو في متغيرات البيئة (Render Environment Variables)
API_ID = 1234567  # استبدل برقم الـ API ID الخاص بك
API_HASH = "your_api_hash"  # استبدل برقم الـ API HASH الخاص بك

app = Client("tastar_session", api_id=API_ID, api_hash=API_HASH)

# متغيرات مؤقتة للتحكم في الجلسة والتحكم بالايقاف
user_sessions = {}

# قائمة خيارات السرعة (بالثواني)
SPEEDS = {
    "⚡ سريع جداً (0.5 ثانية)": 0.5,
    "🔥 متوسط (1.5 ثانية)": 1.5,
    "🐢 هادئ (3 ثواني)": 3.0
}

@app.on_message(filters.command("تستر", prefixes=".") & filters.me)
async def start_tastar(client: Client, message: Message):
    chat_id = message.chat.id
    
    # 1. طلب السطور
    await message.edit("⚡ **أهلاً بك يا غالي في نظام التستر المطور.**\n\nأرسل الآن **الأسطر** التي تريد إرسالها (أي عدد تريده، ضعها في رسالة واحدة):")
    
    try:
        lines_msg = await client.listen(chat_id, timeout=120)
        lines_text = lines_msg.text
        if not lines_text:
            await message.reply("❌ لم ترسل أسطراً صحيحة. تم إلغاء العملية.")
            return
    except asyncio.TimeoutError:
        await message.reply("⏰ انتهى الوقت ولم تقم بإرسال الأسطر.")
        return

    # 2. سؤال عن طريقة العرض (سطر أو سطرين)
    row_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 سطر واحد لكل رسالة", callback_data="split_1")],
        [InlineKeyboardButton("📜 سطرين لكل رسالة", callback_data="split_2")]
    ])
    prompt_split = await message.reply("كيف تريد أن تنزل الأسطر؟ اختر الطريقة:", reply_markup=row_kb)
    
    # انتظار اختيار المستخدم للتقسيم
    try:
        split_press = await client.listen(chat_id, timeout=60)
        await split_press.delete()
        await prompt_split.delete()
        
        # تحديد عدد الأسطر بناءً على الضغطة أو النص إذا فضلنا أزرار تفاعلية بسيطة
        # للتسهيل، سنعتمد على النص أو زر (نأخذ القيمة مباشرة)
        lines_per_msg = 2 if "سطرين" in split_press.text or "2" in split_press.text else 1
    except:
        # افتراضي إذا حصل تأخير
        lines_per_msg = 1

    # 3. سؤال عن يوزر الشخص المستهدف
    prompt_target = await message.reply("👤 **أرسل الآن يوزر الشخص (أو المعرف/الرابط)** الذي تريد إرسال السطور عليه (مثلاً: `@username`):")
    try:
        target_msg = await client.listen(chat_id, timeout=60)
        target_user = target_msg.text.strip()
    except asyncio.TimeoutError:
        await message.reply("⏰ انتهى الوقت.")
        return

    # 4. سؤال عن سرعة النزول
    speed_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(name, callback_data=str(delay))] for name, delay in SPEEDS.items()
    ])
    prompt_speed = await message.reply("⚙️ **اختر سرعة نزول السطور:**", reply_markup=speed_kb)
    
    # استقبال اختيار السرعة
    try:
        speed_msg = await client.listen(chat_id, timeout=60)
        # مطابقة الاختيار
        selected_speed = 1.5 # افتراضي
        for name, delay in SPEEDS.items():
            if name in speed_msg.text:
                selected_speed = delay
                break
        await speed_msg.delete()
        await prompt_speed.delete()
    except:
        selected_speed = 1.5

    # تجهيز الأسطر وتقسيمها
    raw_lines = lines_text.split("\n")
    cleaned_lines = [l.strip() for l in raw_lines if l.strip()]
    
    grouped_lines = []
    for i in range(0, len(cleaned_lines), lines_per_msg):
        group = "\n".join(cleaned_lines[i:i + lines_per_msg])
        grouped_lines.append(group)

    # 5. رسالة الجاهزية مع زر الإيقاف
    stop_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🛑 إيقاف التسطير", callback_data="stop_tastar")]])
    
    ready_msg = await message.reply(
        f"🚀 **جاهز للبث والتسطير!**\n\n"
        f"• عدد الأسطر الإجمالي: `{len(cleaned_lines)}`\n"
        f"• المستهدف: `{target_user}`\n"
        f"• السرعة: `{selected_speed} ثانية`\n\n"
        f"جاري بدء التسطير الآن...",
        reply_markup=stop_btn
    )
    
    # حفظ حالة التشغيل للتحكم بالإيقاف
    user_sessions[chat_id] = True

    # البدء بالإرسال مع خاصية "يكتب الآن..." (typing)
    try:
        for group in grouped_lines:
            if not user_sessions.get(chat_id, False):
                break # تم إيقاف العملية
            
            # إظهار حالة الكتابة لتبدو طبيعية كأنك تكتب يدويًا
            async with client.action(target_user, "typing"):
                await asyncio.sleep(0.8) # وقت قصير لمحاكاة الكتابة الحقيقية
                
            # إرسال السطر/السطرين
            await client.send_message(target_user, group)
            
            # الانتظار حسب السرعة المحددة
            await asyncio.sleep(selected_speed)
            
        await ready_msg.edit("✅ **تم الانتهاء من التسطير بنجاح وفخامة!** ✨")
    except Exception as e:
        await ready_msg.edit(f"❌ حدث خطأ أثناء الإرسال: `{e}`")
    finally:
        if chat_id in user_sessions:
            del user_sessions[chat_id]

# زر الإيقاف
@app.on_callback_query(filters.regex("stop_tastar"))
async def stop_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id in user_sessions:
        user_sessions[chat_id] = False
        await callback_query.message.edit("🛑 **تم إيقاف التسطير بناءً على رغبتك.**")
    else:
        await callback_query.answer("لا توجد عملية نشطة حالياً.", show_alert=True)

app.run()
