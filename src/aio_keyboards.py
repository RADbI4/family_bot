from aiogram import types


class CalendarKeyboards:
    @staticmethod
    def calendar_kb():
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(types.KeyboardButton(text="Сегодня"))
        keyboard.add(types.KeyboardButton(text="Завтра"))
        keyboard.add(types.KeyboardButton(text="Послезавтра"))
        return keyboard


class YaKeyboards:
    @staticmethod
    def drive_kb():
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(types.KeyboardButton(text="Да"))
        keyboard.add(types.KeyboardButton(text="Нет"))
        return keyboard


