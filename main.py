import requests
import telebot
import wikipediaapi
from googletrans import Translator

bot = telebot.TeleBot('<your telegram-bot token>')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, """Добрый `день, я бот по поиску погоды и информации на wiki. Всегда рад вам помочь!""")
    help(message)

@bot.message_handler(commands=['help'])
def show_help(message):
    help(message)


@bot.message_handler(commands=['developer'])
def show_developer(message):
    bot.send_message(message.chat.id, '''Username создателя - @ENifakin''' )



def help(message):
    bot.send_message(message.chat.id, '''Я - бот, который позволяет просматривать погоду и информацию на wiki
/wiki - поиск чего-либо на wiki
/weather - поиск погоды
/help - позволяет просмотреть возможности
/translate - позволяет переводить вводимый текст
/developer - показывает username создателя бота''')

@bot.message_handler(commands=['weather'])
def search_weather(message):
    send = bot.send_message(message.chat.id, 'Введите название города')
    bot.register_next_step_handler(send, city)



def city(message):
    try:
        API_key = '<your weather-api token>'
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_key}&units=metric&lang=ru')
        data = r.json()
        city = data['name']
        cur_weather = data['main']['temp']

        if cur_weather > 0:
            cur_weather = f'+ {round(cur_weather)}'
        else:
            cur_weather = f'- {round(cur_weather)}'

        feels_like = data['main']['feels_like']

        if feels_like > 0:
            feels_like = f'+ {round(feels_like)}'
        else:
            feels_like = f'- {round(feels_like)}'

        wind_speed = data['wind']['speed']

        z = data["weather"]
        description = z[0]["description"]
        bot.send_message(message.chat.id, f'''Данные города {city}
Описание: {description}
Текущая температура: {cur_weather} °C
Ощущается как: {feels_like} °C
Скорость ветра: {wind_speed} м/с''')
    except:
        bot.send_message(message.chat.id, 'Ошибка в поиске города!!!')

@bot.message_handler(commands=['wiki'])
def search_info(message):
    send = bot.send_message(message.chat.id, 'Укажите, что нужно найти')
    bot.register_next_step_handler(send, wiki)
    
def wiki(message):
    try:
        wiki = wikipediaapi.Wikipedia('ru')
        page = wiki.page(f'{message.text}')
        bot.send_message(message.chat.id,
                         f'Вот что мне удалось найти\n{page.fullurl}')
    except:
        bot.send_message(message.chat.id, 'Возникла непредвиденная ошибка!')


@bot.message_handler(commands=['translate']) # РАСПИСАТЬ МЕТОД ДЛЯ ПЕРЕВОДА ЯЗЫКОВ 
def send_answer(message):
    mar = telebot.types.InlineKeyboardMarkup()
    item1 = telebot.types.InlineKeyboardButton('rus-eng',callback_data='rus-eng')
    item2 = telebot.types.InlineKeyboardButton('eng-rus',callback_data='eng-rus')
    mar.add(item1,item2)
    bot.send_message(message.chat.id, 'Укажите, с какого на какой язык нужно перевечти',reply_markup=mar)



@bot.callback_query_handler(func=lambda call:True)
def query_hendler(call):
    if call.message:
        if call.data == 'rus-eng':
            send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Режим перевода: rus-eng\nВведите, что требуется перевести",reply_markup=None)
            bot.register_next_step_handler(send,translateOnEng)
        elif call.data == 'eng-rus':
            send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Режим перевода: eng-rus\nВведите, что требуется перевести",reply_markup=None)
            bot.register_next_step_handler(send,translateOnRus)

def translateOnEng(message):
    translator = Translator()
    bot.send_message(message.chat.id,translator.translate(message.text,src='ru', dest='en').text)

def translateOnRus(message):
    translator = Translator()
    bot.send_message(message.chat.id,translator.translate(message.text,src='en', dest='ru').text)





if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
