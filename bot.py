from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

TOKEN = "8408634586:AAEW-jBJSlEFL8bKVo9XZK8RuAzFMzulsWc"
CHANNEL_LINK = "https://t.me/+a163cq-juqRjMzMy"


# ---------- HANDLERS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name

    text = (
        f"{first_name}, добро пожаловать в SMI 👋\n\n"
        "Переходите в закрытый канал вебинара\n"
        "«Инструменты инвестиций в 2026 году» 👇"
    )

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎁 ПЕРЕЙТИ В КАНАЛ", url=CHANNEL_LINK)]]
    )

    with open("webinar.jpg", "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )


# ---------- ЗАПУСК ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
