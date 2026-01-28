from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8408634586:AAFC1aIugJxY3jdI1rgYUcTPXU1gozSj5pw"   # вставь новый токен

user_state = {}
user_data_temp = {}   # временно храним имя и телефон

DATA_FILE = "registrations.txt"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name

    text = (
        f"{first_name}, добро пожаловать в бот SMI 👋\n\n"
        "Он поможет вам зарегистрироваться на вебинар\n"
        "«Инструменты инвестиций в 2026 году» и получить подарок 🎁\n\n"
        "Чтобы завершить регистрацию, оставьте ваш номер телефона и почту по кнопке ниже 👇🏻"
    )

    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📲 Отправить имя и телефон", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(text, reply_markup=keyboard)
    user_state[update.effective_user.id] = "WAIT_CONTACT"


# ===== Получаем контакт =====
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_state.get(user_id) != "WAIT_CONTACT":
        return

    contact = update.message.contact
    name = contact.first_name
    phone = contact.phone_number

    # сохраняем временно
    user_data_temp[user_id] = {"name": name, "phone": phone}

    await update.message.reply_text(
        "Спасибо! Теперь введите ваш email 📧",
        reply_markup=ReplyKeyboardRemove()
    )

    user_state[user_id] = "WAIT_EMAIL"


# ===== Получаем email =====
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_state.get(user_id) != "WAIT_EMAIL":
        return

    email = update.message.text.strip()

    # простая проверка email
    if "@" not in email or "." not in email:
        await update.message.reply_text("Введите корректный email 📧")
        return

    name = user_data_temp[user_id]["name"]
    phone = user_data_temp[user_id]["phone"]

    # сохраняем в файл
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name} | {phone} | {email}\n")

    await update.message.reply_text("Спасибо! Регистрируем вас...")

    # ===== Сообщение 2: картинка + текст + кнопка =====
    text = (
        f"{name}, поздравляю! 🎉\n\n"
        "Вы успешно зарегистрированы на вебинар\n"
        "10 февраля в 19:00\n"
        "«Инструменты инвестиций в 2026 году»\n\n"
        "📍На эфире вас ждёт:\n"
        "— обзор рынков\n"
        "— инвестиционные идеи\n"
        "— разбор акций\n"
        "— бонус в эфире 😉\n\n"
        "Переходите в закрытый канал вебинара 👇"
    )

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎁 ЗАБРАТЬ ПОДАРОК", url="https://t.me/+a163cq-juqRjMzMy")]]
    )

    with open("webinar.jpg", "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )

    user_state[user_id] = "DONE"
    user_data_temp.pop(user_id, None)


async def fallback_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, следуйте шагам регистрации 🙂")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))
    app.add_handler(MessageHandler(filters.ALL, fallback_text))

    app.run_polling()


if __name__ == "__main__":
    main()
