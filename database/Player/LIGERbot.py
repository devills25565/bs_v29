import logging
from aiogram import Bot, Dispatcher, executor, types
from DB.DB import DB

bot = Bot("6919193070:AAEl9hBdXzp1zmI6Y0POP9DUbWtciJ781Io")
dp = Dispatcher(bot)

@dp.message_handler(commands="top")
async def top(message: types.Message):
    db = DB()
    data = db.sortPlayers('trophies')
    text = "♿Топ 5 Vokes Brawl (PROD)\n"
    for i in range(5):
    	text += f"{i+1}. {data[i]['name']} | {data[i]['trophies']}🏆\n"
    	
    text += f"\nВсего игроков: {len(data)}"
    	
    await message.reply(text)


if __name__ == "__main__":
    executor.start_polling(dp)