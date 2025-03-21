import asyncio
import aiogram
from aiogram.filters.command import Command

bot = aiogram.Bot(token="7222583888:AAE0LBk6xr65VXGBL75UFJJIeXY583jx8ug")
dp = aiogram.Dispatcher()

types_maraphone = ["традиционный", "сверхмарафон", "многодневный пробег"]
idToName = {}   
nameToList = {}

@dp.message(Command("start"))
async def cmd_start(message: aiogram.types.Message):
    await message.answer("Это чат-бот для записи на марафон.\nУкажите свои ФИО и тип забега в формате <Фамилия имя отчество - тип забега>")

@dp.message(Command("types"))
async def cmd_get(message: aiogram.types.Message):
    answer = "Доступные варианты марафона:\n"
    for s in types_maraphone:
        answer += s + "\n"
    await message.answer(answer)

@dp.message(Command("get"))
async def cmd_get(message: aiogram.types.Message):
    user_id = str(message.chat.id)
    if user_id in idToName:
        name = idToName[user_id]
        if name in nameToList:
            await message.answer(f"Вы {name}\nВы записаны на:\n{nameToList[name]}")
        else:
            await message.answer("Вы не записаны ни на один из марафонов!")
    else:
        await message.answer("Вы не записаны ни на один из марафонов!")

@dp.message()
async def message_get(message: aiogram.types.Message):
    try:
        parse = message.text.split("-")
        if len(parse) != 2:
            raise ValueError("Неправильный формат ввода")
        
        name = parse[0].strip()
        marathon_type = parse[1].strip().lower()
        
        if marathon_type not in types_maraphone:
            await message.answer("Неподдерживаемый тип забега!")
            return
        
        user_id = str(message.chat.id)
        idToName[user_id] = name
        nameToList[name] = marathon_type
        
        await message.answer("Вы записаны успешно!")
    except Exception as e:
        await message.answer("Неподдерживаемый формат записи")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())