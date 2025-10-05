# Импортируем только то, что нам нужно, из модуля
from sobriety_calculator import (
    chooseLanguage,
    inputDate,
    calculate_sobriety_delta,
    format_output,
    MESSAGES
)

def main():   
    """
    Основная функция для запуска калькулятора.
    """
    # 1. Установка языка и ввод даты
    lang = chooseLanguage()
    given_date = inputDate(lang)
    day, month, year = given_date.day, given_date.month, given_date.year

    print("-" * 40)
    print(f"{MESSAGES['enteredDate'][lang]}: {day:02d}.{month:02d}.{year}")

    # 2. Вычисления (вызывается функция модуля)
    total_days, delta_relative = calculate_sobriety_delta(given_date)

    # 3. Форматирование и вывод (вызывается функция модуля)
    output_days, output_relative = format_output(total_days, delta_relative, lang)
    
    print(output_days)
    print(output_relative)
    print("-" * 40)


if __name__ == "__main__":
    main()