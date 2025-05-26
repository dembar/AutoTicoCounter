# Project Time Tracker

A simple desktop application built with Python that helps you track time spent on different projects. Perfect for freelancers, students, or anyone who needs to monitor time spent on various tasks.

## What Does It Do?

- Track how much time you spend on different projects using unique project IDs
- Show a live timer while you're working
- Save detailed logs of your work sessions in text files
- Create daily and monthly summaries of your time
- Simple, easy-to-use interface with project management
- All data stored in human-readable text files

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
1. Open PowerShell (several ways to do this):
   - Press `Windows + X` and select "Windows PowerShell" or "Terminal"
   - Hold Shift + Right-click in the project folder and choose "Open PowerShell window here"
   - Open PowerShell and navigate to your project folder using:
     ```powershell
     cd "d:\Projects\AutoCounter"  # Replace with your actual path
     ```

2. Run the application:
   ```powershell
   python counter.py
   ```

3. The application will create these files automatically:
   - `projects.txt`: Stores your project list
   - `records.txt`: Stores your time records
   - `session_*.txt`: Daily session logs
   - `Session_Summary_*.txt`: Daily summaries
   - `Time_Summary_*.txt`: Monthly summaries

#### Mac/Linux:
1. Open Terminal
2. Navigate to the project folder:
   ```bash
   cd path/to/AutoCounter
   ```
3. Run the application:
   ```bash
   python3 counter.py
   ```

## How to Use

1. **Project Management**
   - When you first run the app, you'll see the project list page
   - Click "Modify Projects" to add or remove projects
   - Each project gets a unique ID to track its time accurately

2. **Start Tracking Time**
   - Click "Start Timer" to go to the timer page
   - Select a project from the dropdown menu
   - Click "Start" to begin timing
   - The timer shows hours:minutes:seconds
   - Click "Stop" when you're done

3. **View Reports**
   - "Session Summary": Shows time tracked in the current session
   - "Generate Report": Creates a monthly summary of all projects
   - Click "Back to Projects" to return to the project list

4. **File Organization**
   - All data is stored in human-readable text files
   - Session logs are created automatically
   - Daily summaries update when you stop timing
   - Monthly reports are generated on demand

## Files Used by the App

1. **Project Data** (`projects.txt`)
   - Stores project information
   - Format: `project_id|project_name`
   - Created automatically with default projects
   - Updated when you add/remove projects

2. **Time Records** (`records.txt`)
   - Stores all time tracking data
   - Format: `project_id|timestamp|seconds`
   - Automatically maintains daily records

3. **Session Files** (`session_YYYYMMDD_HHMMSS.txt`)
   - Created each time you start tracking
   - Contains human-readable entries like:
   ```
   2025-05-24 20:15:25 - Project 1: 00:10:20
   2025-05-24 20:25:39 - Project 2: 00:15:08
   ```

4. **Daily Summary** (`Session_Summary_YYYYMMDD.txt`)
   - One file per day
   - Shows total time per project for the day
   ```
   Project 1: 00:45:30
   Project 2: 01:15:20
   ```

5. **Monthly Summary** (`Time_Summary_YYYYMM.txt`)
   - One file per month
   - Shows total time per project for the entire month
   - Generated when you click "Generate Report"

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
