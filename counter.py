import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import json
import os
import calendar
import uuid

class TimeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Time Tracker")
        self.root.geometry("400x400")

        # Initialize project management
        self.projects_file = "projects.txt"
        self.time_records_file = "records.txt"
        self.project_data = {}  # Dict to store project data {id: (name, hotkey)}
        self.load_projects()
        
        # Set up key bindings for hotkeys
        self.root.bind('<KeyPress>', self.handle_hotkey)
        
        # Create session log file with current date-time
        current_date = datetime.now().strftime('%Y%m%d')
        current_time = datetime.now().strftime('%H%M%S')
        self.session_log = f"session_{current_date}_{current_time}.txt"
        
        self.current_project = None
        self.start_time = None
        self.is_tracking = False
        self.daily_records = self.load_records()

        # Create main frame for pages
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create preview page
        self.create_preview_page()

    def handle_hotkey(self, event):
        # Only handle number keys 1-9
        if not event.char.isdigit() or event.char == '0':
            return
            
        # Find project with this hotkey
        for pid, (name, hotkey) in self.project_data.items():
            if hotkey == event.char:
                if self.is_tracking:
                    # Stop current tracking
                    self.stop_timer()
                    
                # Switch to timer page if not already there
                if hasattr(self, 'preview_frame') and self.preview_frame.winfo_viewable():
                    self.show_timer_page()
                    
                # Select the project and start timer
                self.project_var.set(name)
                self.start_timer()
                break

    def create_preview_page(self):
        self.preview_frame = tk.Frame(self.main_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

        # Project list
        self.project_listbox = tk.Listbox(self.preview_frame, selectmode=tk.MULTIPLE)
        self.project_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.update_project_list()

        # Buttons frame
        button_frame = tk.Frame(self.preview_frame)
        button_frame.pack(pady=10)

        # Modify button
        modify_button = tk.Button(button_frame, text="Modify Projects", command=self.show_modify_dialog)
        modify_button.pack(side=tk.LEFT, padx=5)

        # Start button
        start_button = tk.Button(button_frame, text="Start Timer", command=self.show_timer_page)
        start_button.pack(side=tk.LEFT, padx=5)

    def update_project_list(self):
        self.project_listbox.delete(0, tk.END)
        for name, hotkey in self.project_data.values():
            self.project_listbox.insert(tk.END, f"({hotkey}){name}")

    def show_modify_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Modify Projects")
        dialog.geometry("300x400")

        # Project entry frame with name and hotkey
        entry_frame = tk.Frame(dialog)
        entry_frame.pack(pady=10, padx=10)
        
        # Project name entry
        name_frame = tk.Frame(entry_frame)
        name_frame.pack(fill=tk.X)
        tk.Label(name_frame, text="Project Name:").pack(side=tk.LEFT)
        project_entry = tk.Entry(name_frame)
        project_entry.pack(side=tk.LEFT, padx=5)
        
        # Hotkey entry
        hotkey_frame = tk.Frame(entry_frame)
        hotkey_frame.pack(fill=tk.X, pady=5)
        tk.Label(hotkey_frame, text="Hotkey (1-9):").pack(side=tk.LEFT)
        hotkey_entry = tk.Entry(hotkey_frame, width=5)
        hotkey_entry.pack(side=tk.LEFT, padx=5)

        # Add button with both name and hotkey
        tk.Button(entry_frame, text="Add Project", 
                 command=lambda: self.add_project(project_entry.get(), hotkey_entry.get(), dialog)).pack(pady=5)

        # Project list frame
        list_frame = tk.Frame(dialog)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Project list with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        project_list = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        project_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=project_list.yview)
        
        # Fill project list
        for name, hotkey in self.project_data.values():
            project_list.insert(tk.END, f"({hotkey}){name}")

        # Delete button
        tk.Button(list_frame, text="Delete Selected", 
                 command=lambda: self.delete_project(project_list.curselection(), project_list, dialog)).pack(pady=5)

    def add_project(self, project_name, hotkey, dialog):
        if not project_name:
            return
        
        # Validate hotkey
        if not hotkey or not hotkey.isdigit() or int(hotkey) < 1 or int(hotkey) > 9:
            return
            
        # Check if hotkey is already used
        for pid, (name, existing_hotkey) in self.project_data.items():
            if existing_hotkey == hotkey:
                return
            if name == project_name:
                return
        
        project_id = str(uuid.uuid4())
        self.project_data[project_id] = (project_name, hotkey)
        self.save_projects()
        self.update_project_list()
        dialog.destroy()
        self.show_modify_dialog()

    def delete_project(self, selections, project_list, dialog):
        if selections:
            # Get the selected project names
            selected_texts = [project_list.get(idx) for idx in selections]
            
            # Find and delete the corresponding project IDs
            for text in selected_texts:
                # Extract name from "(hotkey)name" format
                name = text[3:] if text.startswith('(') else text
                project_id = self.get_project_id_by_name(name)
                if project_id in self.project_data:
                    del self.project_data[project_id]
            
            self.save_projects()
            self.update_project_list()
            dialog.destroy()
            self.show_modify_dialog()

    def load_projects(self):
        try:
            if os.path.exists(self.projects_file):
                with open(self.projects_file, 'r') as f:
                    projects_data = [line.strip().split('|') for line in f.readlines()]
                    self.project_data = {}
                    for parts in projects_data:
                        if len(parts) == 3:  # id|name|hotkey format
                            pid, name, hotkey = parts
                            self.project_data[pid] = (name, hotkey)
                    if not self.project_data:
                        self.initialize_default_projects()
            else:
                self.initialize_default_projects()
        except (FileNotFoundError, ValueError):
            self.initialize_default_projects()

    def initialize_default_projects(self):
        default_projects = [("Project 1", "1"), ("Project 2", "2"), ("Project 3", "3")]
        self.project_data = {str(uuid.uuid4()): data for data in default_projects}
        self.save_projects()

    def save_projects(self):
        with open(self.projects_file, 'w') as f:
            for project_id, (name, hotkey) in self.project_data.items():
                f.write(f"{project_id}|{name}|{hotkey}\n")

    def get_project_id_by_name(self, project_name):
        for pid, (name, _) in self.project_data.items():
            if name == project_name:
                return pid
        return None

    def get_project_name_by_id(self, project_id):
        if project_id in self.project_data:
            return self.project_data[project_id][0]
        return None

    def show_preview_page(self):
        self.timer_frame.pack_forget()
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

    def load_records(self):
        try:
            if os.path.exists(self.time_records_file):
                records = {}
                with open(self.time_records_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) == 3:  # project_id|timestamp|seconds
                            project_id, timestamp, seconds = parts
                            if project_id not in records:
                                records[project_id] = []
                            records[project_id].append(float(timestamp))
                            records[project_id].append(int(seconds))
                
                # Filter for today's records only
                today_records = {pid: [] for pid in self.project_data.keys()}
                today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
                today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).timestamp()
                
                for project_id, times in records.items():
                    if project_id in self.project_data:
                        for i in range(0, len(times), 2):
                            if i + 1 < len(times):
                                timestamp = times[i]
                                if today_start <= timestamp <= today_end:
                                    today_records[project_id].append(times[i])
                                    today_records[project_id].append(times[i + 1])
                
                return today_records
        except (FileNotFoundError, ValueError):
            pass
        
        return {pid: [] for pid in self.project_data.keys()}

    def save_records(self):
        # Read existing records that aren't from today
        existing_records = []
        if os.path.exists(self.time_records_file):
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            with open(self.time_records_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        _, timestamp, _ = parts
                        if float(timestamp) < today_start:
                            existing_records.append(line.strip())

        # Write back old records and append today's records
        with open(self.time_records_file, 'w') as f:
            # Write old records
            for record in existing_records:
                f.write(record + '\n')
            
            # Write today's records
            for project_id, times in self.daily_records.items():
                for i in range(0, len(times), 2):
                    if i + 1 < len(times):
                        timestamp = times[i]
                        seconds = times[i + 1]
                        f.write(f"{project_id}|{timestamp}|{seconds}\n")

    def start_timer(self):
        project_name = self.project_var.get()
        project_id = self.get_project_id_by_name(project_name)
        if not self.is_tracking and project_id:
            self.current_project = project_id
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
            
            # Store timestamp and seconds using project ID
            if self.current_project not in self.daily_records:
                self.daily_records[self.current_project] = []
            self.daily_records[self.current_project].append(current_time)
            self.daily_records[self.current_project].append(total_seconds)
            self.save_records()
            
            # Save to session log file with project name and time
            project_name = self.get_project_name_by_id(self.current_project)
            with open(self.session_log, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} - {project_name}: {self.format_time(total_seconds)}\n")
            
            # Generate updated daily summary
            session_date = datetime.now().strftime('%Y%m%d')
            all_sessions_today = [f for f in os.listdir() if f.startswith(f'session_{session_date}')] # check later if this is working
            
            # Combine all sessions for today
            combined_times = {}
            for session_file in all_sessions_today:
                times = self.sum_session_times(session_file, generate_file=False)
                for project, seconds in times.items():
                    if project not in combined_times:
                        combined_times[project] = 0
                    combined_times[project] += seconds
            
            # Write daily summary
            with open(f"Daily_Summary_{session_date}.txt", 'w') as f: #Here is create the daily summary file
                for project_name in sorted(combined_times.keys()):
                    total_seconds = combined_times[project_name]
                    f.write(f"{project_name}: {self.format_time(total_seconds)}\n")
            
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

    def show_timer_page(self):
        # Hide preview frame
        self.preview_frame.pack_forget()
        
        # Create and show timer frame
        self.create_timer_page()

    def create_timer_page(self):
        self.timer_frame = tk.Frame(self.main_frame)
        self.timer_frame.pack(fill=tk.BOTH, expand=True)

        # Create new session log file when timer page is created
        current_date = datetime.now().strftime('%Y%m%d')
        current_time = datetime.now().strftime('%H%M%S')
        self.session_log = f"session_{current_date}_{current_time}.txt"

        # Project selection
        self.project_var = tk.StringVar()
        project_names = [name for name, _ in self.project_data.values()]
        self.project_dropdown = ttk.Combobox(self.timer_frame, textvariable=self.project_var, values=project_names)
        self.project_dropdown.set("Select Project")
        self.project_dropdown.pack(pady=20)

        # Timer display
        self.timer_label = tk.Label(self.timer_frame, text="00:00:00", font=("Arial", 24))
        self.timer_label.pack(pady=20)
        
        # Control buttons frame
        control_frame = tk.Frame(self.timer_frame)
        control_frame.pack(pady=10)
        
        # Start and Stop buttons in the same line
        self.start_button = tk.Button(control_frame, text="Start", command=self.start_timer, width=12)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED, width=12)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Bottom buttons frame
        bottom_frame = tk.Frame(self.timer_frame)
        bottom_frame.pack(pady=10)

        # Generate report and Back buttons
        self.report_button = tk.Button(bottom_frame, text="Day Report", command=self.generate_report, width=12)
        self.report_button.pack(side=tk.LEFT, padx=5)
        
        self.summary_button = tk.Button(bottom_frame, text="Month Report", command=self.generate_report, width=12)
        self.summary_button.pack(side=tk.LEFT, padx=5)


        self.report_button = tk.Button(bottom_frame, text="Month Report", command=self.generate_report, width=12)
        self.report_button.pack(side=tk.LEFT, padx=5)
        
        self.back_button = tk.Button(bottom_frame, text="Back to Projects", command=self.show_preview_page, width=12)
        self.back_button.pack(side=tk.LEFT, padx=5)

        # Initialize timer variables
        self.current_project = None
        self.start_time = None
        self.is_tracking = False
        self.daily_records = self.load_records()
        
        self.update_timer()

    def generate_report(self):
        if self.is_tracking:          # stop current timer first
            self.stop_timer()

        current_month = datetime.now().strftime('%Y%m')
        monthly_times = {}

        # pick all daily files whose *date* (the third chunk) starts with YYYYMM
        for fname in (f for f in os.listdir()
                    if f.startswith('Daily_Summary_')
                    and f.split('_')[-1][:6] == current_month):
            for project, secs in self.sum_session_times(fname, generate_file=False).items():
                monthly_times[project] = monthly_times.get(project, 0) + secs

        with open(f"Montly_Summary_{current_month}.txt", 'w') as f:
            for project in sorted(monthly_times):
                f.write(f"{project}: {self.format_time(monthly_times[project])}\n")


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
                    
                    project_name = parts[0]
                    if '(' in project_name:  # Handle "(hotkey)name" format
                        project_name = project_name[3:]  # Remove "(n)" prefix
                    time_str = parts[1]
                    
                    try:
                        h, m, s = map(int, time_str.split(':'))
                        seconds = h * 3600 + m * 60 + s
                        if project_name not in project_times:
                            project_times[project_name] = 0
                        project_times[project_name] += seconds
                    except ValueError:
                        continue
            
            if generate_file:
                # Generate daily summary report (overwrite if exists)
                session_date = session_file.split('_')[1]  # Extract date from filename
                summary_file = f"Daily_Summary_{session_date}.txt"
                
                with open(summary_file, 'w') as f:
                    for project_name in sorted(project_times.keys()):
                        total_seconds = project_times[project_name]
                        f.write(f"{project_name}: {self.format_time(total_seconds)}\n")
            
            return project_times
                    
        except FileNotFoundError:
            print(f"Session file {session_file} not found")
            return {}

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimeTracker()
    app.run()
