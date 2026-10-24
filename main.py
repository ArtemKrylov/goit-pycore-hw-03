from csv import excel
from datetime import datetime, timedelta
import random
import re
from typing import TypedDict


# Завдання 1
def get_days_from_today(date: str) -> int | None:
    # calcs number of days between input date with format "%Y-%m-%d" and current date
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except:
        print("Wrong date format")
        return None

    curr_date = datetime.today()
    delta = parsed_date.toordinal() - curr_date.toordinal()
    return delta


print("Днів між 2021-10-09 та сьогодні: ", get_days_from_today("2021-10-09"))
print("Днів між 2026-10-27 та сьогодні: ", get_days_from_today("2026-10-27"))


# Завдання 2
def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    # return sorted list of quantity unique integers between min (>=1) and max (<=1000)
    try:
        min < 1
    except:
        print("Min must be not less than 1")
        return []

    try:
        max > 1000
    except:
        print("Max must be not bigger than 1000")
        return []

    return sorted(random.sample(range(min, max + 1), quantity))


print("Ваші лотерейні числа: ", get_numbers_ticket(1, 49, 6))


# Завдання 3
def normalize_phone(phone_number: str) -> str:
    # gets phone number string and formats it to +380d*10 template

    cleared_number = re.sub(r"\D", "", phone_number)
    NORMAL_NUMBER_WITHOUT_PREFIX_LEN = 10
    without_prefix_number = (
        re.sub(r"^38|^8", "", cleared_number)
        if len(cleared_number) > NORMAL_NUMBER_WITHOUT_PREFIX_LEN
        else cleared_number
    )
    UA_NUMBER_PREFIX = "+38"
    return f"{UA_NUMBER_PREFIX}{without_prefix_number}"


raw_numbers = [
    "8067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)


# Завдання 4
class User(TypedDict):
    name: str
    birthday: str


class Congratulation(TypedDict):
    name: str
    congratulation_date: str


DATE_FORMAT = "%Y.%m.%d"
WEEKEND_DAYS = (5, 6)
DAYS_IN_WEEK = 7


def get_upcoming_birthdays(
    users: list[User], date_format: str = DATE_FORMAT, is_workday_congrats: bool = True
) -> list[Congratulation]:
    # gets users list with name and birhday properties and return list of upcoming birthday within next 7 day (including today); if is_workday_congrats param is true and birthday is on weekend day - moves congrat to nearest workday

    curr_date = datetime.today()
    congrats = []

    # for leap year error catching
    def birthday_in_year(birthday, year):
        try:
            return birthday.replace(year=year)
        except ValueError:
            return birthday.replace(year=year, day=28)

    for user in users:
        try:
            birthday_datetime = datetime.strptime(user["birthday"], date_format)
        except ValueError:
            print(f"birthday date does not match format {date_format}")
            continue

        birthday_this_year = birthday_in_year(birthday_datetime, curr_date.year)
        # for congrat in new year
        if birthday_this_year.toordinal() < curr_date.toordinal():
            birthday_this_year = birthday_in_year(birthday_datetime, curr_date.year + 1)
        day_of_birth_this_year = birthday_this_year.weekday()

        delta_days = birthday_this_year.toordinal() - curr_date.toordinal()
        if delta_days >= 7 or delta_days < 0:
            continue

        is_weekend = day_of_birth_this_year in WEEKEND_DAYS
        if is_weekend and is_workday_congrats:
            birthday_this_year += timedelta(days=DAYS_IN_WEEK - day_of_birth_this_year)
            delta_days = birthday_this_year.toordinal() - curr_date.toordinal()

        congrats.append(
            {
                "name": user["name"],
                "congratulation_date": datetime.strftime(
                    curr_date + timedelta(days=delta_days), date_format
                ),
            }
        )

    return congrats


users = [
    {"name": "Jane Doe", "birthday": "1991.01.02"},
    {"name": "John Smith", "birthday": "1973.10.24"},
    {"name": "Jane Smith", "birthday": "1990.10.25"},
    {"name": "Jane Doe", "birthday": "1991.10.28"},
]
upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays)
