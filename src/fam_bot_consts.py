from datetime import date, timedelta, datetime as dt

work_days_callback_map = {
    'today': tuple(map(int, date.today().strftime("%d-%m-%Y").split("-"))),
    'next_day': tuple(map(int, (dt.now() + timedelta(days=1)).strftime("%d-%m-%Y").split("-"))),
    'day_add_1': tuple(map(int, (dt.now() + timedelta(days=2)).strftime("%d-%m-%Y").split("-"))),
}

if __name__ == "__main__":
    b = work_days_callback_map.get('next_day')
    pass