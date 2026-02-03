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
        f"{name}, поздравляю! 🎉\n\n"
        "Вы успешно зарегистрированы на вебинар\n"
        "10 февраля в 19:00\n"
        "«Инструменты инвестиций в 2026 году»\n"
        "Фондовые рынки и как на них зарабатывать в России и США\n\n"
        "📍На эфире вас ждёт:\n"
        "— обзор российского и американского инвестиционных рынков\n"
        "— роль и ситуация с рублем в 2026 году\n"
        "— что происходит с процентной ставкой в США\n"
        "— разбор конкретных акций и причин их роста\n"
        "— и приятный бонус, который раскроем уже в эфире 😉\n\n"
        "Переходите в закрытый канал вебинара —\n"
        "там мы будем делиться всеми новостями и именно туда пришлём ссылку на эфир 👇"
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
