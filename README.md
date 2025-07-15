# Project Time Tracker

A simple desktop application built with Python that helps you track time spent on different projects. Perfect for freelancers, students, or anyone who needs to monitor time spent on various tasks.

## What Does It Do?

- **Track Time by Project:** Assign unique IDs to projects and log hours automatically
- **Live Timer:** See a running timer while you work
- **Human‑Readable Logs:** All session data saved to text files
- **Daily & Monthly Summaries:** Generate reports for any day or month
- **Simple UI:** Built with Tkinter for quick setup and easy use

## Getting Started

### First‑Time Setup (Complete Beginner’s Guide)

### ▶️ Without Python (Standalone Executable)

> No Python install needed

1. Extract `WindowsProgram.zip`
2. **Windows:** Double‑click `TicoCounter.exe`
3. **Mac/Linux:**
   ```bash
   cd path/to/extracted
   chmod +x AutoCounter 
   ./AutoCounter
   ```

1. **Install Python** (One‑time only):

   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download the latest version and **Run Installer**
   - ✅ **Check** “Add Python to PATH”
   - Click **Install Now**

2. **Download Project Files**:

   - **Option A:** Clone or download ZIP from this repo
   - **Option B:** Download the **Standalone Build** (no Python required)
   - Extract ZIP to a folder of your choice

## Running the Application

### ▶️ With Python Installed

#### Windows

1. Open PowerShell (Shift + Right‑click → **Open PowerShell** here)
2. `cd` into project folder:
   ```powershell
   cd "D:\Projects\AutoCounter"
   ```
3. Launch:
   ```powershell
   python counter.py
   ```

#### Mac/Linux

1. Open Terminal
2. Change directory:
   ```bash
   cd path/to/AutoCounter
   ```
3. Launch:
   ```bash
   python3 counter.py
   ```

4. The app UI opens immediately

## How to Use

1. **Manage Projects**

   - **Modify Projects** page to add/remove entries
   - Each project has a unique **ID**

2. **Track Time**

   - **Start Timer** → select project → **Start** → **Stop** when done
   - Timer shows **HH\:MM****:SS**

3. **View Reports**

   - **Day Summary:** `Day_Summary_YYYYMMDD.txt`
   - **Monthly Summary:** Click **Generate Report** → `Month_Summary_YYYYMM.txt`

## Files Used by the App

- **projects.txt**

  > Stores `project_id|project_name`

- **records.txt**

  > Stores `project_id|timestamp|seconds`

- **session\_YYYYMMDD\_HHMMSS.txt**

  > Logs each start/stop event per run

- **Day\_Summary\_YYYYMMDD.txt**

  > Auto-generated daily totals

- **Month\_Summary\_YYYYMM.txt**

  > Generated on demand via **Generate Report**

## Common Issues & Solutions

1. **"Python is not recognized..."**\
   Reinstall Python with **Add to PATH** enabled.

2. **"No module named tkinter"**

   - **Windows:** Reinstall Python and include **tcl/tk and IDLE**
   - **Linux:** `sudo apt-get install python3-tk`
   - **Mac:** Use Python.org installer (avoid Homebrew version)

3. **Timer window hidden**\
   Bring it to front or restart the app.

4. **Standalone EXE won’t launch**

   - **Windows:** Right‑click → **Run as administrator**
   - **Mac/Linux:** Ensure file is executable (`chmod +x AutoCounter`)

## Questions?

- Check your Python installation
- Verify you’re in the correct directory
- Restart terminal or computer

---

> Feel free to customize **counter.py**! It uses **Tkinter**, **datetime**, and simple file I/O for storage.