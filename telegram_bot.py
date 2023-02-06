import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '5871188271:AAHKSCQsu6Vdh3AG_WvNoYgJVjJUnC3TJsw'
BASE_URL = 'https://openexchangerates.org/api'
API_EX = '4acb7e8594fd4b2ab23097f147317f6b'

logging.basicConfig(level=logging.INFO)

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

USD = KeyboardButton("\U0001F1FA\U0001F1F8 USD")
EUR = KeyboardButton("\U0001F1EA\U0001F1FA EUR")
RUB = KeyboardButton("\U0001F1F7\U0001F1FA RUB")
SEK = KeyboardButton("\U0001F1F8\U0001F1EA SEK")
KZT = KeyboardButton("\U0001F1F0\U0001F1F3 KZT")
markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup.add(USD, EUR, RUB, SEK)

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.answer("Hi! This bot shows current exchange rates", reply_markup=markup)

currency_symbols = {
    "\U0001F1FA\U0001F1F8 USD": "USD",
    "\U0001F1EA\U0001F1FA EUR": "EUR",
    "\U0001F1F7\U0001F1FA RUB": "RUB",
    "\U0001F1F8\U0001F1EA SEK": "SEK",
    "\U0001F1F0\U0001F1FF KZT": "KZT"
}
currency_flags = {value: key for key, value in currency_symbols.items()}



@dp.message_handler(lambda message: message.text in currency_symbols.keys())
async def process_currency_button(message: Message):
    print(message)
    currency = currency_symbols[message.text]
    amount=1 
    exchange_rate = get_exchange_rates(currency)
    await message.answer(f"Exchange rate for {amount} {message.text}:\n{exchange_rate}")
   

    
def get_exchange_rates(selected_currency):    
    url = f'{BASE_URL}/latest.json?app_id={API_EX}'
    response = requests.get(url)
    data = response.json()
    currency= data['rates']
    currency_list = ['USD','SEK','EUR','RUB','KZT']
    exchange_rate = ""
    for i in currency_list:
        exchange_rate += f"{currency_flags[i]} = {(currency['USD']/currency[selected_currency])/(currency['USD']/currency[i])}\n"
    # exchange_rate = f" USD = {currency['USD']}\n SEK = {currency['SEK']}\n EUR = {currency['EUR']}\n RUB = {currency['RUB']}\n GPB = {currency['GBP']}\n KZT = {currency['KZT']}"
    return (exchange_rate)
 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

    



    




