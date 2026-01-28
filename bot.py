from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re

TOKEN = "YOUR_BOT_TOKEN"

# Хранилище состояний пользователей
user_state = {}
user_data = {}   # user_id -> {"name":..., "phone":..., "email":...}

# Файл для сохранения заявок
DATA_FILE = "registrations.txt"

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


# --- Клавиатура запроса контакта ---
def contact_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📲 Отправить имя и телефон", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=False
    )


# --- Кнопка перехода в канал ---
def channel_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎁 ЗАБРАТЬ ПОДАРОК", url="https://t.me/+a163cq-juqRjMzMy")]]
    )


# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name

    text = (
        f"{first_name}, добро пожаловать в бот SMI 👋\n\n"
        "Он поможет вам зарегистрироваться на вебинар\n"
        "«Инструменты инвестиций в 2026 году» и получить подарок 🎁\n\n"
        "Чтобы завершить регистрацию, нажмите кнопку ниже 👇"
    )

    await update.message.reply_text(text, reply_markup=contact_keyboard())
    user_state[update.effective_user.id] = "WAIT_CONTACT"


# --- Получение контакта ---
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_state.get(user_id) != "WAIT_CONTACT":
        await update.message.reply_text(
            "Регистрация уже пройдена ✅",
            reply_markup=channel_keyboard()
        )
        return

    contact = update.message.contact
    name = contact.first_name
    phone = contact.phone_number

    # сохраняем временно
    user_data[user_id] = {"name": name, "phone": phone}

    await update.message.reply_text(
        "Отлично! Теперь введите ваш email 📧"
    )

    user_state[user_id] = "WAIT_EMAIL"


# --- Получение email ---
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_state.get(user_id) != "WAIT_EMAIL":
        return

    if not EMAIL_REGEX.match(text):
        await update.message.reply_text("❌ Неверный email. Попробуйте ещё раз:")
        return

    # сохраняем email
    user_data[user_id]["email"] = text

    name = user_data[user_id]["name"]
    phone = user_data[user_id]["phone"]
    email = user_data[user_id]["email"]

    # Записываем всё в файл
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name} | {phone} | {email}\n")

    # Финальное сообщение
    text_msg = (
        f"{name}, поздравляю! 🎉\n\n"
        "Вы успешно зарегистрированы на вебинар\n"
        "10 февраля в 19:00\n"
        "«Инструменты инвестиций в 2026 году»\n\n"
        "Переходите в закрытый канал вебинара —\n"
        "там будет ссылка на эфир 👇"
    )

    await update.message.reply_text(text_msg, reply_markup=channel_keyboard())

    user_state[user_id] = "DONE"


# --- Обработка любого текста ---
async def fallback_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_state.get(user_id) == "WAIT_CONTACT":
        await update.message.reply_text(
            "Пожалуйста, нажмите кнопку для отправки имени и телефона 👇",
            reply_markup=contact_keyboard()
        )
        return

    if user_state.get(user_id) == "WAIT_EMAIL":
        await handle_email(update, context)
        return

    if user_state.get(user_id) == "DONE":
        await update.message.reply_text(
            "Вы уже зарегистрированы ✅\nПереходите в канал 👇",
            reply_markup=channel_keyboard()
        )
        return

    await update.message.reply_text(
        "Нажмите /start для начала регистрации",
        reply_markup=contact_keyboard()
    )


# --- Запуск ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_text))

    app.run_polling()


if __name__ == "__main__":
    main()
