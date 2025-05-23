import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import json
import os

class TimeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Time Tracker")
        self.root.geometry("400x300")

        # Create session log file with current date-time
        self.session_log = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        self.projects = ["Project 1", "Project 2", "Project 3", "Project 4", "Project 5"]
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

        # Generate report button
        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_button.pack(pady=10)

        self.update_timer()

    def load_records(self):
        today = datetime.now().strftime('%Y-%m-%d')
        try:
            if os.path.exists('time_records.json'):
                with open('time_records.json', 'r') as f:
                    all_records = json.load(f)
                # Check if we have a new day, if so clear the records
                if not any(self.is_from_today(t) for times in all_records.values() for t in times):
                    return {project: [] for project in self.projects}
                return all_records
        except FileNotFoundError:
            return {project: [] for project in self.projects}

    def is_from_today(self, timestamp):
        today = datetime.now().date()
        return datetime.fromtimestamp(timestamp).date() == today

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
            self.daily_records[self.current_project].append(current_time)
            self.daily_records[self.current_project].append(total_seconds)
            self.save_records()
            
            # Save to session log file with hh:mm:ss format
            with open(self.session_log, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} - {self.current_project}: {self.format_time(total_seconds)}\n")
            
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
            
        # Generate the summary report
        with open(f"Time_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
            for project in self.projects:
                times = self.daily_records[project]
                # Every even index is a timestamp, odd index is duration
                today_times = [times[i+1] for i in range(0, len(times), 2) if self.is_from_today(times[i])]
                total_seconds = sum(today_times) if today_times else 0
                f.write(f"{project}: {self.format_time(total_seconds)}\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimeTracker()
    app.run()