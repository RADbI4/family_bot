from src.aio_bot import dp
from aiogram.utils import executor


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    pass
