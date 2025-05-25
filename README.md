# Project Time Tracker

A simple desktop application that helps you track time spent on different projects. Perfect for freelancers, students, or anyone who needs to monitor time spent on various tasks.

## What Does It Do?

- Track how much time you spend on different projects
- Show a live timer while you're working
- Save detailed logs of your work sessions
- Create daily and monthly summaries of your time
- Simple, easy-to-use interface

## Getting Started

### First Time Setup (Complete Beginner's Guide)

1. **Install Python** (One-time setup):
   - Go to [Python's official website](https://www.python.org/downloads/)
   - Click the big "Download Python" button (get the latest version)
   - Run the installer you downloaded
   - ⚠️ Important: Check "Add Python to PATH" during installation
   - Click Install Now

2. **Get the Project Files**:
   - Download this project (green "Code" button → "Download ZIP")
   - Extract the ZIP file to a folder on your computer
   - Remember where you put it!

### Running the Application

#### Windows:
1. Open the folder where you extracted the files
2. Hold Shift + Right-click in the folder
3. Choose "Open PowerShell window here"
4. Type this command and press Enter:
```powershell
python counter.py
```

#### Mac/Linux:
1. Open Terminal
2. Navigate to the project folder (use 'cd' command)
3. Run the application:
```bash
python3 counter.py
```

## How to Use

1. **Start the App**
   - When the app opens, you'll see a dropdown menu with project names
   - The big timer display shows 00:00:00

2. **Track Time**
   - Pick a project from the dropdown
   - Click "Start" to begin timing
   - The timer will show how long you've been working
   - Click "Stop" when you're done

3. **View Reports**
   - "Session Summary": Shows total time for each project today
   - "Generate Report": Creates a monthly summary

## Files Created by the App

1. **Session Files** (`session_YYYYMMDD_HHMMSS.txt`)
   - Created each time you start tracking
   - Contains detailed entries like:
   ```
   2025-05-24 20:15:25 - Project 1: 00:10:20
   2025-05-24 20:25:39 - Project 2: 00:15:08
   ```

2. **Daily Summary** (`Session_Summary_YYYYMMDD.txt`)
   - One file per day
   - Shows total time per project for the day
   ```
   Project 1: 00:45:30
   Project 2: 01:15:20
   ```

3. **Monthly Summary** (`Time_Summary_YYYYMM.txt`)
   - One file per month
   - Shows total time per project for the entire month

## Common Issues & Solutions

1. **"Python is not recognized..."**
   - Solution: Reinstall Python and make sure to check "Add Python to PATH"

2. **"No module named tkinter"**
   - Windows: Reinstall Python and select "tcl/tk and IDLE" during installation
   - Linux: Run `sudo apt-get install python3-tk`
   - Mac: Use Python from python.org, not Homebrew

3. **Can't see the timer window**
   - Check if it opened behind other windows
   - Try closing and reopening the application

## Questions?

If you run into problems:
1. Make sure Python is installed correctly
2. Try closing and reopening your terminal/PowerShell
3. Make sure you're in the right folder when running the command

## Want to Modify the App?

The main program is in `counter.py`. It's written in Python and uses:
- Tkinter for the window and buttons
- Basic file operations for saving data
- datetime for time calculations

Feel free to modify it for your needs!
