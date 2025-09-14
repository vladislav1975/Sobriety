import calendar
from datetime import date
from dateutil import relativedelta

MESSAGES = {"inputDay": {"ru": "Введите день", "en": "Enter a day"}
            , "inputMonth": {"ru": "Введите месяц", "en": "Enter a month"}
            , "inputYear": {"ru": "Введите год", "en": "Enter a year"}
            
            , "errorInt": {"ru": "Ошибка ввода. Введите целое число", "en": "Input error. Please enter an integer"}
            , "inFuture": {"ru": "Введенная дата в будущем. Пожалуйста, введите корректную дату в прошлом", "en": "The entered date is in the future. Please enter a valid past date"}
            , "enteredDate": {"ru": "Вы ввели дату", "en": "You entered the date"}
            , "day": {"ru": "день", "en": "day"}
            , "month": {"ru": "месяц", "en": "month"}
            , "year": {"ru": "год", "en": "year"}
            , "daysFrom": {"ru": "Дней с введенной даты до сегодня", "en": "Days from the given date to today"}
            , "whichIs": {"ru": "Что составляет", "en": "Which is"}
            , "years": {"ru": "лет", "en": "years"}
            , "months": {"ru": "месяцев", "en": "months"}
            , "and": {"ru": "и", "en": "and"}
            , "days": {"ru": "дней", "en": "days"}  
}

def inputInt(prompt, min_value, max_value, lang="en"):
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
    lang = input("Choose language: \n-----------\nRu\nEn(default)\n----------- \n").strip().lower()
    if lang not in ["ru", "en"]:
        print("Invalid choice, defaulting to English.")
        lang = "en"
    return lang    

def inputDate(lang="en"):
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
    # Set language preference
    lang = chooseLanguage()
    print()
    # Input month and year first
    given_date = inputDate(lang)
    day, month, year = given_date.day, given_date.month, given_date.year

    print(f"{MESSAGES['enteredDate'][lang]}: {MESSAGES['day'][lang]} {day}, {MESSAGES['month'][lang]} {month}, {MESSAGES['year'][lang]} {year}")

    # Calculate days from given date to today
    today = date.today()
    delta = (today - given_date).days
    print(f"{MESSAGES['daysFrom'][lang]}: {delta}")

    diff = relativedelta.relativedelta(today, given_date)
    print(f"{MESSAGES['whichIs'][lang]} {diff.years} {MESSAGES['years'][lang]}, {diff.months} {MESSAGES['months'][lang]}, {MESSAGES['and'][lang]} {diff.days} {MESSAGES['days'][lang]}.")


if __name__ == "__main__":
    main()