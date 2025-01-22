from telegram import Bot
from datetime import datetime
import random
import json
import schedule
import time
import asyncio

# Токен вашого бота
BOT_TOKEN = '8198273247:AAGyYo_-JCosp2lNJzU-OKq79um155zBR-k'
CHAT_ID = '-4690038303'

# Шлях до бази даних
DATABASE_PATH = 'birthdays.json'

# Список привітань
greetings = [
    "🎉 З днем народження, {name}! Бажаємо щастя та здоров'я!",
    "🌟 Вітаємо, {name}! Нехай кожен день буде сповнений радістю!",
    "🎂 Зі святом, {name}! Успіхів у всіх починаннях!"
]

# Завантаження даних із бази
def load_birthdays():
    with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функція перевірки днів народження
async def check_and_send_birthdays():
    today = datetime.now().strftime("%m-%d")
    bot = Bot(token=BOT_TOKEN)
    birthdays = load_birthdays()

    for person in birthdays:
        if person['birth_date'] == today:
            # Вибір рандомного привітання
            name = f"@{person['username']}" if person['username'] else person['name']
            message = random.choice(greetings).format(name=name)
            # Відправка привітання
            await bot.send_message(chat_id=CHAT_ID, text=message)
            print(f"Відправлено привітання для {name}")

# Запуск завдання
def job():
    asyncio.run(check_and_send_birthdays())

# Заплануйте запуск щодня о 8:00
schedule.every().day.at("17:46").do(job)

# Постійна робота програми
if __name__ == "__main__":
    print("Бот запущено. Очікування запланованого часу...")
    while True:
        schedule.run_pending()
        time.sleep(60)
