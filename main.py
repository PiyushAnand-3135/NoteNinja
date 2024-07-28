from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.geometry("1080x620")
root.title("NoteNinja - The OpenSource text editor")
root.iconbitmap('logo.ico')

saved = False
file_path = None  # Keep track of the file path
default_font_size = 20  # Set the default font size

def on_closing():
    if not saved and not is_text_area_empty():
        if messagebox.askokcancel("Unsaved Changes", "You have unsaved changes. Do you want to quit without saving?"):
            root.destroy()
    else:
        root.destroy()

def is_text_area_empty():
    content = text_area.get("1.0", "end-1c").strip()
    return len(content) == 0

def new_file():
    global saved
    if saved or is_text_area_empty():
        text_area.delete("1.0", END)
        saved = False
    else:
        new_confirm = messagebox.askyesno("Unsaved Changes",
                                          "Are you sure you want to create a new file without saving changes?")
        if new_confirm:
            text_area.delete("1.0", END)
            saved = False

def open_file():
    global file_path, saved
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as f:
            content = f.read()
            text_area.delete("1.0", "end")
            text_area.insert("1.0", content)
        saved = True

def save_file():
    global saved, file_path
    if not saved:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            saved = True

    if saved and file_path:
        with open(file_path, 'w') as f:
            f.write(text_area.get("1.0", "end-1c"))

def save_as():
    global saved, file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        saved = True
        with open(file_path, 'w') as f:
            f.write(text_area.get("1.0", "end-1c"))

def exit_app():
    global saved
    if saved or is_text_area_empty():
        root.quit()
    else:
        quit_confirm = messagebox.askyesno("Unsaved Changes", "Are you sure you want to exit without saving changes?")
        if quit_confirm:
            root.quit()

def about():
    messagebox.showinfo("About NoteNinja", "NoteNinja is a text editor made by Piyush Anand")

def report_problem():
    messagebox.showinfo("Report a problem", "Write a mail on anandpiyush404@gmail.com")

def edit_font_size():
    def set_font_size():
        try:
            size = int(font_size_entry.get())
            text_area.config(font=("Arial", size))
            font_size_win.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid font size")

    font_size_win = Toplevel(root)
    font_size_win.geometry("220x180")
    font_size_win.title("Edit Font Size")
    font_size_label = Label(font_size_win, text="Enter font size:")
    font_size_label.pack(pady=10)
    font_size_entry = Entry(font_size_win, width=20)
    font_size_entry.pack(pady=10)
    set_button = Button(font_size_win, text="Set", command=set_font_size, width=10)
    set_button.pack(pady=10)

# Frame for the menu bar
menu_frame = Frame(root)
menu_frame.pack(side=TOP, fill=X)

# MenuBar
my_menu = Menu(root)

# File Menu
file_menu = Menu(my_menu, tearoff=False)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_command(label="Exit", command=exit_app)
my_menu.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
edit_menu.add_command(label="Edit Font Size", command=edit_font_size)
my_menu.add_cascade(label="Edit", menu=edit_menu)

# Help Menu
help_menu = Menu(my_menu, tearoff=False)
help_menu.add_command(label="About NoteNinja", command=about)
help_menu.add_command(label="Report a problem", command=report_problem)
my_menu.add_cascade(label="Help", menu=help_menu)

# Show main menu on the app window
root.config(menu=my_menu)

# Frame for the text area
text_frame = Frame(root)
text_frame.pack(expand=True, fill='both')

# Add a Scrollbar to the text area
scroll_bar = Scrollbar(text_frame)
scroll_bar.pack(side=RIGHT, fill=Y)

# Input text area
text_area = Text(text_frame, wrap=WORD, undo=True, font=("Arial", default_font_size), yscrollcommand=scroll_bar.set)
text_area.pack(expand=True, fill='both')

# Configure the Scrollbar
scroll_bar.config(command=text_area.yview)

# Set focus to the text area
text_area.focus_set()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
