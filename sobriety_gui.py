import tkinter as tk
import json
from datetime import date
from pathlib import Path
# Импортируем только математику расчёта, без интерактивных функций ввода
from sobriety_calculator import calculate_sobriety_delta, format_output, SETTING_PATH, SETTINGS_FILE

def load_date_gui():
    """Тихое чтение даты для GUI без использования терминала"""
    config_path = Path.home() / SETTING_PATH
    file_path = config_path / SETTINGS_FILE
    
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                date_data = json.load(file)
                return date(date_data['year'], date_data['month'], date_data['day'])
        except Exception:
            # Если файл поврежден, возвращаем сегодня
            return date.today()
    else:
        # Если файла нет, возвращаем сегодня
        return date.today()

def main():
    lang = "ru"
    
    # Загружаем дату без вопросов в консоли
    given_date = load_date_gui()
    
    # Считаем дни
    total_days, delta_relative = calculate_sobriety_delta(given_date)
    output_days, output_relative = format_output(total_days, delta_relative, lang)

    # Создаем окно
    window = tk.Tk()
    window.title("Калькулятор трезвости")
    window.geometry("400x120")

    full_text = f"{output_days}\n{output_relative}"

    label = tk.Label(window, text=full_text, font=("Arial", 11), justify="center")
    label.pack(pady=25)

    window.mainloop()

if __name__ == "__main__":
    main()