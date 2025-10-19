Thanks! Here's your Markdown cleaned up and properly formatted for your `README.md` file. I’ve corrected indentation, code blocks, and section breaks so it renders beautifully on GitHub:

```markdown
# 🌱 Sobriety Calculator

A simple command-line tool to help you track your sobriety journey in English or Russian. It calculates the number of days since your quit date and displays your progress in years, months, and days.

---

## 🧰 Requirements

- Python 3.7 or newer  
- [`python-dateutil`](https://pypi.org/project/python-dateutil/) library

To install the dependency:
```bash
pip install python-dateutil
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/vladislav1975/Sobriety.git
cd Sobriety
```

### 2. Run the Program
```bash
python main.py
```

---

## 🗣️ Language Support

You can choose between:

- 🇬🇧 English  
- 🇷🇺 Russian  

The app will prompt you to select your preferred language at startup.

---

## 📅 Features

- Choose your sobriety start date manually or use today’s date  
- Automatically saves your date to a config file  
- Calculates:
  - Total days sober
  - Breakdown in years, months, and days  
- Friendly CLI interface with multilingual prompts  
- ASCII art banner for a motivational touch  

---

## 📂 Configuration

Your selected date is saved to:

```
~/.config/sobriety_calculator/date.json
```

This allows the app to remember your date across sessions.

---

## 🧪 Example Output

```
    S O B R I E T Y C O U N T E R
            NEW BEGINNING  ::  
+--------------------------------+
> Choose language [ru/en]: en
> Use the saved date
Days from the given date to today: 1234
Which is: 3 years, 4 months and 18 days
----------------------------------------
```

---

## 🛠️ Future Improvements

- GUI version  
- Milestone reminders  
- Export progress to CSV or JSON  

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues for suggestions or bugs.
```
