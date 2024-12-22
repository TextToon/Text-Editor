import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def new_file():
    text_area.delete(1.0, tk.END)
    root.title("Basica 2.0 - Untitled")
    global file_path
    file_path = None

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)
            root.title(f"Basica 2.0 - {file_path}")

def save_file():
    global file_path
    if file_path:
        with open(file_path, 'w') as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)
    else:
        save_file_as()

def save_file_as():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)
            root.title(f"Basica 2.0 - {file_path}")

def find_text():
    target = simpledialog.askstring("Find", "Enter text:")
    content = text_area.get(1.0, tk.END)
    start_idx = content.find(target)
    if start_idx != -1:
        end_idx = start_idx + len(target)
        text_area.tag_add("highlight", f"1.{start_idx}", f"1.{end_idx}")
        text_area.tag_config("highlight", background="yellow")
    else:
        messagebox.showinfo("Not Found", f"'{target}' not found")

def change_font_size():
    size = simpledialog.askinteger("Font Size", "Enter size:")
    if size:
        text_area.config(font=("Arial", size))

def toggle_theme():
    current_bg = text_area.cget("bg")
    new_bg = "black" if current_bg == "white" else "white"
    new_fg = "white" if current_bg == "white" else "black"
    text_area.config(bg=new_bg, fg=new_fg)

# Initialize Tkinter
root = tk.Tk()
root.title("Basica 2.0")
root.geometry("800x600")

# Create Frame for settings
frame = tk.Frame(root, bg="lightgrey")
frame.pack(side="left", fill="y")

# Create Buttons for settings
tk.Button(frame, text="New File", command=new_file).pack(padx=10, pady=5)
tk.Button(frame, text="Open", command=open_file).pack(padx=10, pady=5)
tk.Button(frame, text="Save", command=save_file).pack(padx=10, pady=5)
tk.Button(frame, text="Save As", command=save_file_as).pack(padx=10, pady=5)
tk.Button(frame, text="Find", command=find_text).pack(padx=10, pady=5)
tk.Button(frame, text="Font Size", command=change_font_size).pack(padx=10, pady=5)
tk.Button(frame, text="Toggle Theme", command=toggle_theme).pack(padx=10, pady=5)

# Create Text Area
text_area = tk.Text(root, wrap='word', font=('Arial', 12), bg="white", fg="black")
text_area.pack(expand=1, fill='both', side="right")

# Run the application
root.mainloop()
