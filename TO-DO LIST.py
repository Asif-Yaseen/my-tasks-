import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("🌈 Colorful To-Do List")
root.geometry("400x500")
root.configure(bg="#f0f8ff")

tasks = []

# Add task function
def add_task():
    task = entry.get()
    if task:
        tasks.append({"text": task, "done": False})
        entry.delete(0, tk.END)
        update_list()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Delete selected task
def delete_task():
    selected = listbox.curselection()
    if selected:
        tasks.pop(selected[0])
        update_list()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Delete all tasks
def delete_all():
    if tasks:
        confirm = messagebox.askyesno("Confirm Delete All", "Are you sure you want to delete all tasks?")
        if confirm:
            tasks.clear()
            update_list()
    else:
        messagebox.showinfo("No Tasks", "There are no tasks to delete.")

# Mark task as done
def mark_done():
    selected = listbox.curselection()
    if selected:
        tasks[selected[0]]["done"] = not tasks[selected[0]]["done"]
        update_list()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark.")

# Update listbox display
def update_list():
    listbox.delete(0, tk.END)
    for task in tasks:
        display_text = task["text"]
        listbox.insert(tk.END, display_text)
        index = listbox.size() - 1
        if task["done"]:
            listbox.itemconfig(index, {'bg': '#98fb98', 'fg': '#006400'})  # Green for done
        else:
            listbox.itemconfig(index, {'bg': '#add8e6', 'fg': '#00008b'})  # Blue for pending

# UI Elements
entry = tk.Entry(root, font=("Helvetica", 14))
entry.pack(pady=10, padx=20, fill=tk.X)

btn_frame = tk.Frame(root, bg="#f0f8ff")
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="Add Task", command=add_task, bg="#87cefa", fg="white", width=10)
add_btn.grid(row=0, column=0, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Task", command=delete_task, bg="#ff6347", fg="white", width=10)
delete_btn.grid(row=0, column=1, padx=5)

done_btn = tk.Button(btn_frame, text="Mark Done", command=mark_done, bg="#32cd32", fg="white", width=10)
done_btn.grid(row=0, column=2, padx=5)

delete_all_btn = tk.Button(root, text="🗑️Delete All Tasks", command=delete_all, bg="#dc143c", fg="white", font=("Helvetica", 12))
delete_all_btn.pack(pady=10)

listbox = tk.Listbox(root, font=("Helvetica", 12), selectbackground="#ffa07a", activestyle="none")
listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Run the app
root.mainloop()