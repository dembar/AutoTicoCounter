import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import json
import os
import calendar

class TimeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Time Tracker")
        self.root.geometry("400x350")  # Made window slightly taller

        # Initialize project management
        self.projects_file = "projects.txt"
        self.load_projects()
        
        # Create session log file with current date-time
        current_date = datetime.now().strftime('%Y%m%d')
        current_time = datetime.now().strftime('%H%M%S')
        self.session_log = f"session_{current_date}_{current_time}.txt"
        
        self.current_project = None
        self.start_time = None
        self.is_tracking = False
        self.daily_records = self.load_records()

        # Project selection
        self.project_var = tk.StringVar()
        self.project_dropdown = ttk.Combobox(self.root, textvariable=self.project_var, values=self.projects)
        self.project_dropdown.set("Select Project")
        self.project_dropdown.pack(pady=20)

        # Timer display
        self.timer_label = tk.Label(self.root, text="00:00:00", font=("Arial", 24))
        self.timer_label.pack(pady=20)

        # Control buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Report buttons frame
        report_frame = tk.Frame(self.root)
        report_frame.pack(pady=5)
        
        # Generate report button
        self.report_button = tk.Button(report_frame, text="Generate Report", command=self.generate_report)
        self.report_button.pack(side=tk.LEFT, padx=5)
        
        # Session summary button
        self.summary_button = tk.Button(report_frame, text="Session Summary", 
                                      command=lambda: self.sum_session_times(self.session_log))
        self.summary_button.pack(side=tk.LEFT, padx=5)

        self.update_timer()

    def load_projects(self):
        try:
            with open(self.projects_file, 'r') as f:
                self.projects = [line.strip() for line in f.readlines()]
                if not self.projects:  # If file is empty, add default projects
                    self.projects = ["Project 1", "Project 2", "Project 3"]
                    self.save_projects()
        except FileNotFoundError:
            self.projects = ["Project 1", "Project 2", "Project 3"]
            self.save_projects()

    def save_projects(self):
        with open(self.projects_file, 'w') as f:
            f.write('\n'.join(self.projects))

    def load_records(self):
        try:
            if os.path.exists('time_records.json'):
                with open('time_records.json', 'r') as f:
                    all_records = json.load(f)
                return all_records
        except FileNotFoundError:
            pass
        return {project: [] for project in self.projects}

    def save_records(self):
        with open('time_records.json', 'w') as f:
            json.dump(self.daily_records, f)

    def start_timer(self):
        if not self.is_tracking and self.project_var.get() in self.projects:
            self.current_project = self.project_var.get()
            self.start_time = datetime.now()
            self.is_tracking = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.project_dropdown.config(state=tk.DISABLED)

    def stop_timer(self):
        if self.is_tracking:
            duration = datetime.now() - self.start_time
            total_seconds = int(duration.total_seconds())
            current_time = datetime.now().timestamp()
            
            # Store timestamp and seconds
            if self.current_project not in self.daily_records:
                self.daily_records[self.current_project] = []
            self.daily_records[self.current_project].append(current_time)
            self.daily_records[self.current_project].append(total_seconds)
            self.save_records()
            
            # Save to session log file with hh:mm:ss format
            with open(self.session_log, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} - {self.current_project}: {self.format_time(total_seconds)}\n")
            
            # Generate updated daily summary
            session_date = datetime.now().strftime('%Y%m%d')
            all_sessions_today = [f for f in os.listdir() if f.startswith(f'session_{session_date}')]
            
            # Combine all sessions for today
            combined_times = {}
            for session_file in all_sessions_today:
                times = self.sum_session_times(session_file, generate_file=False)
                for project, seconds in times.items():
                    if project not in combined_times:
                        combined_times[project] = 0
                    combined_times[project] += seconds
            
            # Write daily summary
            with open(f"Session_Summary_{session_date}.txt", 'w') as f:
                for project in sorted(combined_times.keys()):
                    total_seconds = combined_times[project]
                    f.write(f"{project}: {self.format_time(total_seconds)}\n")
            
            self.is_tracking = False
            self.start_time = None
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.project_dropdown.config(state=tk.NORMAL)
            self.timer_label.config(text="00:00:00")

    def update_timer(self):
        if self.is_tracking and self.start_time:
            duration = datetime.now() - self.start_time
            total_seconds = int(duration.total_seconds())
            self.timer_label.config(text=self.format_time(total_seconds))
        self.root.after(1000, self.update_timer)

    def format_time(self, seconds):
        # Convert total seconds to hours, minutes, seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_report(self):
        # If timer is running, stop it first
        if self.is_tracking:
            self.stop_timer()
            
        # Generate the monthly summary report
        current_month = datetime.now().strftime('%Y%m')
        monthly_summary_file = f"Time_Summary_{current_month}.txt"
        
        # Get all session files for this month
        session_files = [f for f in os.listdir() if f.startswith('session_') and f.split('_')[1][:6] == current_month]
        
        # Aggregate all times for the month
        monthly_times = {}
        for session_file in session_files:
            project_times = self.sum_session_times(session_file, generate_file=False)
            for project, seconds in project_times.items():
                if project not in monthly_times:
                    monthly_times[project] = 0
                monthly_times[project] += seconds
        
        # Write monthly summary
        with open(monthly_summary_file, 'w') as f:
            for project in sorted(monthly_times.keys()):
                total_seconds = monthly_times[project]
                f.write(f"{project}: {self.format_time(total_seconds)}\n")

    def sum_session_times(self, session_file, generate_file=True):
        """Sum times for each project from a session log file"""
        project_times = {}  # Dictionary to store total seconds per project
        
        try:
            with open(session_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    # Split the line into timestamp, project and time
                    if " - " in line:
                        _, rest = line.strip().split(" - ", 1)
                    else:
                        rest = line.strip()
                    
                    parts = rest.split(': ')
                    if len(parts) != 2:
                        continue
                    
                    project = parts[0]
                    time_str = parts[1]
                    
                    try:
                        h, m, s = map(int, time_str.split(':'))
                        seconds = h * 3600 + m * 60 + s
                        if project not in project_times:
                            project_times[project] = 0
                        project_times[project] += seconds
                    except ValueError:
                        continue
            
            if generate_file:
                # Generate daily summary report (overwrite if exists)
                session_date = session_file.split('_')[1]  # Extract date from filename
                summary_file = f"Session_Summary_{session_date}.txt"
                
                with open(summary_file, 'w') as f:
                    for project in sorted(project_times.keys()):
                        total_seconds = project_times[project]
                        f.write(f"{project}: {self.format_time(total_seconds)}\n")
            
            return project_times
                    
        except FileNotFoundError:
            print(f"Session file {session_file} not found")
            return {}

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimeTracker()
    app.run()