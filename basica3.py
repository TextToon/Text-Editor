import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
import threading
from spellchecker import SpellChecker

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
    text_area.tag_remove('highlight', '1.0', tk.END)
    if target:
        idx = '1.0'
        while True:
            idx = text_area.search(target, idx, nocase=1, stopindex=tk.END)
            if not idx: break
            lastidx = f'{idx}+{len(target)}c'
            text_area.tag_add('highlight', idx, lastidx)
            idx = lastidx
        text_area.tag_config('highlight', background='yellow')

def change_font_size():
    size = simpledialog.askinteger("Font Size", "Enter size:")
    if size:
        text_area.config(font=("Arial", size))

def toggle_theme():
    current_bg = text_area.cget("bg")
    new_bg = "black" if current_bg == "white" else "white"
    new_fg = "white" if current_bg == "white" else "black"
    text_area.config(bg=new_bg, fg=new_fg)

def auto_save():
    if file_path:
        with open(file_path, 'w') as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)
    else:
        save_file_as()
    threading.Timer(60, auto_save).start()  # Auto-save every 60 seconds

def add_color():
    color = colorchooser.askcolor()[1]
    if color:
        current_tags = text_area.tag_names("sel.first")
        text_area.tag_add("colored_text", "sel.first", "sel.last")
        text_area.tag_configure("colored_text", foreground=color)

spell_checker = SpellChecker()

def check_spelling():
    text = text_area.get("1.0", "end-1c")
    words = text.split()
    misspelled = spell_checker.unknown(words)
    for word in misspelled:
        start_idx = text_area.search(word, "1.0", tk.END)
        end_idx = f"{start_idx}+{len(word)}c"
        text_area.tag_add("misspelled", start_idx, end_idx)
        text_area.tag_config("misspelled", background="red", foreground="white")

def quit_app():
    root.quit()

# Initialize Tkinter
root = tk.Tk()
root.title("Basica 3.0")
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
tk.Button(frame, text="Auto Save", command=auto_save).pack(padx=10, pady=5)
tk.Button(frame, text="Add Color", command=add_color).pack(padx=10, pady=5)
tk.Button(frame, text="Check Spelling", command=check_spelling).pack(padx=10, pady=5)

# Create Text Area
text_area = tk.Text(root, wrap='word', font=('Arial', 12), bg="white", fg="black")
text_area.pack(expand=1, fill='both', side="right")

# Bind Shortcuts
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Shift-S>', lambda event: save_file_as())
root.bind('<Control-f>', lambda event: find_text())
root.bind('<Control-n>', lambda event: new_file())
root.bind('<Control-a>', lambda event: text_area.tag_add('sel', '1.0', 'end'))
root.bind('<Control-c>', lambda event: root.event_generate('<<Copy>>'))
root.bind('<Control-v>', lambda event: root.event_generate('<<Paste>>'))
root.bind('<Control-Shift-C>', lambda event: check_spelling())
root.bind('<Control-q>', lambda event: quit_app())

# Run the application
root.mainloop()


