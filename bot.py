import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("7820128112:AAEaSlH0hA5kb_toUQ8AXHwtrRqKfekmaEI")
GOOGLE_API_KEY = os.getenv("AIzaSyDbat83D0k6RWPttcW_XT2-SbTGrjVCyhA")

def get_coordinates(address):
    res = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': address, 'key': GOOGLE_API_KEY}).json()
    if res['results']:
        loc = res['results'][0]['geometry']['location']
        return f"{loc['lat']},{loc['lng']}"
    return None

def get_nearby(location, place_type):
    res = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params={'location': location, 'radius': 5000, 'type': place_type, 'key': GOOGLE_API_KEY}).json()
    return [f"{p['name']}\n📍 {p.get('vicinity','Unknown')}\n⭐ {p.get('rating','N/A')}" for p in res.get('results', [])[:3]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a location to find nearby:\n🛡️ Police\n🚒 Fire Station\n🏥 Hospitals")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    loc = get_coordinates(text)
    if not loc:
        await update.message.reply_text("❌ Couldn't find that location.")
        return
    police = get_nearby(loc, 'police')
    fire = get_nearby(loc, 'fire_station')
    hospital = get_nearby(loc, 'hospital')
    resp = "🛡️ *Police Stations*\n" + "\n\n".join(police) + "\n\n🚒 *Fire Stations*\n" + "\n\n".join(fire) + "\n\n🏥 *Hospitals*\n" + "\n\n".join(hospital)
    await update.message.reply_text(resp, parse_mode="Markdown")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
