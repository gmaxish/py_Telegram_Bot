import datetime
import telebot
from telebot import types
from dateutil.parser import parse

TOKEN = "5112076920:AAFgLwEqEeQcWeVPqxts7UO8g-xUNwSC7UA"

bot = telebot.TeleBot(TOKEN)

procedure = None
client = None
date = None
time = None


@bot.message_handler(commands=['start'])
def first_line(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_manicure = types.KeyboardButton("💅🏻 Маникюр")
    button_pedicure = types.KeyboardButton("👣 Педикюр")
    button_beautician = types.KeyboardButton("👄 Косметолог")
    button_visagiste = types.KeyboardButton("👸🏼 Визажист")
    markup.add(button_manicure, button_pedicure, button_beautician, button_visagiste, row_width=2)
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name} {message.from_user.last_name}.\n'
                                      f'Выберите, пожалуйста, процедуру для записи.', reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(message.chat.id, callback=second_line)
    global client
    client = f'{message.from_user.first_name} {message.from_user.last_name}'


def second_line(message):
    global procedure
    procedure = message.text
    days = []
    today = datetime.datetime.today()
    days_list = [today + datetime.timedelta(days=x) for x in range(0, 10)]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in days_list:
        button_date = types.KeyboardButton(day.strftime("%d.%m %a"))
        days.append(button_date.text)
    markup.add(days[0], days[1], days[2], days[3], days[4], days[5],
               days[6], days[7], days[8], days[9], row_width=5)
    bot.send_message(message.chat.id, "Выберите дату", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(message.chat.id, callback=third_line)


def third_line(message):
    global date
    date = message.text
    start_time = datetime.time(10, 30, 0)
    finish = parse(str(datetime.time(19, 0, 0)))
    td = datetime.timedelta(minutes=30)
    working_times = []
    while start_time != finish:
        start_time = parse(str(start_time)) + td
        working_times.append(start_time.strftime('%H:%M'))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(working_times[0], working_times[1], working_times[2], working_times[3], working_times[4],
               working_times[5], working_times[6], working_times[7], working_times[8], working_times[9],
               working_times[10], working_times[11], working_times[12], working_times[13], working_times[14],
               working_times[15], working_times[16], row_width=int(len(working_times) / 3))
    bot.send_message(message.chat.id, "Выберите время для записи", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(message.chat.id,callback=fourth_line)

def fourth_line(message):
    global time
    time = message.text
    keyboard = types.InlineKeyboardMarkup()
    button_true = types.InlineKeyboardButton(text="Верно!", callback_data='Ok')
    button_false = types.InlineKeyboardButton(text="Не верно!", callback_data='No')
    keyboard.add(button_true, button_false)
    bot.send_message(message.chat.id, f'Проверьте, верно ли создана запись? '
                                      f'\nПроцедура - {procedure}'
                                      f'\nНа имя:  {client}'
                                      f'\nДата: {date}'
                                      f'\nВремя:  {time}',
                     reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(callback):
    if callback.data == "Ok":
        bot.send_message(callback.message.chat.id, 'Запись создана! Ждем Вашего визита!')
        end_markup = types.ReplyKeyboardRemove(selective=True)
        bot.send_message(callback.message.chat.id, text='До скорой встречи!', reply_markup=end_markup)
    elif callback.data == "No":
        bot.send_message(callback.message.chat.id, 'Давайте начнем сначала. Воcпользуйтесь командой /start')


bot.polling()

print(client, procedure, date, time)
