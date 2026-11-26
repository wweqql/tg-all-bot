import asyncio, json, os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")
FILE = "members.json"
bot = Bot(TOKEN)
dp = Dispatcher()

def load():
    return json.load(open(FILE)) if os.path.exists(FILE) else {}

def save(d):
    json.dump(d, open(FILE, "w"))

@dp.message(Command("join"))
async def join(m: Message):
    d = load()
    d[str(m.from_user.id)] = m.from_user.full_name
    save(d)
    await m.reply("Добавил!")

@dp.message(Command("all"))
@dp.message(F.text.lower().startswith("@all"))
async def all_(m: Message):
    d = load()
    text = " ".join(
        f'<a href="tg://user?id={uid}">{name}</a>' for uid, name in d.items()
    )
    await m.answer(text or "Список пуст", parse_mode="HTML")

asyncio.run(dp.start_polling(bot))
