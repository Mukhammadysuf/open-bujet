import os
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# === Токен берём из переменной окружения (Render → Environment Variables) ===
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 1000765175

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# States
PHONE, CODE, ADMIN_MESSAGE = range(3)

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.setdefault(user_id, {"balance": 0})
    menu = [["Ovoz Berish✅"], ["Balans⚡"], ["Isbotlar"], ["Admin bilan bog'lanish"]]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text("Assalomu alaykum! Kerakli bo‘limni tanlang:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "Ovoz Berish✅":
        await update.message.reply_text("Iltimos, telefon raqamingizni kiriting:")
        return PHONE
    elif text == "Balans⚡":
        balance = users.get(user_id, {}).get("balance", 0)
        await update.message.reply_text(f"Sizning balansingiz: {balance} so'm")
    elif text == "Isbotlar":
        await update.message.reply_text("Isbotlar kanali: https://t.me/s/your_channel")
    elif text == "Admin bilan bog'lanish":
        await update.message.reply_text("Admin uchun xabaringizni yuboring:")
        return ADMIN_MESSAGE

    return ConversationHandler.END

async def phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kod yuborildi. Iltimos, tasdiqlash kodini kiriting:")
    return CODE

async def code_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id]["balance"] += 50000
    await update.message.reply_text("Ovoz tasdiqlandi. Balansga 50,000 so‘m qo‘shildi!")
    return ConversationHandler.END

async def admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"Foydalanuvchidan xabar:\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await update.message.reply_text("Xabaringiz adminga yuborildi.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_input)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, code_input)],
            ADMIN_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_message)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
