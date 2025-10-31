# To-Do List Manager
A powerful, feature-rich command-line to-do list manager built with Python. This app uses Rich for colorful terminal UI, Matplotlib for progress charts, and TinyDB for task storage. It supports task urgency levels, motivational messages, statistics, search, and optional email reporting.

## Features
- Colorful CLI interface using Rich library
- Add, view, delete tasks with urgency (low, medium, high)
- Mark tasks complete or pending
- Search tasks by keyword or urgency
- View detailed statistics on task progress
- Weekly and monthly progress charts with Matplotlib
- Customizable settings including dark mode and email SMTP
- Motivational slogans to boost productivity
- Cross-platform support: Windows, macOS, Linux, Android-Termux, iOS (a-Shell/iSH)
- Handles Unicode issues on Windows CMD for clear output

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/username/todo-list-manager.git
   cd todo-list-manager
   ```

2. Create and activate a Python 3.8+ virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Start the app using:
```
python main.py
```
- Follow the on-screen menu to add tasks, mark completion, view statistics, and more.
- Configure user profile and email settings through the settings menu to enable monthly report emails.
- Use arrow keys and number inputs for smooth navigation.
- Motivational messages will be shown to encourage productivity.

## Configuration
- Settings are saved in `settings.json`.
- Tasks are saved in `tasks.json`.
- Unicode display issues on Windows CMD are addressed automatically.
- Customize settings via the settings menu in the app.

## Contribution
Contributions, issues, and feature requests are welcome!  
Please fork the repository and submit a pull request with descriptive commit messages.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- [Rich](https://github.com/Textualize/rich) for terminal rendering
- [Matplotlib](https://matplotlib.org/) for charts
- [TinyDB](https://tinydb.readthedocs.io/en/latest/) for lightweight JSON database
