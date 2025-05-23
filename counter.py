import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import json
import os

class TimeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Time Tracker")
        self.root.geometry("400x400")

        # Initialize project management
        self.projects_file = "projects.txt"
        self.time_records_file = "time_records.json"
        self.project_data = {}  # Dict to store project data {id: name}
        self.load_projects()
        
        # Create main frame for pages
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create preview page
        self.create_preview_page()

    def load_projects(self):
        try:
            if os.path.exists(self.projects_file):
                with open(self.projects_file, 'r') as f:
                    projects_data = [line.strip().split('|') for line in f.readlines()]
                    self.project_data = {pid: name for pid, name in projects_data if pid and name}
                    if not self.project_data:
                        self.initialize_default_projects()
            else:
                self.initialize_default_projects()
        except (FileNotFoundError, ValueError):
            self.initialize_default_projects()

    def initialize_default_projects(self):
        import uuid
        default_projects = ["Project 1", "Project 2", "Project 3"]
        self.project_data = {str(uuid.uuid4()): name for name in default_projects}
        self.save_projects()

    def save_projects(self):
        with open(self.projects_file, 'w') as f:
            for project_id, name in self.project_data.items():
                f.write(f"{project_id}|{name}\n")

    def get_project_id_by_name(self, project_name):
        for pid, name in self.project_data.items():
            if name == project_name:
                return pid
        return None

    def get_project_name_by_id(self, project_id):
        return self.project_data.get(project_id)
        
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
        for name in self.project_data.values():
            self.project_listbox.insert(tk.END, name)

    def show_modify_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Modify Projects")
        dialog.geometry("300x400")

        # Project entry
        entry_frame = tk.Frame(dialog)
        entry_frame.pack(pady=10, padx=10)
        
        tk.Label(entry_frame, text="Project Name:").pack()
        project_entry = tk.Entry(entry_frame)
        project_entry.pack(pady=5)

        # Buttons
        tk.Button(entry_frame, text="Add Project", 
                 command=lambda: self.add_project(project_entry.get(), dialog)).pack(pady=5)

        # Project list
        list_frame = tk.Frame(dialog)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        project_list = tk.Listbox(list_frame)
        project_list.pack(fill=tk.BOTH, expand=True)
        
        for project in self.projects:
            project_list.insert(tk.END, project)

        # Delete button
        tk.Button(list_frame, text="Delete Selected", 
                 command=lambda: self.delete_project(project_list.curselection(), dialog)).pack(pady=5)

    def add_project(self, project_name, dialog):
        if project_name and project_name not in self.project_data.values():
            import uuid
            project_id = str(uuid.uuid4())
            self.project_data[project_id] = project_name
            self.save_projects()
            self.update_project_list()
            dialog.destroy()
            self.show_modify_dialog()

    def delete_project(self, selections, dialog):
        if selections:
            indices = list(selections)
            indices.sort(reverse=True)
            project_ids = list(self.project_data.keys())
            for idx in indices:
                if idx < len(project_ids):
                    del self.project_data[project_ids[idx]]
            self.save_projects()
            self.update_project_list()
            dialog.destroy()
            self.show_modify_dialog()

    def show_timer_page(self):
        # Hide preview frame
        self.preview_frame.pack_forget()
        
        # Create and show timer frame
        self.create_timer_page()

    def create_timer_page(self):
        self.timer_frame = tk.Frame(self.main_frame)
        self.timer_frame.pack(fill=tk.BOTH, expand=True)

        # Create new session log file when timer page is created
        self.session_log = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        # Project selection
        self.project_var = tk.StringVar()
        self.project_dropdown = ttk.Combobox(self.timer_frame, textvariable=self.project_var, 
                                           values=list(self.project_data.values()))
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

        # Generate report and Back buttons in the same line
        self.report_button = tk.Button(bottom_frame, text="Generate Report", command=self.generate_report, width=12)
        self.report_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(bottom_frame, text="Back to Projects", command=self.show_preview_page, width=12)
        self.back_button.pack(side=tk.LEFT, padx=5)

        # Initialize timer variables
        self.current_project = None
        self.start_time = None
        self.is_tracking = False
        self.daily_records = self.load_records()
        
        self.update_timer()

    def show_preview_page(self):
        self.timer_frame.pack_forget()
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

    def load_records(self):
        try:
            if os.path.exists(self.time_records_file):
                with open(self.time_records_file, 'r') as f:
                    all_records = json.load(f)
                
                # Create a new dictionary for today's records
                today_records = {pid: [] for pid in self.project_data.keys()}
                today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
                today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).timestamp()
                
                # Only copy times from today to the new records
                for project_id, times in all_records.items():
                    if project_id in self.project_data:  # Check by ID instead of name
                        for i in range(0, len(times), 2):
                            if i + 1 < len(times):
                                timestamp = times[i]
                                if today_start <= timestamp <= today_end:
                                    today_records[project_id].append(times[i])
                                    today_records[project_id].append(times[i + 1])
                
                return today_records
        except FileNotFoundError:
            pass
        
        return {pid: [] for pid in self.project_data.keys()}

    def is_from_today(self, timestamp):
        today = datetime.now().date()
        return datetime.fromtimestamp(timestamp).date() == today

    def save_records(self):
        with open('time_records.json', 'w') as f:
            json.dump(self.daily_records, f)

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
            
            # Save to session log file with project name
            project_name = self.get_project_name_by_id(self.current_project)
            with open(self.session_log, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} - {project_name}: {self.format_time(total_seconds)}\n")
            
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
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).timestamp()
            
            for project_id, times in self.daily_records.items():
                project_name = self.get_project_name_by_id(project_id)
                if not project_name:
                    continue
                    
                # Get durations for timestamps within today
                today_times = [times[i+1] for i in range(0, len(times), 2) 
                             if i+1 < len(times) and today_start <= times[i] <= today_end]
                total_seconds = sum(today_times) if today_times else 0
                f.write(f"{project_name}: {self.format_time(total_seconds)}\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimeTracker()
    app.run()
