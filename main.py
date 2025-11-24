import asyncio
from aiogram import types, Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery
import random

TOKEN = 'YOUR_TOKEN'
bot = Bot(token=TOKEN)
dp = Dispatcher()

saved_facts = {}

facts = [
    "Пчёлы могут различать человеческие лица.",
    "Осьминоги имеют три сердца и синюю кровь.",  
    "Самая сильная мышца в человеческом теле — язык.",  
    "У жирафа нет голосовых связок.", 
    "Кошки могут издавать более 100 различных звуков.", 
    "Шоколад когда-то использовался как денежная валюта.",  
    "У медуз нет мозга, сердца и костей.",  
    "В Японии есть остров, где живут только кролики.",  
    "Лимоны плавают в воде, а лаймы — тонут.",  
    "Мед — единственный продукт, который не портится тысячелетиями."
]


@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text='Узнать Факт')]
    ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(
        "Здравствуйте! Добро пожаловать в мир фактов.\n"  
        "Нажмите на кнопку 'Узнать Факт', чтобы получить один рандомный факт.", 
        reply_markup=keyboard
    )
    
@dp.message(F.text == 'Узнать Факт')
async def send_fact(message: types.Message):
    random_fact = random.choice(facts)  
    
    buttons = [
        [types.InlineKeyboardButton(text='Сохранить', callback_data='save')], 
        [types.InlineKeyboardButton(text='Ещё факты', callback_data='more')],  
        [types.InlineKeyboardButton(text='Сохранённые факты', callback_data='saved')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(f"📌 {random_fact}", reply_markup=keyboard)
    

@dp.callback_query()    
async def progress(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    
    if callback.data == 'save':
        fact_text = callback.message.text.replace("📌 ", "")
        
        # ВАЖНО: Проверяем, есть ли пользователь в словаре
        if user_id not in saved_facts:
            saved_facts[user_id] = []  # Создаём пустой список
        
        saved_facts[user_id].append(fact_text)
        await callback.message.answer("✅ Сохранено!")
    
    elif callback.data == 'more':
        random_fact = random.choice(facts)
        buttons = [
            [types.InlineKeyboardButton(text='Сохранить', callback_data='save')],
            [types.InlineKeyboardButton(text='Ещё факты', callback_data='more')],
            [types.InlineKeyboardButton(text='Сохранённые', callback_data='saved')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text(f"📌 {random_fact}", reply_markup=keyboard)
    
    elif callback.data == 'saved':
        if user_id in saved_facts and saved_facts[user_id]:
            text = "\n\n".join(saved_facts[user_id])
            await callback.message.answer(f"📚 Ваши факты:\n\n{text}")
        else:
            await callback.message.answer("📭 Пока пусто")
        
        
    
   
async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    print("Бот запустился")
    asyncio.run(main())
    
