
"""sobriety_calculator

Small utility module that provides CLI helpers to read a sobriety/quit
date, save/load it from a config file and calculate the time elapsed
in days / years-months-days. All user-facing strings are stored in
the `MESSAGES` mapping to support English and Russian output.

Public functions:
 - choose_language()
 - input_date(lang)
 - get_date(lang)
 - save_date_to_file(given_date, lang)
 - calculate_sobriety_delta(given_date)
 - format_output(total_days, delta_relative, lang)
"""

import calendar  # For month/day calculations
import json  # For reading/writing JSON files
from datetime import date  # For working with dates
from dateutil import relativedelta  # For calculating date differences
from pathlib import Path  # For file path manipulations

# All user-facing messages. Extend this dict to add more languages.
MESSAGES = {
    "inputDay": {"ru": "Введите день", "en": "Enter a day"},
    "inputMonth": {"ru": "Введите месяц", "en": "Enter a month"},
    "inputYear": {"ru": "Введите год", "en": "Enter a year"},
    "selectOption": {"ru": "Выберите опцию", "en": "Select an option"},
    "useSavedDate": {"ru": "Использовать сохраненную дату", "en": "Use the saved date"},
    "enterNewDate": {"ru": "Ввести новую дату", "en": "Enter a new date"},
    "useTodaysDate": {"ru": "Использовать и сохранить сегодняшнюю дату", "en": "Use and save today's date"},
    "readingDate": {"ru": "Чтение даты из файла...", "en": "Reading date from file..."},
    "useThisDate": {"ru": "Использовать эту дату? (Нажмите Enter для подтверждения): ", "en": "Use this date? (Press Enter to confirm): "},
    "dateReadFromFile": {"ru": "Дата прочитана из файла:", "en": "Date read from file:"},
    "saveThisDate": {"ru": "Сохранить эту дату в файл? (Y/n): ", "en": "Save this date to file? (Y/n): "},
    "dateSaved": {"ru": "Дата сохранена в", "en": "Date saved to"},
    "errorLanguage": {"ru": "Ошибка ввода. Введите 'ru' или 'en'", "en": "Input error. Please enter 'ru' or 'en'"},
    "errorInt": {"ru": "Ошибка ввода.", "en": "Input error."},
    "inFuture": {"ru": "Введенная дата в будущем. Пожалуйста, введите корректную дату в прошлом", "en": "The entered date is in the future. Please enter a valid past date"},
    "errorReadingFile": {"ru": "Ошибка чтения файла.", "en": "Error reading date from file."},
    "enteredDate": {"ru": "Вы ввели дату", "en": "You entered the date"},
    "fileNotFound": {"ru": "Файл даты не найден", "en": "Date file not found."},
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


LOGO_ASCII = """
    S O B R I E T Y C O U N T E R
            NEW BEGINNING  ::  
+--------------------------------+
"""

# Where to store the saved date relative to the user's home directory
SETTING_PATH = ".config/sobriety_calculator/"
# Filename used to persist the date
SETTINGS_FILE = "date.json"

def input_int(prompt, min_value, max_value, lang="en"):
    """
    Prompt the user for an integer input within a specified range.
    Repeats until a valid integer in the range is entered.
    Styled for Linux terminal look.
    """
    while True:
        try:
            value = int(input(f"> {prompt} [{min_value}-{max_value}]: "))
            if min_value <= value <= max_value:
                return value
            # Out of allowed range
            print(f"! {MESSAGES['errorInt'][lang]}")
        except ValueError:
            # Non-integer input
            print(f"! {MESSAGES['errorInt'][lang]}")

def save_date_to_file(given_date: date, lang: str = "en") -> Path:
    """
    Save given_date to the settings file and return the file path.
    """
    # Ensure config directory exists, then write the date as JSON
    config_path = Path.home() / SETTING_PATH
    config_path.mkdir(parents=True, exist_ok=True)
    file_path = config_path / SETTINGS_FILE
    date_data = {
        "day": given_date.day,
        "month": given_date.month,
        "year": given_date.year,
    }
    with open(file_path, "w", encoding="utf-8") as file_to_save:
        json.dump(date_data, file_to_save)
    print(f"{MESSAGES['dateSaved'][lang]} {file_path}")
    return file_path

def choose_language():
    """
    Ask the user to choose a language (Russian or English).
    Defaults to English if input is invalid.
    Styled for Linux terminal look.
    """
    while True:
        lang = input("> Choose language [ru/en]: ").strip().lower()
        if lang not in ["ru", "en"]:
            # Always show this specific error in English so the prompt remains
            # understandable even if the user's input is malformed.
            print(f"! {MESSAGES['errorLanguage']['en']}")
        else:
            return lang

def input_date(lang="en"):
    """
    Prompt the user to enter a valid past date (day, month, year).
    Ensures the date is not in the future and the day is valid for the given month/year.
    """

    while True:
        month = input_int(MESSAGES["inputMonth"][lang], 1, 12, lang)
        year = input_int(MESSAGES["inputYear"][lang], 1900, date.today().year, lang)
        max_day = calendar.monthrange(year, month)[1]
        day = input_int(MESSAGES["inputDay"][lang], 1, max_day, lang)
        given_date = date(year, month, day)

        # Do not accept future dates
        if given_date >= date.today():
            print(MESSAGES["inFuture"][lang])
        else:
            # Show the parsed date in a compact format
            print(
                f"{MESSAGES['enteredDate'][lang]}: {MESSAGES['day'][lang]} {day:02d}, "
                f"{MESSAGES['month'][lang]} {month:02d}, {MESSAGES['year'][lang]} {year}"
            )

            # Ask whether the user wants to persist the date
            while True:
                is_save = input(MESSAGES['saveThisDate'][lang])
                if is_save.strip().lower() in ['y', 'yes', '']:
                    save_date_to_file(given_date, lang)
                    break
                if is_save.strip().lower().startswith('n'):
                    break

            return given_date


def get_date(lang="en"):
    """
    Get the date from a file if it exists, otherwise prompt the user for input.
    """
    config_path = Path.home() / SETTING_PATH
    file_path = config_path / SETTINGS_FILE
    if file_path.exists():
        # Try to read persisted date from JSON file
        print(MESSAGES['readingDate'][lang])
        with open(file_path, 'r', encoding='utf-8') as file_to_read:
            try:
                date_data = json.load(file_to_read)
            except json.JSONDecodeError:
                # If the file is corrupt offer to re-enter or use today's date
                print(MESSAGES['errorReadingFile'][lang] + "\n")
                print(f"1. {MESSAGES['enterNewDate'][lang]}")
                print(f"2. {MESSAGES['useTodaysDate'][lang]}")
                while True:
                    date_option = input("> ")
                    if date_option.strip() in ('1', '2'):
                        break
                    else:
                        print(f"! {MESSAGES['errorInt'][lang]}")
                if date_option.strip() == '1':
                    return input_date(lang)
                # option 2: save and return today's date
                today = date.today()
                save_date_to_file(today, lang)
                return today

        # If read successful, present the saved date and options
        print(
            f"{MESSAGES['dateReadFromFile'][lang]} {date_data['day']:02d}."
            f"{date_data['month']:02d}.{date_data['year']}"
        )
        # Selecting date for work
        print()
        print(f"1. {MESSAGES['useSavedDate'][lang]}")
        print(f"2. {MESSAGES['enterNewDate'][lang]}")
        print(f"3. {MESSAGES['useTodaysDate'][lang]}")
        while True:
            date_option = input("> ")
            if date_option.strip() in ('1', '2', '3'):
                break
            else:
                print(f"! {MESSAGES['errorInt'][lang]}")
        if date_option.strip() == '1':
            return date(date_data['year'], date_data['month'], date_data['day'])
        if date_option.strip() == '2':
            return input_date(lang)
        # option 3: use today's date and persist it
        today = date.today()
        save_date_to_file(today, lang)
        return today
    else:
        print(MESSAGES['fileNotFound'][lang] + "\n")
        print(f"1. {MESSAGES['enterNewDate'][lang]}")
        print(f"2. {MESSAGES['useTodaysDate'][lang]}")

        while True:
            date_option = input("> ")
            if date_option.strip() in ('1', '2'):
                break
            else:
                print(f"! {MESSAGES['errorInt'][lang]}")
        if date_option.strip() == '1':
            return input_date(lang)
        else:  # option 2
            today = date.today()
            save_date_to_file(today, lang)
            return today    

def calculate_sobriety_delta(given_date: date):
    """
    Calculates the difference in days and the relative difference in years/months/days
    between the given date and today.
    Returns a tuple: (total_days, relativedelta_object).
    """
    today = date.today()
    total_days = (today - given_date).days
    delta_relative = relativedelta.relativedelta(today, given_date)
    return total_days, delta_relative

# Format the output for the sobriety calculation result
def format_output(total_days, delta_relative, lang="en"):
    """
    Formats the result string using the correct language and grammar.
    Returns two strings: total days and relative difference (years, months, days).
    """
    diff = delta_relative
    # Format total days difference
    output_total_days = f"{MESSAGES['daysFrom'][lang]}: {total_days}"

    # Format relative difference (years, months, days)
    parts = []
    if diff.years > 0:
        parts.append(f"{diff.years} {MESSAGES['years'][lang]}")
    if diff.months > 0:
        parts.append(f"{diff.months} {MESSAGES['months'][lang]}")
    # Always show days if there are no years/months or if days > 0
    if diff.days > 0 or not parts:
        parts.append(f"{diff.days} {MESSAGES['days'][lang]}")

    if lang == "en":
        output_relative = ", ".join(parts)
        if len(parts) > 1:
            # Add 'and' before the last element
            last_item = parts[-1]
            all_but_last = parts[:-1]
            output_relative = f"{', '.join(all_but_last)} and {last_item}"
    elif lang == "ru":
        output_relative = ", ".join(parts)

    output_relative_final = f"{MESSAGES['whichIs'][lang]}: {output_relative}"
    return output_total_days, output_relative_final

def init():
    """
    Initialize any required settings or configurations.
    Currently a placeholder for future use.
    """
    # Print the small ASCII logo on startup
    print(LOGO_ASCII)
