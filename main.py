import datetime
import sys
import requests
import telebot
from telebot import types

sys.path.append('/home/a/akchur2k/programming-circle.ru/.local/lib/python3.6/site-packages')

bot = telebot.TeleBot("1859159548:AAHfnoEYS6HARO0EoEnAfmWT_nCV4qOwvkI")

# API https://api.openweathermap.org/
token = "68cc2d3173c1c4b9d04e6a33419160f4"


def answer_weather(message):
    weather_icons = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Слабый дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
        "Shower rain": "Ливень \U000026C6"
    }
    try:
        city_name = message.text

        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={token}&units=metric"
        )
        data = r.json()

        weather_description = data["weather"][0]["main"]
        if weather_description in weather_icons:
            wd = weather_icons[weather_description]
        else:
            wd = "Посмотри в окно, у меня нет иконки на этот день XD!"

        city_name = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        weather_send = (f"**{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}**\n"
                        f"Погода в городе: {city_name}\nТемпература: {temperature}C° {wd}\n"
                        f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\n"
                        f"Скорость ветра: {wind} м/с\nВосход: {sunrise}\n"
                        f"Закат: {sunset}")

        bot.send_message(message.chat.id, weather_send, parse_mode='html')
        bot.register_next_step_handler(message, answer_weather)
    except Exception as ex:
        bot.send_message(message.chat.id, "Указанный город не найден!")
        bot.register_next_step_handler(message, answer_weather)


@bot.message_handler(commands=['start', 'help'])
def helper(message):
    send_message = f"<b>Привет {message.from_user.first_name}!</b>\n" \
                   f"Я бот для бабули. У меня не так много возможностей.\n" \
                   f" <b>Вот что я могу!</b>\n" \
                   f"Если хочешь узнать погоду напиши {'/weather'}\n"
    bot.send_message(message.chat.id, send_message, parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Мантурово')
    btn2 = types.KeyboardButton('Сыктывкар')
    btn3 = types.KeyboardButton('Санкт-Петербург')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Введите или выберите из списка название города', reply_markup=markup)
    bot.register_next_step_handler(message, answer_weather)


bot.polling(none_stop=True)
