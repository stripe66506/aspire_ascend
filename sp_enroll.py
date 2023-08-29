import tkinter as tk
import sqlite3
import os
from tkinter import messagebox
import client_profile
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def about():
    root.iconbitmap('images/icons/database.ico')  # Set the icon for messagebox
    messagebox.showinfo("About", message="Names of the ERC applicants not yet enrolled in groups and services are listed here.")
    root.iconbitmap('images/icons/futuristic.ico')  # Reset the icon back to original after messagebox is closed

def get_unenrolled_students():
    conn = sqlite3.connect('database/central_database.db')
    cursor = conn.cursor()

    # Assuming that 'clients' is your table name and 'enrolled' is your column name
    cursor.execute("SELECT * FROM clients WHERE enrolled=0")
    students = cursor.fetchall()
    conn.close()
    return students

def update_listbox(listbox, students):
    listbox.delete(0, tk.END)
    for i, student in enumerate(students):
        id, first_name, last_name = student[0], student[2], student[1]
        listbox.insert(tk.END, f"{i+1}. {first_name} {last_name}")

def refresh():
    global students
    students = get_unenrolled_students()
    update_listbox(listbox, students)

def display_selected_student(event):
    # Get the index of the selected listbox item
    index = listbox.curselection()[0]

    # Get the data of the selected student
    selected_student = students[index]

    # Now you can display the selected student's data

def open_profile(event):

    # Get the index of the selected listbox item
    index = listbox.curselection()[0]

    # Get the data of the selected student
    selected_student = students[index]

    # Now you can open the client_profile.py script and pass the student's ID
    # os.system(f"python client_profile.py {selected_student[0]}")
    subprocess.Popen(['python', 'client_profile.py', str(selected_student[0])])

# Create the GUI
root = tk.Tk()
root.title("Enrollment")
root.configure(background="#000000")
root.state("zoomed")
root.iconbitmap('images/icons/futuristic.ico')

# Create a top-level menu
menubar = tk.Menu(root)

# Create a pull-down menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Client Management Menu", command=root.quit)
filemenu.add_command(label="Main Menu", command=root.quit)

aboutmenu = tk.Menu(menubar, tearoff=0)
aboutmenu.add_command(label="Help", command=about)

# Add the pull-down menu to the menu bar
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="About", menu=aboutmenu)

# Display the menu bar
root.config(menu=menubar)

# Create the frame
frame = tk.Frame(root)
frame.pack(side=tk.LEFT, fill=tk.BOTH)

# Create the listbox
listbox = tk.Listbox(frame, width=50)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame, orient="vertical")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)

listbox.bind('<Double-Button-1>', open_profile)

image = tk.PhotoImage(file="images/enrollment.png")
# Adjust the image size by changing the values of x and y in subsample(x, y)
image = image.subsample(2, 2)
image_label = tk.Label(root, image=image, bg = "#000000")
image_label.pack(side=tk.RIGHT, fill=tk.BOTH)

# Bind the <<ListboxSelect>> event to the function
listbox.bind('<<ListboxSelect>>', open_profile)

refresh()

refresh_button = tk.Button(root, text="Refresh", command=refresh)
refresh_button.place(relx=0.5, rely=0.5, anchor='center')

root.mainloop()
