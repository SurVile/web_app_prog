import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Filter
from aiogram.types.web_app_info import WebAppInfo
from aiogram.enums import ParseMode

from typing import Union, Dict, Any
import json


class WebAppDataFilter(Filter):

    async def __call__(self, message: types.Message, **kwargs) -> Union[bool, Dict[str, Any]]:
        return dict(web_app_data=message.web_app_data) if message.web_app_data else False


TOKEN = '7329234509:AAGKqp-6gE9JAC6Rz_nS4FeipelB5XABr38'
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    web_button = types.KeyboardButton(
        text='Открыть веб-приложение',
        web_app=WebAppInfo(url='https://survile.github.io/Top-Python-App/')
    )
    kb = types.ReplyKeyboardMarkup(keyboard=[[web_button]], resize_keyboard=True)

    await message.answer('Привет, пользователь!', reply_markup=kb)


@dp.message(WebAppDataFilter())
async def web_app_handler(message: types.Message):
    res = json.loads(message.web_app_data.data)
    item_name, img_url = '', ''

    if res['data_type'] == 'user_reg':
        await message.answer(f'ФИО: {res["data_name"]}\nEmail: {res["data_email"]}\nТелефон: {res["data_tel"]}')
    elif res['data_type'] == 'buy_item':
        match res['data_name']:
            case 'dead_pool':
                item_name = 'Dead Pool'
                img_url = 'https://github.com/SurVile/Top-Python-App/blob/main/img/dead%20pool.webp'
            case 'spider_man':
                item_name = 'Spider Man'
                img_url = 'https://github.com/SurVile/Top-Python-App/blob/main/img/spider%20man.jpeg'
            case 'iron_man':
                item_name = 'Iron Man'
                img_url = 'https://github.com/SurVile/Top-Python-App/blob/main/img/iron%20man.jpg'

        await message.answer(text=f'Вы выбрали фигурку {item_name}? {img_url}')


async def main():
    await dp.start_polling(bot)

# Точка входа
if __name__ == '__main__':  # проверяем название программы
    asyncio.run(main())
