# Project Time Tracker

A simple desktop application built with Python and Tkinter that helps you track time spent on different projects.

## Features

- Track time for multiple projects
- Real-time timer display in HH:MM:SS format
- Session-based logging of time entries
- Daily summary reports
- Automatic saving of time records
- Clean and simple user interface

## How It Works

1. **Project Selection**: Choose a project from the dropdown menu
2. **Time Tracking**: 
   - Click "Start" to begin tracking time for the selected project
   - Click "Stop" to end the tracking session
   - The timer displays the current session duration in HH:MM:SS format

3. **Time Logging**:
   - Each session is automatically logged to a dated session file (e.g., `session_20250523_134928.txt`)
   - Log entries include timestamp and duration
   - Format: `YYYY-MM-DD HH:MM:SS - Project Name: HH:MM:SS`

4. **Generate Reports**:
   - Click "Generate Report" to create a summary of all time tracked for the current day
   - Reports are saved as `Time_Summary_YYYYMMDD_HHMMSS.txt`
   - Shows total time spent on each project

## Files Generated

- `session_[datetime].txt`: Individual session logs with detailed timestamps
- `Time_Summary_[datetime].txt`: Daily summary reports of total time per project
- `time_records.json`: Data storage file for the application

## Requirements

- Python 3.x
- tkinter (usually comes with Python)

## Installation

1. Clone this repository:
```powershell
git clone https://github.com/[your-username]/AutoCounter.git
```

2. Navigate to the project directory:
```powershell
cd AutoCounter
```

3. Run the application:
```powershell
python counter.py
```

## Usage

1. Start the application
2. Select a project from the dropdown menu
3. Click "Start" to begin tracking time
4. Click "Stop" when you're done with the task
5. Generate a daily summary report using the "Generate Report" button

## Sample Output

### Session Log (session_20250523_134928.txt):
```
2025-05-23 13:51:25 - Project 1: 00:00:20
2025-05-23 13:51:39 - Project 1: 00:00:08
```

### Summary Report (Time_Summary_20250523_135142.txt):
```
Project 1: 00:03:08
Project 2: 00:00:32
Project 3: 00:00:48
Project 4: 00:00:00
Project 5: 00:00:39
```

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements!
