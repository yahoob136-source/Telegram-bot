import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

# ====== APNI DETAILS YAHAN BHARO ======
BOT_TOKEN = "8773000685:AAEA1JZw3XGe6NOaN8oQR_XZRIZWzbPPXZw"
CHANNEL_1 = "https://t.me/dexterheaven"
CHANNEL_2 = "https://t.me/dexter2hub"
PINTEREST_LINK = "https://pin.it/Olbqcx5RI"
ADMIN_ID = 7575318765
# =======================================

current_video = {"file_id": ""}

async def check_subscription(user_id: int, context) -> bool:
    try:
        member1 = await context.bot.get_chat_member(CHANNEL_1, user_id)
        member2 = await context.bot.get_chat_member(CHANNEL_2, user_id)
        allowed = ["member", "administrator", "creator"]
        return member1.status in allowed and member2.status in allowed
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📌 Pinterest Follow Karo", url=PINTEREST_LINK)],
        [InlineKeyboardButton("📢 Channel 1 Join Karo", url=f"https://t.me/{CHANNEL_1.replace('@', '')}")],
        [InlineKeyboardButton("📢 Channel 2 Join Karo", url=f"https://t.me/{CHANNEL_2.replace('@', '')}")],
        [InlineKeyboardButton("🎬 Video Dekho", callback_data="get_video")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "🎬 Video dekhne ke liye:\n"
        "1️⃣ Pinterest follow karo\n"
        "2️⃣ Dono channels join karo\n"
        "3️⃣ Video Dekho button dabao\n\n"
        "⚠️ Dono channels join karne ke baad hi video milegi!",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "get_video":
        user_id = query.from_user.id
        is_subscribed = await check_subscription(user_id, context)
        if is_subscribed:
            if current_video["file_id"]:
                await query.message.reply_video(
                    video=current_video["file_id"],
                    caption="🎬 Enjoy karo! 🔥"
                )
            else:
                await query.message.reply_text("⚠️ Abhi koi video nahi hai!")
        else:
            keyboard = [
                [InlineKeyboardButton("📌 Pinterest Follow Karo", url=PINTEREST_LINK)],
                [InlineKeyboardButton("📢 Channel 1 Join Karo", url=f"https://t.me/{CHANNEL_1.replace('@', '')}")],
                [InlineKeyboardButton("📢 Channel 2 Join Karo", url=f"https://t.me/{CHANNEL_2.replace('@', '')}")],
                [InlineKeyboardButton("✅ Maine Join Kar Liya!", callback_data="get_video")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "❌ Pehle dono channels join karo!\n\n"
                "Join karne ke baad dobara try karo 👇",
                reply_markup=reply_markup
            )

async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        current_video["file_id"] = update.message.video.file_id
        await update.message.reply_text("✅ Nayi video set ho gayi! 🎬")
    else:
        await update.message.reply_text("❌ Permission nahi hai!")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO, receive_video))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
