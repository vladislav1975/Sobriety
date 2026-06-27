import tkinter as tk
import json
from datetime import date
from pathlib import Path
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
            return date.today()
    else:
        return date.today()

# --- ЛОГИКА ПЕРЕТАСКИВАНИЯ ОКНА ---
# Создаем простой словарь для хранения координат
drag_data = {"x": 0, "y": 0}

def start_drag(event):
    """Запоминаем начальные координаты мыши при клике"""
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def drag_window(event, window):
    """Вычисляем сдвиг и перемещаем окно"""
    deltax = event.x - drag_data["x"]
    deltay = event.y - drag_data["y"]
    new_x = window.winfo_x() + deltax
    new_y = window.winfo_y() + deltay
    window.geometry(f"+{new_x}+{new_y}")
# ----------------------------------

def main():
    lang = "ru"
    given_date = load_date_gui()
    
    total_days, delta_relative = calculate_sobriety_delta(given_date)
    output_days, output_relative = format_output(total_days, delta_relative, lang)

    window = tk.Tk()
    window.overrideredirect(True)
    
    # Стартовая позиция виджета
    window.geometry("260x35+870+2")
    window.configure(bg="#2d2d2d")

    full_text = f"{output_days}\n{output_relative}"

    label = tk.Label(
        window, 
        text=full_text, 
        font=("Arial", 9, "bold"), 
        justify="center",
        fg="#ffffff",
        bg="#2d2d2d"
    )
    label.pack(pady=1)

    # --- ОБНОВЛЕННАЯ ПРИВЯЗКА СОБЫТИЙ МЫШИ ---
    # Теперь мы не передаем window в start_drag, так как используем глобальный drag_data
    window.bind("<Button-1>", start_drag)
    label.bind("<Button-1>", start_drag)

    # В drag_window по-прежнему передаем window, чтобы знать, какое окно двигать
    window.bind("<B1-Motion>", lambda event: drag_window(event, window))
    label.bind("<B1-Motion>", lambda event: drag_window(event, window))

    # Двойной клик для закрытия
    window.bind("<Double-Button-1>", lambda event: window.destroy())
    label.bind("<Double-Button-1>", lambda event: window.destroy())

    window.mainloop()

if __name__ == "__main__":
    main()