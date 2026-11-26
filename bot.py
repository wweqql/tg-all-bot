import asyncio, json, os, html
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")
FILE = "members.json"
TRIGGERS = {"@all", "@все", "!all", "!все"}

bot = Bot(TOKEN)
dp = Dispatcher()

def load():
    return json.load(open(FILE)) if os.path.exists(FILE) else {}

def save(d):
    json.dump(d, open(FILE, "w"))

def remember(m: Message):
    u = m.from_user
    if u and not u.is_bot:
        d = load()
        if d.get(str(u.id)) != u.full_name:
            d[str(u.id)] = u.full_name
            save(d)

async def mention_all(m: Message, extra: str = ""):
    d = load()
    hidden = "".join(
        f'<a href="tg://user?id={uid}">\u200b</a>' for uid in d
    )
    text = html.escape(extra) if extra else "📢 Все сюда!"
    await m.answer(text + hidden, parse_mode="HTML")

@dp.message(Command("join"))
async def join(m: Message):
    remember(m)
    await m.reply("Добавил!")

@dp.message(Command("all"))
async def all_cmd(m: Message):
    remember(m)
    extra = (m.text or "").partition(" ")[2]
    await mention_all(m, extra)

@dp.message(F.text)
async def any_text(m: Message):
    remember(m)
    first, _, rest = m.text.partition(" ")
    if first.lower() in TRIGGERS:
        await mention_all(m, rest)

asyncio.run(dp.start_polling(bot))
