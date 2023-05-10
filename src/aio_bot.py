from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .states import ClaendarStates, YaDriveStates
from .aio_keyboards import YaKeyboards, CalendarKeyboards
from .publishers import yandex_drive_publish, calendar_in_publish
from .fam_bot_consts import work_days_callback_map
from base64 import b64encode
# from aiogram.utils import executor
import os
import json
# from .fam_bot_consts import work_days_callback_map

storage = MemoryStorage()
family_bot = Bot(token=os.environ.get('telegram_bot_1'))
dp = Dispatcher(family_bot, storage=storage)

ya_folder = []

@dp.message_handler(commands=['start'])
def get_start_msgs(message):
    family_bot.send_message(message.chat.id, text="Меня зовут radmir_family_bot, я помошник вашей семьи.\n"
                                                  "Наберите /help, чтобы узнать о моих возможностях.")


@dp.message_handler(commands=['files'])
async def files_call(message):
    """
    Транспорт файлов на загрузку в google cloud.
    :param message:
    :return:
    """
    text = 'Хотите загрузить файлы на Яндекс диск?'
    await YaDriveStates.arhcieve_dir.set()
    await family_bot.send_message(message.chat.id, text=text, reply_markup=YaKeyboards.drive_kb())


@dp.message_handler(state=YaDriveStates.arhcieve_dir)
async def files_call(message, state: FSMContext):
    """
    Транспорт файлов на загрузку в google cloud.
    :param message:
    :return:
    """
    text = 'Как назвать папку в архиве?'
    async with state.proxy() as data:
        data['name'] = message.text
    await YaDriveStates.next()
    await family_bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=YaDriveStates.req_for_files)
async def files_callback(message, state: FSMContext):
    text = 'Окей, Загрузите ваши файлы'
    async with state.proxy() as data:
        data['name'] = message.text
    folder = message.html_text
    ya_folder.append(folder)
    data = {'action': 'create_folder', 'folder_name': folder}
    rabbitMQ_body = json.dumps(data)
    yandex_drive_publish(msg=rabbitMQ_body)
    await YaDriveStates.next()
    await family_bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['photo'], state=YaDriveStates.wait_for_files)
async def files_callback(message, state: FSMContext):
    text = f'Файлы загружаются на Яндекс диск'
    file_name = message.photo[-1].file_unique_id
    file_id_info = await family_bot.get_file(message.photo[-1].file_id)
    downloaded_file = await family_bot.download_file(file_path=file_id_info.file_path)
    file_to_floader = b64encode(downloaded_file.getvalue()).decode('utf-8')
    data = {'f_data': file_to_floader, 'f_name': file_name + '.jpg', 'action': 'load_files', 'folder_name': ya_folder[0]}
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
async def get_work_msgs(message):
    text = "Пожалуйста, выберите, когда будет следующий\n" \
           "первый рабочий день Радмира"
    await ClaendarStates.wait_answer.set()
    await family_bot.send_message(message.chat.id, text=text, reply_markup=CalendarKeyboards.calendar_kb())


@dp.message_handler(state=ClaendarStates.wait_answer)
async def wait_answer_calendar(message: types.Message, state: FSMContext):
    """
    Отправляет сообщение в очередь RabbitMQ work_d_out
    :param call:
    :return:
    """
    async with state.proxy() as data:
        data['name'] = message.text
    data_for_work_days_returns = work_days_callback_map.get(message.html_text)
    date_to_calculate_work_days = {'date': data_for_work_days_returns, 'chat_id': message.chat.id}
    rabbitMQ_body = json.dumps(date_to_calculate_work_days)
    calendar_in_publish(msg=rabbitMQ_body)
    await family_bot.send_message(message.chat.id, text='Скоро будет загружен календарь\n '
                                                        'рабочих дней Радмира!',
                                  reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    # executor.start_polling(dp)
    pass
