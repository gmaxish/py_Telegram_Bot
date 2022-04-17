import telebot
from telebot import types
import datetime


bot = telebot.TeleBot("5112076920:AAFgLwEqEeQcWeVPqxts7UO8g-xUNwSC7UA")


# @bot.message_handler()
# def send_message(message):
#     bot.send_message(message.chat.id, f'{message.from_user.first_name} {message.from_user.last_name} '
#                                       f'начните работу с команды /start.\n')


@bot.message_handler(commands=['start'])
def send_message(message):
    # bot.send_message(message.chat.id, f'{message.from_user.first_name} {message.from_user.last_name} '
    #                                   f'начните работу с команды /start.\n')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_manicure = types.KeyboardButton("💅🏻 Маникюр")
    button_pedicure = types.KeyboardButton("👣 Педикюр")
    button_beautician = types.KeyboardButton("👄 Косметолог")
    button_visagiste = types.KeyboardButton("👸🏼 Визажист")
    markup.add(button_manicure, button_pedicure, button_beautician, button_visagiste, row_width=2)
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name} {message.from_user.last_name}.\n'
                                              f'Выберите, пожалуйста, процедуру для записи.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def second_line(message):
    if message.text == "Маникюр" or "Педикюр" or "Косметолог" or "Визажист":
        days = []
        today = datetime.datetime.today()
        days_list = [today + datetime.timedelta(days=x) for x in range(0, 10)]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for day in days_list:
            button_date = types.KeyboardButton(day.strftime("%d-%m %a"))
            days.append(button_date.text)
        markup.add(days[0], days[1], days[2], days[3], days[4], days[5],
                   days[6], days[7], days[8], days[9], row_width=5)
        bot.send_message(message.chat.id, "Выберите дату", reply_markup=markup)


bot.infinity_polling()
