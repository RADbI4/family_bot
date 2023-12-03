from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import bot_const as bc

storage = MemoryStorage()
family_bot = Bot(token=os.environ.get('telegram_bot_1'))
dp = Dispatcher(family_bot, storage=storage)


@dp.message_handler(commands=['start'])
async def get_start_msgs(message):
    await family_bot.send_message(message.chat.id, text="Меня зовут radmir_family_bot, я помошник вашей семьи.\n"
                                                  "Наберите /help, чтобы узнать о моих возможностях.")

@dp.message_handler(commands=['help'])
async def get_help_msgs(message):
    bc.base_sleep()
    await family_bot.send_message(message.chat.id, text="Я могу сделать для вас следующее:\n"
                                                        "1. Чтобы узнать, когда у Радмира выходной, напишите- /work \n"
                                                        )

@dp.message_handler(commands=['work'])
async def answer_work(message: types.Message, state: FSMContext):
    """
    Отвечает за отправку ссыли на моё рассписание
    :param call:
    :return:
    """
    bc.base_sleep()
    await family_bot.send_message(message.chat.id, text='Календарь рабочих дней радмира:\n'
                                                        'https://docs.google.com/spreadsheets/d/1_Iuwdc1ytRH8yiFITAG1Pf_Y1BTe9m5o57aDPkSqRW4/edit#gid=1462589716')

if __name__ == '__main__':
    # executor.start_polling(dp)
    pass
