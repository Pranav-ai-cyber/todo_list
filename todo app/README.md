# Ultimate To-Do List Manager
A feature-rich, cross-platform command-line to-do list application built with Python. This app uses Rich for beautiful terminal output, matplotlib for progress charts, and TinyDB for task storage, designed for productivity and motivation.

## Features
- Colorful and interactive CLI with Rich library
- Manage tasks with add, view, complete, pending, delete, and search capabilities
- Set task urgency levels: low, medium, high
- Track task progress with weekly and monthly charts using matplotlib
- Motivational quotes and progress stats displayed dynamically
- Email monthly reports (configurable SMTP settings)
- Cross-platform support: Windows, macOS, Linux, Android-Termux, iOS (a-Shell/iSH)
- Settings for dark mode, user profile, and notifications
- Handles Unicode properly in Windows CMD

## Installation
1. Ensure Python 3.8+ is installed.
2. Clone this repository:
   ```
   git clone https://github.com/username/todo-list-manager.git
   ```
3. Navigate into the project folder:
   ```
   cd todo-list-manager
   ```
4. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the main program:
```
python main.py
```
Follow the on-screen menus to add tasks, view lists, mark completion, and view statistics. Configure email and profile settings from the Settings menu.

## File Overview
- `main.py` - Main program entry and menu handling
- `gui.py` - User interface and display logic using Rich and matplotlib
- `task.py` - Task class with properties and methods
- `config\settings.json` - User configuration and preferences
- `TODO.md` - Project notes and known issues

## Contributions
Contributions are welcome! Please fork the repository and submit pull requests for bug fixes, new features, or improvements.

## License
This project is licensed under the MIT License.