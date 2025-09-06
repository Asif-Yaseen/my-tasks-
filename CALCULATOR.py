import tkinter as tk
from tkinter import ttk, messagebox, font
import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_colors()
        self.setup_fonts()
        self.tasks = []
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("Modern To-Do List")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
    def setup_colors(self):
        # Modern color palette
        self.colors = {
            'bg_primary': '#2C3E50',      # Dark blue-gray
            'bg_secondary': '#34495E',     # Slightly lighter blue-gray
            'accent': '#3498DB',           # Bright blue
            'accent_hover': '#2980B9',     # Darker blue
            'success': '#27AE60',          # Green
            'danger': '#E74C3C',           # Red
            'warning': '#F39C12',          # Orange
            'text_primary': '#FFFFFF',     # White
            'text_secondary': '#BDC3C7',   # Light gray
            'completed': '#95A5A6',        # Gray for completed tasks
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
    def setup_fonts(self):
        self.fonts = {
            'title': ('Segoe UI', 18, 'bold'),
            'heading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'task': ('Segoe UI', 11),
        }
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📝 My To-Do List",
            font=self.fonts['title'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(pady=(0, 20))
        
        # Date display
        today = datetime.date.today().strftime("%B %d, %Y")
        date_label = tk.Label(
            main_frame,
            text=today,
            font=self.fonts['body'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        date_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Task entry
        self.task_var = tk.StringVar()
        self.task_entry = tk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=self.fonts['body'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            relief='flat',
            bd=0,
            highlightthickness=2,
            highlightcolor=self.colors['accent'],
            highlightbackground=self.colors['bg_secondary']
        )
        self.task_entry.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=8)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task,
            font=self.fonts['body'],
            bg=self.colors['accent'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text_primary']
        )
        add_btn.pack(side='right')
        
        # Tasks section
        tasks_label = tk.Label(
            main_frame,
            text="Tasks",
            font=self.fonts['heading'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        tasks_label.pack(anchor='w', pady=(10, 5))
        
        # Tasks container with scrollbar
        tasks_container = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        tasks_container.pack(fill='both', expand=True)
        
        # Canvas and scrollbar for scrollable task list
        self.canvas = tk.Canvas(
            tasks_container,
            bg=self.colors['bg_primary'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(tasks_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_primary'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Statistics
        self.stats_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], pady=10)
        self.stats_frame.pack(fill='x', pady=(20, 0))
        
        self.stats_label = tk.Label(
            self.stats_frame,
            text="Total: 0 | Completed: 0 | Remaining: 0",
            font=self.fonts['body'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.stats_label.pack()
        
        # Focus on entry
        self.task_entry.focus()
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def add_task(self):
        task_text = self.task_var.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task!")
            return
            
        task = {
            'id': len(self.tasks),
            'text': task_text,
            'completed': False,
            'timestamp': datetime.datetime.now()
        }
        
        self.tasks.append(task)
        self.task_var.set("")
        self.refresh_tasks()
        self.update_stats()
        
    def toggle_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                break
        self.refresh_tasks()
        self.update_stats()
        
    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.refresh_tasks()
        self.update_stats()
        
    def refresh_tasks(self):
        # Clear existing task widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Create task widgets
        for i, task in enumerate(self.tasks):
            self.create_task_widget(task, i)
            
    def create_task_widget(self, task, index):
        # Task container
        task_frame = tk.Frame(
            self.scrollable_frame,
            bg=self.colors['bg_secondary'],
            pady=8,
            padx=12
        )
        task_frame.pack(fill='x', pady=2)
        
        # Checkbox
        checkbox_var = tk.BooleanVar(value=task['completed'])
        checkbox = tk.Checkbutton(
            task_frame,
            variable=checkbox_var,
            command=lambda: self.toggle_task(task['id']),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent'],
            selectcolor=self.colors['bg_secondary'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['accent'],
            cursor='hand2',
            bd=0,
            highlightthickness=0
        )
        checkbox.pack(side='left', padx=(0, 10))
        
        # Task text
        text_color = self.colors['completed'] if task['completed'] else self.colors['text_primary']
        task_font = self.fonts['task']
        
        task_label = tk.Label(
            task_frame,
            text=task['text'],
            font=task_font,
            bg=self.colors['bg_secondary'],
            fg=text_color,
            anchor='w',
            justify='left'
        )
        
        if task['completed']:
            # Add strikethrough effect for completed tasks
            task_font = (task_font[0], task_font[1], 'overstrike')
            task_label.configure(font=task_font)
            
        task_label.pack(side='left', fill='x', expand=True)
        
        # Delete button
        delete_btn = tk.Button(
            task_frame,
            text="🗑️",
            command=lambda: self.delete_task(task['id']),
            bg=self.colors['danger'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0,
            padx=8,
            pady=2,
            cursor='hand2',
            font=('Segoe UI', 12),
            activebackground='#C0392B',
            activeforeground=self.colors['text_primary']
        )
        delete_btn.pack(side='right', padx=(10, 0))
        
    def update_stats(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        remaining = total - completed
        
        stats_text = f"Total: {total} | Completed: {completed} | Remaining: {remaining}"
        self.stats_label.configure(text=stats_text)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()