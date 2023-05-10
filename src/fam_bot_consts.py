from datetime import date, timedelta, datetime as dt

work_days_callback_map = {
    'Сегодня': tuple(map(int, date.today().strftime("%d-%m-%Y").split("-"))),
    'Завтра': tuple(map(int, (dt.now() + timedelta(days=1)).strftime("%d-%m-%Y").split("-"))),
    'Послезавтра': tuple(map(int, (dt.now() + timedelta(days=2)).strftime("%d-%m-%Y").split("-"))),
}

if __name__ == "__main__":
    b = work_days_callback_map.get('next_day')
    pass