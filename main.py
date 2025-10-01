import calendar  # For month/day calculations
from datetime import date  # For working with dates
from dateutil import relativedelta  # For calculating date differences

MESSAGES = {
    # Dictionary containing all user-facing messages in Russian and English
    "inputDay": {"ru": "Введите день", "en": "Enter a day"},
    "inputMonth": {"ru": "Введите месяц", "en": "Enter a month"},
    "inputYear": {"ru": "Введите год", "en": "Enter a year"},
    "errorInt": {"ru": "Ошибка ввода. Введите целое число", "en": "Input error. Please enter an integer"},
    "inFuture": {"ru": "Введенная дата в будущем. Пожалуйста, введите корректную дату в прошлом", "en": "The entered date is in the future. Please enter a valid past date"},
    "enteredDate": {"ru": "Вы ввели дату", "en": "You entered the date"},
    "day": {"ru": "день", "en": "day"},
    "month": {"ru": "месяц", "en": "month"},
    "year": {"ru": "год", "en": "year"},
    "daysFrom": {"ru": "Дней с введенной даты до сегодня", "en": "Days from the given date to today"},
    "whichIs": {"ru": "Что составляет", "en": "Which is"},
    "years": {"ru": "лет", "en": "years"},
    "months": {"ru": "месяцев", "en": "months"},
    "and": {"ru": "и", "en": "and"},
    "days": {"ru": "дней", "en": "days"}
}

def inputInt(prompt, min_value, max_value, lang="en"):
    """
    Prompt the user for an integer input within a specified range.
    Repeats until a valid integer in the range is entered.
    """
    while True:
        try:
            value = int(input(prompt + f" ({min_value}-{max_value}): "))
            if min_value <= value <= max_value:
                return value
            else:
                print(MESSAGES["errorInt"][lang])
        except ValueError:
            print(MESSAGES["errorInt"][lang])

def chooseLanguage():
    """
    Ask the user to choose a language (Russian or English).
    Defaults to English if input is invalid.
    """
    lang = input("Choose language: \n-----------\nRu\nEn(default)\n----------- \n").strip().lower()
    if lang not in ["ru", "en"]:
        print("Invalid choice, defaulting to English.")
        lang = "en"
    return lang    

def inputDate(lang="en"):
    """
    Prompt the user to enter a valid past date (day, month, year).
    Ensures the date is not in the future and the day is valid for the given month/year.
    """
    month = inputInt(MESSAGES["inputMonth"][lang], 1, 12)
    year = inputInt(MESSAGES["inputYear"][lang], 1900, 2100)
    max_day = calendar.monthrange(year, month)[1]
    day = inputInt(MESSAGES["inputDay"][lang], 1, max_day)
    given_date = date(year, month, day)
    if given_date >= date.today():
        print(MESSAGES["inFuture"][lang])
        return inputDate(lang)
    return given_date

def main():   
    """
    Main function to run the sobriety date calculator.
    - Sets language
    - Gets a valid past date from the user
    - Displays the entered date
    - Calculates and displays the number of days since that date
    - Calculates and displays the difference in years, months, and days
    """
    # Set language preference
    lang = chooseLanguage()
    print()
    # Input month and year first
    given_date = inputDate(lang)
    day, month, year = given_date.day, given_date.month, given_date.year

    # Display the entered date
    print(f"{MESSAGES['enteredDate'][lang]}: {MESSAGES['day'][lang]} {day}, {MESSAGES['month'][lang]} {month}, {MESSAGES['year'][lang]} {year}")

    # Calculate days from given date to today
    today = date.today()
    delta = (today - given_date).days
    print(f"{MESSAGES['daysFrom'][lang]}: {delta}")

    # Calculate difference in years, months, and days
    diff = relativedelta.relativedelta(today, given_date)
    print(f"{MESSAGES['whichIs'][lang]} {diff.years} {MESSAGES['years'][lang]}, {diff.months} {MESSAGES['months'][lang]}, {MESSAGES['and'][lang]} {diff.days} {MESSAGES['days'][lang]}.")


if __name__ == "__main__":
    # Entry point for the script
    main()