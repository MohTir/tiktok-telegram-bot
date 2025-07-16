import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("8096546428:AAE1SmXhPx9FMPlBnjd9pUAe_kaUbxAVUmQ")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 أرسل رابط TikTok وسأنزله لك بدون علامة مائية!")

def get_tikmate_download_link(tiktok_url):
    try:
        api_url = f"https://api.tikmate.app/api/lookup?url={tiktok_url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            video_id = data.get("id")
            token = data.get("token")
            if video_id and token:
                download_url = f"https://tikmate.app/download/{video_id}/{token}.mp4"
                return download_url
        return None
    except:
        return None

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "tiktok.com" not in url:
        await update.message.reply_text("⚠️ أرسل رابط تيك توك صالح.")
        return

    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    video_url = get_tikmate_download_link(url)

    if video_url:
        try:
            await update.message.reply_video(video_url)
        except:
            await update.message.reply_text("⚠️ حصل خطأ أثناء الإرسال.")
    else:
        await update.message.reply_text("❌ لم أستطع تحميل الفيديو.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))

app.run_polling()
