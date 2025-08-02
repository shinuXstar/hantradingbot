from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os, json
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

USER_FILE = "user_data.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /register <API_KEY> <SECRET> to start copying trades.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, api_key, api_secret = update.message.text.strip().split()
        user = {
            "user_id": update.effective_user.id,
            "api_key": api_key,
            "api_secret": api_secret,
            "multiplier": 1.0,
            "max_trades": 10,
            "max_volume": 100.0,
            "daily_trades": 0,
            "daily_volume": 0.0
        }
        users = load_users()
        if any(u["user_id"] == user["user_id"] for u in users):
            await update.message.reply_text("You're already registered.")
        else:
            users.append(user)
            save_users(users)
            await update.message.reply_text("Registered for copy trading!")
    except:
        await update.message.reply_text("Usage: /register <API_KEY> <SECRET>")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    for u in users:
        if u["user_id"] == update.effective_user.id:
            msg = (
                "Registered\n"
                f"Multiplier: {u.get('multiplier', 1.0)}\n"
                f"Max Trades/Day: {u.get('max_trades', 10)}\n"
                f"Max Volume/Day: {u.get('max_volume', 100.0)}\n"
                f"Today's Trades: {u.get('daily_trades', 0)}\n"
                f"Today's Volume: {u.get('daily_volume', 0.0)}\n"
            )
            await update.message.reply_text(msg)
            return
    await update.message.reply_text("You are not registered.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    users = [u for u in users if u["user_id"] != update.effective_user.id]
    save_users(users)
    await update.message.reply_text("You have been unregistered.")

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    users = load_users()
    user_id = update.effective_user.id
    user = next((u for u in users if u["user_id"] == user_id), None)
    if not user:
        await update.message.reply_text("You are not registered.")
        return

    try:
        for i in range(0, len(args), 2):
            key, val = args[i], args[i+1]
            if key in ["multiplier", "max_trades", "max_volume"]:
                user[key] = float(val)
        save_users(users)
        await update.message.reply_text("Risk settings updated.")
    except:
        await update.message.reply_text("Usage: /risk multiplier 2 max_trades 5 max_volume 100")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("register", register))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("risk", risk))
app.run_polling()
