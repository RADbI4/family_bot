from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .states import YaDriveStates
from .publishers import yandex_drive_publish, calendar_in_publish
from base64 import b64encode
import datetime
import os
import json

storage = MemoryStorage()
family_bot = Bot(token=os.environ.get('telegram_bot_1'))
dp = Dispatcher(family_bot, storage=storage)


@dp.message_handler(commands=['start'])
def get_start_msgs(message):
    family_bot.send_message(message.chat.id, text="Меня зовут radmir_family_bot, я помошник вашей семьи.\n"
                                                  "Наберите /help, чтобы узнать о моих возможностях.")


@dp.message_handler(commands=['files'])
async def files_call(message):
    """
    Транспорт файлов на загрузку в yandex cloud.
    :param message:
    :return:
    """
    text = 'Окей, Загрузите ваши файлы'
    await YaDriveStates.wait_for_files.set()
    await family_bot.send_message(message.chat.id, text=text)


@dp.message_handler(content_types=['photo', 'video'], state=YaDriveStates.wait_for_files)
async def files_callback(message, state: FSMContext):
    text = f'Файлы загружаются на Яндекс диск'
    file_name = message.photo[-1].file_unique_id
    file_id_info = await family_bot.get_file(message.photo[-1].file_id)
    downloaded_file = await family_bot.download_file(file_path=file_id_info.file_path)
    file_to_floader = b64encode(downloaded_file.getvalue()).decode('utf-8')
    data = {'f_data': file_to_floader,
            'f_name': file_name + '.jpg',
            'action': 'load_files',
            'folder_name': datetime.datetime.date(datetime.datetime.today()).strftime('%d-%m-%y')}
    rabbitMQ_body = json.dumps(data)
    yandex_drive_publish(msg=rabbitMQ_body)

    await family_bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['help'])
async def get_help_msgs(message):
    await family_bot.send_message(message.chat.id, text="Я могу сделать для вас следующее:\n"
                                                        "1. Чтобы узнать, когда у Радмира выходной, напишите- /work \n"
                                                        "2. Чтобы сохранить ваши фото на Яндекс диск Камиллы и Радмира\n"
                                                        "нажмите /files\n")

@dp.message_handler(commands=['work'])
async def answer_work(message: types.Message, state: FSMContext):
    """
    Отправляет сообщение в очередь RabbitMQ work_d_out
    :param call:
    :return:
    """
    async with state.proxy() as data:
        data['name'] = message.text
    rabbitMQ_body = json.dumps({'load': True})
    calendar_in_publish(msg=rabbitMQ_body)
    await family_bot.send_message(message.chat.id, text='Скоро будет загружен календарь\n '
                                                        'рабочих дней Радмира!')

if __name__ == '__main__':
    # executor.start_polling(dp)
    pass
