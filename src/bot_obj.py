import telebot
from telebot import types
import os
import json
from .fam_bot_consts import work_days_callback_map
from .work_d_out_publisher import publish_to_work_days
from .g_cloud_publisher import publish_g_cloud_in
from base64 import b64encode

bot = telebot.TeleBot(os.environ.get('telegram_bot_1'))


@bot.message_handler(commands=['start'])
def get_start_msgs(message):
    bot.send_message(message.chat.id, text="Меня зовут radmir_family_bot, я помошник вашей семьи.\n"
                                           "Наберите /help, чтобы узнать о моих возможностях.")


# @bot.message_handler(content_types=['document'])
@bot.message_handler(commands=['files'])
def files_call(message):
    """
    Транспорт файлов на загрузку в google cloud.
    :param message:
    :return:
    """
    text = 'Хотите загрузить файлы на гугл диск?'
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Да"))
    keyboard.add(types.KeyboardButton(text="Нет"))
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
    bot.register_next_step_handler(message, files_callback)

def files_callback(message):
    text = 'Загрузите файл в формате zip'
    bot.send_message(message.chat.id, text=text)
    bot.register_next_step_handler(message, google_cloud_callback)

def google_cloud_callback(message):
    text = 'Ваши фотки грузятся на гугл диск!\n' \
           'Пока в тестовом режиме на тестовый аккаунт!'
    bot.send_message(message.chat.id, text=text)
    file_name = message.document.file_name
    file_id_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_id_info.file_path)
    file_to_floader = b64encode(downloaded_file).decode('utf-8')
    data = {'f_data': file_to_floader}
    data['f_name'] = file_name
    rabbitMQ_body = json.dumps(data)
    publish_g_cloud_in(data=rabbitMQ_body)

@bot.message_handler(commands=['help'])
def get_help_msgs(message):
    bot.send_message(message.chat.id, text="Я могу сделать для вас следующее\n"
                                           "1. Чтобы узнать, когда у Радмира выходной, напишите- /work \n"
                                           "2. В планах: Сохранение изображений и видео в семейный архив на облаке.\n")


@bot.message_handler(commands=['work'])
def get_work_msgs(message):
    text = "Пожалуйста, выберите, когда будет следующий\n" \
           "первый рабочий день Радмира"
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_today = types.InlineKeyboardButton(text='Сегодня', callback_data='today')  # кнопка «Да»
    keyboard.add(key_today)  # добавляем кнопку в клавиатуру
    key_next_day = types.InlineKeyboardButton(text='Завтра', callback_data='next_day')
    keyboard.add(key_next_day)
    key_day_add_1 = types.InlineKeyboardButton(text='Послезавтра', callback_data='day_add_1')
    keyboard.add(key_day_add_1)
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
    bot.register_next_step_handler(message, callback_worker)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """
    Отправляет сообщение в очередь RabbitMQ work_d_out
    :param call:
    :return:
    """
    data_for_work_days_returns = work_days_callback_map.get(call.data)
    date_to_calculate_work_days = {
        'date': data_for_work_days_returns,
        'chat_id': call.message.chat.id}
    rabbitMQ_body = json.dumps(date_to_calculate_work_days)
    publish_to_work_days(rabbitMQ_body)
    bot.send_message(call.message.chat.id, text='Скоро будет загружен календарь\n'
                                                'рабочих дней Радмира!')


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=1)
    pass
