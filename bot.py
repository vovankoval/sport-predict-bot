from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import requests

# Ключи — твой ключ уже работает!
API_TOKEN = '8075939198:AAEogNTrAsxOevk6Fanj04imVysNO23Ul5M'
GROQ_KEY = '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'  # Твой свежий ключ

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Привет! 🎉 Я ИИ-бот для прогнозов на спорт.\n/predict — свежие реалистичные прогнозы на футбол (и скоро киберспорт) от мощного ИИ!")

@dp.message(Command("predict"))
async def predict(message: types.Message):
    await message.reply("🤖 Генерирую прогнозы от ИИ... 10-20 секунд.")

    prompt = """Ты эксперт по ставкам на футбол с отличной статистикой. Сегодня 31 декабря 2025 года — новогодняя ночь, основных матчей мало (в основном товарищеские или молодёжные).
Дай 5 реалистичных прогнозов на ближайшие футбольные матчи (используй реальные команды из топ-лиг: АПЛ, Ла Лига, Серия A, Бундеслига и т.д., или клубные товарищеские).
Для каждого прогноза укажи:
- Матч (команды)
- Прогноз (победа одной команды, ничья, точный счёт или тотал голов)
- Примерный коэффициент (реалистичный)
- Краткое обоснование (текущая форма команд, статистика голов, история встреч, травмы если известны)
Сделай прогнозы разнообразными, с плюсами и минусами, чтобы было интересно."""

    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",  # Новая мощная модель 2025 года!
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.8
    }
    headers_g = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(groq_url, json=payload, headers=headers_g, timeout=30)
        if response.status_code != 200:
            await message.reply(f"Ошибка Groq: {response.status_code} {response.text}")
            return
        ai_resp = response.json()
        prediction = ai_resp['choices'][0]['message']['content']
    except Exception as e:
        await message.reply(f"Ошибка связи: {str(e)}")
        return

    await message.reply(f"🤖 Прогнозы от ИИ (Llama 3.3) на ближайшие матчи:\n\n{prediction}\n\n⚠️ Это развлечение! Ставки — на свой риск, ничего не гарантирую.")

@dp.message()
async def echo(message: types.Message):
    await message.answer("Напиши /predict для свежих прогнозов!")

async def main():
    print("Бот запущен! Используем новую модель Llama 3.3")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())