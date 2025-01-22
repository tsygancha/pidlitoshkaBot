from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json

# Токен вашого бота
BOT_TOKEN = '8198273247:AAGyYo_-JCosp2lNJzU-OKq79um155zBR-k'

# Шлях до бази даних
DATABASE_PATH = 'birthdays.json'

# Завантаження бази даних
def load_birthdays():
    try:
        with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Збереження бази даних
def save_birthdays(data):
    with open(DATABASE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Додати іменинника
async def add_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Формат: /addbirthday Ім'я MM-DD @username (тег необов'язковий, без @)")
        return
    
    name = args[0]
    birth_date = args[1]
    username = args[2] if len(args) > 2 else ""

    birthdays = load_birthdays()
    birthdays.append({"name": name, "birth_date": birth_date, "username": username})
    save_birthdays(birthdays)

    await update.message.reply_text(f"Додано: {name} ({birth_date})")

# Видалити іменинника
async def remove_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Формат: /removebirthday Ім'я")
        return

    name = args[0]
    birthdays = load_birthdays()
    updated_birthdays = [person for person in birthdays if person['name'] != name]

    if len(birthdays) == len(updated_birthdays):
        await update.message.reply_text(f"Імені {name} не знайдено.")
    else:
        save_birthdays(updated_birthdays)
        await update.message.reply_text(f"{name} видалено з бази.")

# Список іменинників
async def list_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birthdays = load_birthdays()
    if not birthdays:
        await update.message.reply_text("Список порожній.")
        return

    response = "Список іменинників:\n"
    for person in birthdays:
        username = f" (@{person['username']})" if person['username'] else ""
        response += f"- {person['name']} ({person['birth_date']}){username}\n"

    await update.message.reply_text(response)

# Головна функція
def main():
    # Створення додатку
    application = Application.builder().token(BOT_TOKEN).build()

    # Додавання обробників команд
    application.add_handler(CommandHandler("addbirthday", add_birthday))
    application.add_handler(CommandHandler("removebirthday", remove_birthday))
    application.add_handler(CommandHandler("listbirthdays", list_birthdays))

    # Запуск бота
    print("Бот запущено. Використовуйте команди для керування списком.")
    application.run_polling()

if __name__ == "__main__":
    main()