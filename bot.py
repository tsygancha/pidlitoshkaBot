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
    "🎉 З днем народження, {name}! Нехай Бог завжди буде поруч і направляє твої кроки!",
    "🌟 {name}, вітаю зі святом! Бажаю тобі Божого благословення, радості та миру в серці.",
    "🎂 З днем народження, {name}! Нехай у твоєму житті буде більше світла, добра і тепла!",
    "🎈 {name}, вітаю з днем народження! Нехай Господь дарує тобі сили й натхнення для всіх звершень.",
    "✨ З днем народження, {name}! Молюся, щоб у твоєму житті завжди було місце для щастя та віри.",
    "🎁 {name}, зі святом! Нехай Божа любов буде твоїм компасом у житті, а серце сповниться вдячністю.",
    "🥳 З днем народження, {name}! Бажаю гармонії, теплих стосунків і Божого захисту в усьому!",
    "🌟 {name}, вітаємо з днем народження! Нехай усі твої мрії здійснюються, а життя буде наповнене благословеннями!",
    "🎉 Зі святом, {name}! Бажаю тобі світлих днів, добрих друзів і натхнення, що приходить згори.",
    "🎂 {name}, з днем народження! Радості, миру й достатку тобі, а ще багато теплих моментів з близькими.",
    "✨ З днем народження, {name}! Нехай твоє серце завжди радіє, а дорога веде до добра.",
    "🎁 {name}, вітаю тебе зі святом! Нехай твоє життя буде яскравим прикладом добра і любові.",
    "🎈 З днем народження, {name}! Бажаю здоров'я, радості та впевненості, що всі твої мрії здійсняться.",
    "🌟 {name}, вітаємо з днем народження! Нехай кожен день твого життя буде благословенним і наповненим щастям.",
    "🎉 Зі святом, {name}! Пам'ятай, що ти унікальний/а і створений/а для великих справ. Нехай Бог допомагає тобі на цьому шляху."
    "🎉 З днем народження, {name}! Нехай твоє життя буде наповнене світлом, щастям і добром!",
    "🌟 {name}, зі святом! Нехай Господь благословляє твої починання та веде до найкращого.",
    "🎂 Вітаю тебе, {name}! Нехай кожен день приносить радість, а серце буде спокійним і щасливим.",
    "🎈 З днем народження, {name}! Нехай любов і тепло завжди оточують тебе, а мрії здійснюються.",
    "✨ {name}, вітаємо зі святом! Нехай твоє життя буде повним нових можливостей і Божої підтримки.",
    "🎁 З днем народження, {name}! Бажаю тобі бути сміливим/ою, добрим/ою та наповненим/ою любов’ю.",
    "🥳 {name}, вітаємо зі святом! Нехай кожен день нагадує тобі, що ти унікальний/а і важливий/а.",
    "🌟 З днем народження, {name}! Нехай твої мрії здійснюються, а в душі завжди буде радість.",
    "🎉 {name}, зі святом! Бажаю тобі натхнення, добрих друзів і Божого проводу на кожному кроці.",
    "🎂 Вітаю тебе, {name}! Нехай життя буде яскравим, а серце наповнене вірою в себе.",
    "✨ З днем народження, {name}! Нехай у твоєму житті буде багато тепла, добрих людей і благословінь.",
    "🎁 {name}, з днем народження! Нехай твої старання приносять радість, а серце сповнюється вдячністю.",
    "🎈 Зі святом, {name}! Нехай кожен день нагадує про те, як багато ти значиш для цього світу.",
    "🌟 {name}, вітаємо з днем народження! Радості, здоров’я і натхнення тобі на кожен день!",
    "🎉 З днем народження, {name}! Нехай у твоєму серці завжди буде місце для добра та радості!"
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
schedule.every().day.at("8:00").do(job)

# Постійна робота програми
if __name__ == "__main__":
    print("Бот запущено. Очікування запланованого часу...")
    while True:
        schedule.run_pending()
        time.sleep(60)
