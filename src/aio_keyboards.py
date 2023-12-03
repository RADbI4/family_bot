from aiogram import types

class YaKeyboards:
    @staticmethod
    def drive_kb():
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(types.KeyboardButton(text="Да"))
        keyboard.add(types.KeyboardButton(text="Нет"))
        return keyboard


