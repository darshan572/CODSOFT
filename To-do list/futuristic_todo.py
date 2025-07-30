#!/usr/bin/env python3
"""
🚀 CYBER TODO - Futuristic Task Manager
A beautiful, feature-rich Todo application with modern UI and animations
Author: AI Assistant
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import threading
import time
from typing import List, Dict, Optional
import uuid

class FuturisticTodo:
    def __init__(self):
        self.root = tk.Tk()
        self.tasks: List[Dict] = []
        self.current_filter = "all"
        self.search_query = ""
        self.data_file = "futuristic_todos.json"
        
        # Theme colors (Cyberpunk style)
        self.colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#111111',
            'bg_card': '#1a1a2e',
            'accent_cyan': '#00ffff',
            'accent_magenta': '#ff00ff',
            'accent_yellow': '#ffff00',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'success': '#00ff00',
            'warning': '#ff9500',
            'error': '#ff0040',
            'border': '#333333'
        }
        
        self.setup_window()
        self.create_styles()
        self.create_widgets()
        self.load_tasks()
        self.update_stats()
        self.add_welcome_tasks_if_empty()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🚀 CYBER TODO - Futuristic Task Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['bg_primary'])
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Configure window icon (if available)
        try:
            self.root.iconbitmap('rocket.ico')
        except:
            pass
            
    def create_styles(self):
        """Create custom styles for widgets"""
        self.style = ttk.Style()
        
        # Configure theme
        self.style.theme_use('clam')
        
        # Main frame style
        self.style.configure('Main.TFrame', 
                           background=self.colors['bg_primary'])
        
        # Header frame style
        self.style.configure('Header.TFrame',
                           background=self.colors['bg_card'],
                           relief='flat',
                           borderwidth=2)
        
        # Button styles
        self.style.configure('Cyber.TButton',
                           background=self.colors['accent_cyan'],
                           foreground=self.colors['bg_primary'],
                           font=('Arial', 10, 'bold'),
                           relief='flat',
                           borderwidth=0,
                           padding=(20, 10))
        
        self.style.map('Cyber.TButton',
                      background=[('active', self.colors['accent_magenta']),
                                ('pressed', self.colors['accent_yellow'])])
        
        # Entry styles
        self.style.configure('Cyber.TEntry',
                           fieldbackground=self.colors['bg_card'],
                           foreground=self.colors['text_primary'],
                           bordercolor=self.colors['accent_cyan'],
                           insertcolor=self.colors['accent_cyan'],
                           font=('Arial', 11))
        
        # Label styles
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['accent_cyan'],
                           font=('Arial', 24, 'bold'))
        
        self.style.configure('Stat.TLabel',
                           background=self.colors['bg_card'],
                           foreground=self.colors['text_primary'],
                           font=('Arial', 12, 'bold'))
        
        self.style.configure('StatValue.TLabel',
                           background=self.colors['bg_card'],
                           foreground=self.colors['accent_cyan'],
                           font=('Arial', 18, 'bold'))
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_frame)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Filter and search section
        self.create_filter_section(main_frame)
        
        # Tasks display section
        self.create_tasks_section(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Create the header with title and stats"""
        header_frame = ttk.Frame(parent, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.configure(padding=20)
        
        # Title with rocket emoji
        title_frame = ttk.Frame(header_frame, style='Header.TFrame')
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(title_frame, text="🚀 CYBER TODO", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, 
                                 text="Futuristic Task Management System",
                                 background=self.colors['bg_card'],
                                 foreground=self.colors['text_secondary'],
                                 font=('Arial', 10, 'italic'))
        subtitle_label.pack()
        
        # Stats section
        stats_frame = ttk.Frame(header_frame, style='Header.TFrame')
        stats_frame.pack(side=tk.RIGHT)
        
        self.stats_vars = {
            'total': tk.StringVar(value="0"),
            'completed': tk.StringVar(value="0"),
            'pending': tk.StringVar(value="0")
        }
        
        # Create stat boxes
        for i, (key, label) in enumerate([('total', 'TOTAL'), ('completed', 'COMPLETED'), ('pending', 'PENDING')]):
            stat_box = ttk.Frame(stats_frame, style='Header.TFrame')
            stat_box.grid(row=0, column=i, padx=10)
            
            value_label = ttk.Label(stat_box, textvariable=self.stats_vars[key], style='StatValue.TLabel')
            value_label.pack()
            
            label_widget = ttk.Label(stat_box, text=label, style='Stat.TLabel')
            label_widget.pack()
            
    def create_input_section(self, parent):
        """Create the task input section with date and time selection"""
        input_frame = ttk.Frame(parent, style='Main.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # First row - Task input and priority
        first_row = ttk.Frame(input_frame, style='Main.TFrame')
        first_row.pack(fill=tk.X, pady=(0, 10))
        
        # Task input
        self.task_var = tk.StringVar()
        task_entry = ttk.Entry(first_row, textvariable=self.task_var, 
                              style='Cyber.TEntry', font=('Arial', 12))
        task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority dropdown
        self.priority_var = tk.StringVar(value="Low")
        priority_combo = ttk.Combobox(first_row, textvariable=self.priority_var,
                                    values=["Low", "Medium", "High", "Critical"],
                                    state="readonly", width=10)
        priority_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add button
        add_btn = ttk.Button(first_row, text="🚀 DEPLOY MISSION", 
                           style='Cyber.TButton', command=self.add_task)
        add_btn.pack(side=tk.LEFT)
        
        # Second row - Date and time selection
        second_row = ttk.Frame(input_frame, style='Main.TFrame')
        second_row.pack(fill=tk.X)
        
        # Date selection frame
        date_frame = ttk.Frame(second_row, style='Main.TFrame')
        date_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        date_label = ttk.Label(date_frame, text="📅 Due Date:", 
                              background=self.colors['bg_primary'],
                              foreground=self.colors['accent_cyan'],
                              font=('Arial', 10, 'bold'))
        date_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Date selection with current date as default
        current_date = datetime.now()
        self.due_date_var = tk.StringVar(value=current_date.strftime("%Y-%m-%d"))
        
        # Date picker using dropdown menus for better UX
        date_picker_frame = ttk.Frame(date_frame, style='Main.TFrame')
        date_picker_frame.pack(side=tk.LEFT)
        
        # Year dropdown
        self.year_var = tk.StringVar(value=str(current_date.year))
        year_combo = ttk.Combobox(date_picker_frame, textvariable=self.year_var,
                                values=[str(y) for y in range(current_date.year, current_date.year + 5)],
                                state="readonly", width=6)
        year_combo.pack(side=tk.LEFT, padx=(0, 2))
        year_combo.bind('<<ComboboxSelected>>', self.update_date_string)
        
        # Month dropdown
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.month_var = tk.StringVar(value=current_date.strftime("%m"))
        month_combo = ttk.Combobox(date_picker_frame, textvariable=self.month_var,
                                 values=months, state="readonly", width=4)
        month_combo.pack(side=tk.LEFT, padx=(0, 2))
        month_combo.bind('<<ComboboxSelected>>', self.update_date_string)
        
        # Day dropdown
        self.day_var = tk.StringVar(value=current_date.strftime("%d"))
        days = [f"{d:02d}" for d in range(1, 32)]
        day_combo = ttk.Combobox(date_picker_frame, textvariable=self.day_var,
                               values=days, state="readonly", width=4)
        day_combo.pack(side=tk.LEFT, padx=(0, 5))
        day_combo.bind('<<ComboboxSelected>>', self.update_date_string)
        
        # Quick date buttons
        quick_date_frame = ttk.Frame(date_frame, style='Main.TFrame')
        quick_date_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        today_btn = tk.Button(quick_date_frame, text="Today",
                            command=lambda: self.set_quick_date(0),
                            bg=self.colors['accent_cyan'], fg=self.colors['bg_primary'],
                            relief='flat', padx=8, pady=2, font=('Arial', 8, 'bold'))
        today_btn.pack(side=tk.LEFT, padx=2)
        
        tomorrow_btn = tk.Button(quick_date_frame, text="Tomorrow",
                               command=lambda: self.set_quick_date(1),
                               bg=self.colors['accent_magenta'], fg=self.colors['bg_primary'],
                               relief='flat', padx=8, pady=2, font=('Arial', 8, 'bold'))
        tomorrow_btn.pack(side=tk.LEFT, padx=2)
        
        week_btn = tk.Button(quick_date_frame, text="Next Week",
                           command=lambda: self.set_quick_date(7),
                           bg=self.colors['accent_yellow'], fg=self.colors['bg_primary'],
                           relief='flat', padx=8, pady=2, font=('Arial', 8, 'bold'))
        week_btn.pack(side=tk.LEFT, padx=2)
        
        # Time selection frame
        time_frame = ttk.Frame(second_row, style='Main.TFrame')
        time_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        time_label = ttk.Label(time_frame, text="⏰ Due Time:", 
                              background=self.colors['bg_primary'],
                              foreground=self.colors['accent_cyan'],
                              font=('Arial', 10, 'bold'))
        time_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Time selection with current time as default
        current_time = datetime.now()
        
        # Hour dropdown
        self.hour_var = tk.StringVar(value=current_time.strftime("%H"))
        hours = [f"{h:02d}" for h in range(24)]
        hour_combo = ttk.Combobox(time_frame, textvariable=self.hour_var,
                                values=hours, state="readonly", width=4)
        hour_combo.pack(side=tk.LEFT, padx=(0, 2))
        
        time_sep1 = ttk.Label(time_frame, text=":", 
                             background=self.colors['bg_primary'],
                             foreground=self.colors['text_primary'],
                             font=('Arial', 12, 'bold'))
        time_sep1.pack(side=tk.LEFT)
        
        # Minute dropdown
        self.minute_var = tk.StringVar(value=current_time.strftime("%M"))
        minutes = [f"{m:02d}" for m in range(0, 60, 15)]  # 15-minute intervals
        minute_combo = ttk.Combobox(time_frame, textvariable=self.minute_var,
                                  values=minutes, state="readonly", width=4)
        minute_combo.pack(side=tk.LEFT, padx=(2, 5))
        
        # Quick time buttons
        quick_time_frame = ttk.Frame(time_frame, style='Main.TFrame')
        quick_time_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        now_btn = tk.Button(quick_time_frame, text="Now",
                          command=self.set_current_time,
                          bg=self.colors['success'], fg=self.colors['bg_primary'],
                          relief='flat', padx=8, pady=2, font=('Arial', 8, 'bold'))
        now_btn.pack(side=tk.LEFT, padx=2)
        
        eod_btn = tk.Button(quick_time_frame, text="EOD",
                          command=lambda: self.set_quick_time("17:00"),
                          bg=self.colors['warning'], fg=self.colors['bg_primary'],
                          relief='flat', padx=8, pady=2, font=('Arial', 8, 'bold'))
        eod_btn.pack(side=tk.LEFT, padx=2)
        
        # Initialize the date string
        self.update_date_string()
        
    def update_date_string(self, event=None):
        """Update the date string when dropdowns change"""
        try:
            year = self.year_var.get()
            month = self.month_var.get()
            day = self.day_var.get()
            if year and month and day:
                self.due_date_var.set(f"{year}-{month}-{day}")
        except:
            pass
            
    def set_quick_date(self, days_offset):
        """Set date to today + offset days"""
        target_date = datetime.now() + timedelta(days=days_offset)
        self.year_var.set(str(target_date.year))
        self.month_var.set(target_date.strftime("%m"))
        self.day_var.set(target_date.strftime("%d"))
        self.update_date_string()
        
    def set_current_time(self):
        """Set time to current time"""
        current_time = datetime.now()
        self.hour_var.set(current_time.strftime("%H"))
        self.minute_var.set(current_time.strftime("%M"))
        
    def set_quick_time(self, time_str):
        """Set time to specified time (HH:MM format)"""
        hour, minute = time_str.split(":")
        self.hour_var.set(hour)
        self.minute_var.set(minute)
        
    def create_filter_section(self, parent):
        """Create filters and search"""
        filter_frame = ttk.Frame(parent, style='Main.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Filter buttons
        filter_buttons_frame = ttk.Frame(filter_frame, style='Main.TFrame')
        filter_buttons_frame.pack(side=tk.LEFT)
        
        self.filter_buttons = {}
        filters = [("all", "ALL MISSIONS"), ("pending", "PENDING"), 
                  ("completed", "COMPLETED"), ("high", "HIGH PRIORITY")]
        
        for filter_key, filter_text in filters:
            btn = tk.Button(filter_buttons_frame, text=filter_text,
                          command=lambda f=filter_key: self.set_filter(f),
                          bg=self.colors['bg_card'], fg=self.colors['text_secondary'],
                          relief='flat', padx=15, pady=8, font=('Arial', 9, 'bold'))
            btn.pack(side=tk.LEFT, padx=5)
            self.filter_buttons[filter_key] = btn
            
        # Highlight active filter
        self.filter_buttons["all"].configure(bg=self.colors['accent_cyan'], 
                                           fg=self.colors['bg_primary'])
        
        # Search box
        search_frame = ttk.Frame(filter_frame, style='Main.TFrame')
        search_frame.pack(side=tk.RIGHT)
        
        search_label = ttk.Label(search_frame, text="🔍", 
                               background=self.colors['bg_primary'],
                               foreground=self.colors['accent_cyan'],
                               font=('Arial', 12))
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                               style='Cyber.TEntry', width=20)
        search_entry.pack(side=tk.LEFT)
        search_entry.bind('<KeyRelease>', self.on_search)
        
    def create_tasks_section(self, parent):
        """Create the tasks display area"""
        tasks_frame = ttk.Frame(parent, style='Main.TFrame')
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create canvas for scrolling
        canvas = tk.Canvas(tasks_frame, bg=self.colors['bg_primary'], 
                          highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(tasks_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.tasks_container = self.scrollable_frame
        
    def create_status_bar(self, parent):
        """Create status bar with action buttons"""
        status_frame = ttk.Frame(parent, style='Main.TFrame')
        status_frame.pack(fill=tk.X)
        
        # Theme toggle
        theme_btn = tk.Button(status_frame, text="🌙 DARK MODE",
                            command=self.toggle_theme,
                            bg=self.colors['accent_magenta'], fg=self.colors['bg_primary'],
                            relief='flat', padx=15, pady=5, font=('Arial', 9, 'bold'))
        theme_btn.pack(side=tk.LEFT)
        
        # Export button
        export_btn = tk.Button(status_frame, text="📤 EXPORT",
                             command=self.export_tasks,
                             bg=self.colors['accent_yellow'], fg=self.colors['bg_primary'],
                             relief='flat', padx=15, pady=5, font=('Arial', 9, 'bold'))
        export_btn.pack(side=tk.LEFT, padx=10)
        
        # Import button
        import_btn = tk.Button(status_frame, text="📥 IMPORT",
                             command=self.import_tasks,
                             bg=self.colors['accent_cyan'], fg=self.colors['bg_primary'],
                             relief='flat', padx=15, pady=5, font=('Arial', 9, 'bold'))
        import_btn.pack(side=tk.LEFT)
        
        # Clear all button
        clear_btn = tk.Button(status_frame, text="🗑️ CLEAR ALL",
                            command=self.clear_all_tasks,
                            bg=self.colors['error'], fg=self.colors['text_primary'],
                            relief='flat', padx=15, pady=5, font=('Arial', 9, 'bold'))
        clear_btn.pack(side=tk.RIGHT)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready for missions! 🚀")
        status_label = ttk.Label(status_frame, textvariable=self.status_var,
                               background=self.colors['bg_primary'],
                               foreground=self.colors['text_secondary'],
                               font=('Arial', 10))
        status_label.pack(side=tk.RIGHT, padx=20)
        
    def add_task(self):
        """Add a new task with date and time"""
        task_text = self.task_var.get().strip()
        if not task_text:
            messagebox.showerror("Error", "Please enter a task!")
            return
            
        # Parse due date and time
        due_datetime = None
        try:
            # Get date components
            year = self.year_var.get()
            month = self.month_var.get()
            day = self.day_var.get()
            hour = self.hour_var.get()
            minute = self.minute_var.get()
            
            if year and month and day:
                # Create datetime object
                due_datetime = datetime(
                    int(year), int(month), int(day),
                    int(hour) if hour else 23,
                    int(minute) if minute else 59
                )
                due_datetime = due_datetime.isoformat()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date/time: {str(e)}")
            return
        
        task = {
            'id': str(uuid.uuid4()),
            'text': task_text,
            'completed': False,
            'priority': self.priority_var.get().lower(),
            'due_date': due_datetime,
            'due_time': f"{self.hour_var.get()}:{self.minute_var.get()}" if self.hour_var.get() and self.minute_var.get() else None,
            'created_at': datetime.now().isoformat(),
            'notes': ''
        }
        
        self.tasks.insert(0, task)
        self.save_tasks()
        self.render_tasks()
        self.update_stats()
        
        # Clear inputs and reset to current date/time
        self.task_var.set("")
        self.priority_var.set("Low")
        self.reset_datetime_to_current()
        
        self.show_status("Mission added successfully! 🚀", success=True)
        
    def reset_datetime_to_current(self):
        """Reset date and time to current values"""
        current = datetime.now()
        self.year_var.set(str(current.year))
        self.month_var.set(current.strftime("%m"))
        self.day_var.set(current.strftime("%d"))
        self.hour_var.set(current.strftime("%H"))
        self.minute_var.set(current.strftime("%M"))
        self.update_date_string()
        
    def toggle_task(self, task_id):
        """Toggle task completion status"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                task['completed_at'] = datetime.now().isoformat() if task['completed'] else None
                break
                
        self.save_tasks()
        self.render_tasks()
        self.update_stats()
        
        status = "Mission completed! 🎉" if task['completed'] else "Mission reopened! 🔄"
        self.show_status(status, success=True)
        
    def delete_task(self, task_id):
        """Delete a task"""
        if messagebox.askyesno("Confirm", "Delete this mission?"):
            self.tasks = [t for t in self.tasks if t['id'] != task_id]
            self.save_tasks()
            self.render_tasks()
            self.update_stats()
            self.show_status("Mission deleted! 🗑️")
            
    def edit_task(self, task_id):
        """Edit a task with enhanced date/time dialog"""
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if not task:
            return
            
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("🛠️ Edit Mission")
        edit_window.geometry("500x450")
        edit_window.configure(bg=self.colors['bg_card'])
        edit_window.resizable(False, False)
        
        # Center the dialog
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Main frame with scrollbar
        main_frame = tk.Frame(edit_window, bg=self.colors['bg_card'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Task text
        tk.Label(main_frame, text="Mission:", bg=self.colors['bg_card'], 
                fg=self.colors['text_primary'], font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0,5))
        
        text_var = tk.StringVar(value=task['text'])
        text_entry = tk.Entry(main_frame, textvariable=text_var, width=60,
                            bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                            insertbackground=self.colors['accent_cyan'], font=('Arial', 11))
        text_entry.pack(fill=tk.X, pady=(0,15))
        
        # Priority
        tk.Label(main_frame, text="Priority:", bg=self.colors['bg_card'], 
                fg=self.colors['text_primary'], font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0,5))
        
        priority_var = tk.StringVar(value=task['priority'].capitalize())
        priority_combo = ttk.Combobox(main_frame, textvariable=priority_var,
                                    values=["Low", "Medium", "High", "Critical"],
                                    state="readonly", width=15)
        priority_combo.pack(anchor='w', pady=(0,15))
        
        # Date and Time section
        datetime_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        datetime_frame.pack(fill=tk.X, pady=(0,15))
        
        tk.Label(datetime_frame, text="Due Date & Time:", bg=self.colors['bg_card'], 
                fg=self.colors['text_primary'], font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0,5))
        
        # Parse existing due date/time
        current_datetime = datetime.now()
        if task.get('due_date'):
            try:
                current_datetime = datetime.fromisoformat(task['due_date'])
            except:
                pass
        
        # Date selection
        date_frame = tk.Frame(datetime_frame, bg=self.colors['bg_card'])
        date_frame.pack(anchor='w', pady=(0,5))
        
        tk.Label(date_frame, text="📅 Date:", bg=self.colors['bg_card'], 
                fg=self.colors['accent_cyan'], font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0,5))
        
        edit_year_var = tk.StringVar(value=str(current_datetime.year))
        year_combo = ttk.Combobox(date_frame, textvariable=edit_year_var,
                                values=[str(y) for y in range(current_datetime.year, current_datetime.year + 5)],
                                state="readonly", width=6)
        year_combo.pack(side=tk.LEFT, padx=2)
        
        edit_month_var = tk.StringVar(value=current_datetime.strftime("%m"))
        month_combo = ttk.Combobox(date_frame, textvariable=edit_month_var,
                                 values=[f"{m:02d}" for m in range(1, 13)],
                                 state="readonly", width=4)
        month_combo.pack(side=tk.LEFT, padx=2)
        
        edit_day_var = tk.StringVar(value=current_datetime.strftime("%d"))
        day_combo = ttk.Combobox(date_frame, textvariable=edit_day_var,
                               values=[f"{d:02d}" for d in range(1, 32)],
                               state="readonly", width=4)
        day_combo.pack(side=tk.LEFT, padx=2)
        
        # Time selection
        time_frame = tk.Frame(datetime_frame, bg=self.colors['bg_card'])
        time_frame.pack(anchor='w', pady=(0,10))
        
        tk.Label(time_frame, text="⏰ Time:", bg=self.colors['bg_card'], 
                fg=self.colors['accent_cyan'], font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0,5))
        
        edit_hour_var = tk.StringVar(value=current_datetime.strftime("%H"))
        hour_combo = ttk.Combobox(time_frame, textvariable=edit_hour_var,
                                values=[f"{h:02d}" for h in range(24)],
                                state="readonly", width=4)
        hour_combo.pack(side=tk.LEFT, padx=2)
        
        tk.Label(time_frame, text=":", bg=self.colors['bg_card'], 
                fg=self.colors['text_primary'], font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        edit_minute_var = tk.StringVar(value=current_datetime.strftime("%M"))
        minute_combo = ttk.Combobox(time_frame, textvariable=edit_minute_var,
                                  values=[f"{m:02d}" for m in range(0, 60, 15)],
                                  state="readonly", width=4)
        minute_combo.pack(side=tk.LEFT, padx=(2,10))
        
        # Quick datetime buttons
        quick_btn_frame = tk.Frame(time_frame, bg=self.colors['bg_card'])
        quick_btn_frame.pack(side=tk.LEFT, padx=(10,0))
        
        def set_edit_now():
            now = datetime.now()
            edit_year_var.set(str(now.year))
            edit_month_var.set(now.strftime("%m"))
            edit_day_var.set(now.strftime("%d"))
            edit_hour_var.set(now.strftime("%H"))
            edit_minute_var.set(now.strftime("%M"))
        
        now_btn = tk.Button(quick_btn_frame, text="Now",
                          command=set_edit_now,
                          bg=self.colors['success'], fg=self.colors['bg_primary'],
                          relief='flat', padx=6, pady=2, font=('Arial', 8, 'bold'))
        now_btn.pack(side=tk.LEFT, padx=1)
        
        def set_edit_tomorrow():
            tomorrow = datetime.now() + timedelta(days=1)
            edit_year_var.set(str(tomorrow.year))
            edit_month_var.set(tomorrow.strftime("%m"))
            edit_day_var.set(tomorrow.strftime("%d"))
        
        tomorrow_btn = tk.Button(quick_btn_frame, text="Tomorrow",
                               command=set_edit_tomorrow,
                               bg=self.colors['accent_magenta'], fg=self.colors['bg_primary'],
                               relief='flat', padx=6, pady=2, font=('Arial', 8, 'bold'))
        tomorrow_btn.pack(side=tk.LEFT, padx=1)
        
        # Notes
        tk.Label(main_frame, text="Notes:", bg=self.colors['bg_card'], 
                fg=self.colors['text_primary'], font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0,5))
        
        notes_text = tk.Text(main_frame, height=4, width=60,
                           bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                           insertbackground=self.colors['accent_cyan'], font=('Arial', 10))
        notes_text.pack(fill=tk.X, pady=(0,20))
        notes_text.insert('1.0', task.get('notes', ''))
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        btn_frame.pack(fill=tk.X)
        
        def save_changes():
            try:
                # Create new datetime
                new_datetime = datetime(
                    int(edit_year_var.get()),
                    int(edit_month_var.get()),
                    int(edit_day_var.get()),
                    int(edit_hour_var.get()),
                    int(edit_minute_var.get())
                )
                
                task['text'] = text_var.get().strip()
                task['priority'] = priority_var.get().lower()
                task['due_date'] = new_datetime.isoformat()
                task['due_time'] = f"{edit_hour_var.get()}:{edit_minute_var.get()}"
                task['notes'] = notes_text.get('1.0', tk.END).strip()
                task['updated_at'] = datetime.now().isoformat()
                
                self.save_tasks()
                self.render_tasks()
                self.update_stats()
                edit_window.destroy()
                self.show_status("Mission updated successfully! ✨", success=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
        
        save_btn = tk.Button(btn_frame, text="💾 SAVE CHANGES", command=save_changes,
                           bg=self.colors['success'], fg=self.colors['bg_primary'],
                           relief='flat', padx=20, pady=8, font=('Arial', 10, 'bold'))
        save_btn.pack(side=tk.LEFT, padx=(0,10))
        
        cancel_btn = tk.Button(btn_frame, text="❌ CANCEL", command=edit_window.destroy,
                             bg=self.colors['error'], fg=self.colors['text_primary'],
                             relief='flat', padx=20, pady=8, font=('Arial', 10, 'bold'))
        cancel_btn.pack(side=tk.LEFT)
        
    def render_tasks(self):
        """Render all tasks in the display area"""
        # Clear existing tasks
        for widget in self.tasks_container.winfo_children():
            widget.destroy()
            
        filtered_tasks = self.get_filtered_tasks()
        
        if not filtered_tasks:
            # Show empty state
            empty_frame = tk.Frame(self.tasks_container, bg=self.colors['bg_primary'])
            empty_frame.pack(fill=tk.X, pady=50)
            
            empty_label = tk.Label(empty_frame, text="🚀 No missions found\nCreate your first task to get started!",
                                 bg=self.colors['bg_primary'], fg=self.colors['text_secondary'],
                                 font=('Arial', 14), justify=tk.CENTER)
            empty_label.pack()
            return
            
        # Render tasks
        for i, task in enumerate(filtered_tasks):
            self.create_task_widget(task, i)
            
    def create_task_widget(self, task, index):
        """Create a widget for a single task"""
        # Task container
        task_frame = tk.Frame(self.tasks_container, bg=self.colors['bg_card'], 
                            relief='solid', bd=1)
        task_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Priority color indicator
        priority_colors = {
            'low': self.colors['success'],
            'medium': self.colors['warning'],
            'high': self.colors['error'],
            'critical': self.colors['error']
        }
        
        priority_indicator = tk.Frame(task_frame, bg=priority_colors.get(task['priority'], self.colors['success']),
                                    width=5, height=1)
        priority_indicator.pack(side=tk.LEFT, fill=tk.Y)
        
        # Main content
        content_frame = tk.Frame(task_frame, bg=self.colors['bg_card'])
        content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        
        # Task text
        text_color = self.colors['text_secondary'] if task['completed'] else self.colors['text_primary']
        task_text = task['text']
        if task['completed']:
            task_text = f"✅ {task_text}"
        
        text_label = tk.Label(content_frame, text=task_text, bg=self.colors['bg_card'],
                            fg=text_color, font=('Arial', 12, 'bold'), anchor='w')
        text_label.pack(fill=tk.X)
        
        # Meta info
        meta_info = []
        meta_info.append(f"Priority: {task['priority'].upper()}")
        
        if task['due_date']:
            try:
                due_datetime = datetime.fromisoformat(task['due_date'])
                due_date_str = due_datetime.strftime("%Y-%m-%d")
                due_time_str = due_datetime.strftime("%H:%M")
                is_overdue = due_datetime < datetime.now() and not task['completed']
                due_color = self.colors['error'] if is_overdue else self.colors['text_secondary']
                
                # Show both date and time
                meta_info.append(f"Due: {due_date_str} at {due_time_str}")
                
                # Add overdue indicator if applicable
                if is_overdue:
                    meta_info.append("⚠️ OVERDUE")
            except:
                # Fallback for old format
                due_date = datetime.fromisoformat(task['due_date']).strftime("%Y-%m-%d")
                meta_info.append(f"Due: {due_date}")
        
        created_date = datetime.fromisoformat(task['created_at']).strftime("%m/%d %H:%M")
        meta_info.append(f"Created: {created_date}")
        
        meta_label = tk.Label(content_frame, text=" | ".join(meta_info),
                            bg=self.colors['bg_card'], fg=self.colors['text_secondary'],
                            font=('Arial', 9), anchor='w')
        meta_label.pack(fill=tk.X)
        
        # Action buttons
        actions_frame = tk.Frame(task_frame, bg=self.colors['bg_card'])
        actions_frame.pack(side=tk.RIGHT, padx=10)
        
        # Complete button
        complete_text = "✅" if not task['completed'] else "🔄"
        complete_btn = tk.Button(actions_frame, text=complete_text,
                               command=lambda: self.toggle_task(task['id']),
                               bg=self.colors['success'], fg=self.colors['bg_primary'],
                               relief='flat', width=3, font=('Arial', 12))
        complete_btn.pack(side=tk.TOP, pady=2)
        
        # Edit button
        edit_btn = tk.Button(actions_frame, text="✏️",
                           command=lambda: self.edit_task(task['id']),
                           bg=self.colors['accent_cyan'], fg=self.colors['bg_primary'],
                           relief='flat', width=3, font=('Arial', 12))
        edit_btn.pack(side=tk.TOP, pady=2)
        
        # Delete button
        delete_btn = tk.Button(actions_frame, text="🗑️",
                             command=lambda: self.delete_task(task['id']),
                             bg=self.colors['error'], fg=self.colors['text_primary'],
                             relief='flat', width=3, font=('Arial', 12))
        delete_btn.pack(side=tk.TOP, pady=2)
        
    def get_filtered_tasks(self):
        """Get tasks based on current filter and search"""
        filtered = self.tasks.copy()
        
        # Apply search filter
        if self.search_query:
            filtered = [t for t in filtered if 
                       self.search_query in t['text'].lower() or 
                       self.search_query in t.get('notes', '').lower()]
        
        # Apply category filter
        if self.current_filter == 'pending':
            filtered = [t for t in filtered if not t['completed']]
        elif self.current_filter == 'completed':
            filtered = [t for t in filtered if t['completed']]
        elif self.current_filter == 'high':
            filtered = [t for t in filtered if t['priority'] in ['high', 'critical']]
        
        # Sort by priority and creation date
        priority_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        
        def sort_key(task):
            priority_val = priority_order.get(task['priority'], 1)
            created_date = datetime.fromisoformat(task['created_at'])
            return (-priority_val, -created_date.timestamp())
        
        return sorted(filtered, key=sort_key)
    
    def set_filter(self, filter_key):
        """Set the current filter"""
        # Reset all button colors
        for key, btn in self.filter_buttons.items():
            btn.configure(bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
        
        # Highlight active filter
        self.filter_buttons[filter_key].configure(bg=self.colors['accent_cyan'], 
                                                fg=self.colors['bg_primary'])
        
        self.current_filter = filter_key
        self.render_tasks()
        
    def on_search(self, event=None):
        """Handle search input"""
        self.search_query = self.search_var.get().lower()
        self.render_tasks()
        
    def clear_placeholder(self, event):
        """Clear placeholder text in date entry"""
        if event.widget.get() == "YYYY-MM-DD":
            event.widget.delete(0, tk.END)
            
    def update_stats(self):
        """Update statistics display"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        self.stats_vars['total'].set(str(total))
        self.stats_vars['completed'].set(str(completed))
        self.stats_vars['pending'].set(str(pending))
        
    def show_status(self, message, success=False):
        """Show status message"""
        self.status_var.set(message)
        # Reset status after 3 seconds
        self.root.after(3000, lambda: self.status_var.set("Ready for missions! 🚀"))
        
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
            
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
                self.render_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            
    def add_welcome_tasks_if_empty(self):
        """Add welcome tasks if no tasks exist"""
        if not self.tasks:
            # Create welcome tasks with specific times to showcase the feature
            tomorrow_9am = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
            next_week_5pm = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0) + timedelta(days=7)
            today_eod = datetime.now().replace(hour=17, minute=30, second=0, microsecond=0)
            
            welcome_tasks = [
                {
                    'id': str(uuid.uuid4()),
                    'text': 'Welcome to your Futuristic Todo App! 🚀',
                    'completed': False,
                    'priority': 'high',
                    'due_date': next_week_5pm.isoformat(),
                    'due_time': '17:00',
                    'created_at': datetime.now().isoformat(),
                    'notes': 'This is your first mission with date & time! Notice how the due date shows both date and time. You can edit, complete, or delete tasks using the action buttons.'
                },
                {
                    'id': str(uuid.uuid4()),
                    'text': 'Test the new Date & Time selection feature',
                    'completed': False,
                    'priority': 'medium',
                    'due_date': tomorrow_9am.isoformat(),
                    'due_time': '09:00',
                    'created_at': (datetime.now() - timedelta(minutes=1)).isoformat(),
                    'notes': 'Try adding a new task and notice the improved date/time selection with dropdowns and quick buttons!'
                },
                {
                    'id': str(uuid.uuid4()),
                    'text': 'Experience the enhanced edit dialog',
                    'completed': False,
                    'priority': 'critical',
                    'due_date': today_eod.isoformat(),
                    'due_time': '17:30',
                    'created_at': (datetime.now() - timedelta(minutes=2)).isoformat(),
                    'notes': 'Click the edit button (✏️) on any task to see the new date/time selection interface with quick-set buttons!'
                },
                {
                    'id': str(uuid.uuid4()),
                    'text': 'Explore quick date/time buttons',
                    'completed': True,
                    'priority': 'low',
                    'due_date': None,
                    'created_at': (datetime.now() - timedelta(minutes=3)).isoformat(),
                    'notes': 'You can use Today, Tomorrow, Next Week buttons for dates and Now, EOD buttons for times.'
                }
            ]
            
            self.tasks = welcome_tasks
            self.save_tasks()
            self.render_tasks()
            
    def export_tasks(self):
        """Export tasks to JSON file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Tasks"
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.tasks, f, indent=2)
                self.show_status(f"Tasks exported to {filename}! 📤", success=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export tasks: {str(e)}")
            
    def import_tasks(self):
        """Import tasks from JSON file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Import Tasks"
            )
            
            if filename:
                with open(filename, 'r') as f:
                    imported_tasks = json.load(f)
                
                if isinstance(imported_tasks, list):
                    self.tasks = imported_tasks
                    self.save_tasks()
                    self.render_tasks()
                    self.update_stats()
                    self.show_status(f"Tasks imported from {filename}! 📥", success=True)
                else:
                    messagebox.showerror("Error", "Invalid file format!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import tasks: {str(e)}")
            
    def clear_all_tasks(self):
        """Clear all tasks"""
        if messagebox.askyesno("Confirm", "Clear all missions? This cannot be undone!"):
            self.tasks = []
            self.save_tasks()
            self.render_tasks()
            self.update_stats()
            self.show_status("All missions cleared! 🗑️")
            
    def toggle_theme(self):
        """Toggle between dark and light themes (placeholder)"""
        self.show_status("Theme toggle feature coming soon! 🌙✨")
        
    def run(self):
        """Start the application"""
        # Add keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.task_var.set("") or None)
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: (self.load_tasks(), self.render_tasks(), self.update_stats()))
        
        # Start the main loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

def main():
    """Main function to run the application"""
    print("🚀 Starting CYBER TODO - Futuristic Task Manager")
    print("=" * 50)
    print("Features:")
    print("• ✨ Beautiful cyberpunk-themed interface")
    print("• 🎯 Priority levels (Low, Medium, High, Critical)")
    print("• 📅 Due date tracking with overdue alerts")
    print("• 🔍 Real-time search and filtering")
    print("• 💾 Automatic data persistence")
    print("• 📤📥 Export/Import functionality")
    print("• ⌨️  Keyboard shortcuts:")
    print("  - Ctrl+N: New task")
    print("  - Ctrl+Q: Quit")
    print("  - F5: Refresh")
    print("=" * 50)
    
    app = FuturisticTodo()
    app.run()

if __name__ == "__main__":
    main()
