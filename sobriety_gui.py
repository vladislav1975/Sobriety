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
    given_date = load_date_gui()
    
    total_days, delta_relative = calculate_sobriety_delta(given_date)
    output_days, output_relative = format_output(total_days, delta_relative, lang)

    window = tk.Tk()
    
    # --- МАГИЯ ВИДЖЕТА ---
    # 1. Убираем системную рамку и заголовок окна
    window.overrideredirect(True)
    
    # 2. Задаем размер и положение на экране (Ширина x Высота + Отступ_X + Отступ_Y)
    # Например, разместим окошко в правом верхнем углу экрана
    window.geometry("350x90+1000+50")
    
    # 3. Красим фон окна в приятный темно-серый цвет (как в терминале)
    window.configure(bg="#2d2d2d")
    # ---------------------

    full_text = f"{output_days}\n{output_relative}"

    # Настраиваем текст: делаем его белым (fg), а фон — темно-серым (bg) в тон окну
    label = tk.Label(
        window, 
        text=full_text, 
        font=("Arial", 11, "bold"), 
        justify="center",
        fg="#ffffff",
        bg="#2d2d2d"
    )
    label.pack(pady=20)

    # Поскольку кнопок закрытия больше нет, добавим выход из виджета по двойному клику мыши
    window.bind("<Double-Button-1>", lambda event: window.destroy())

    window.mainloop()
if __name__ == "__main__":
    main()