import tkinter as tk
import sqlite3
import bcrypt
from tkinter import messagebox
import os
from transitions import login_transition_sup_main

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Connect to the database
conn = sqlite3.connect('database/central_database.db')
c = conn.cursor()

# Function to login
def login(event=None):
    username = username_entry.get().strip()
    entered_password = password_entry.get().strip()

    if not username or not entered_password:
        messagebox.showerror("Error", "Username and Password cannot be empty.")
        return

    c.execute('SELECT password_hash, salt, fname, lname FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    if user is None:
        messagebox.showerror("Error", "User not found.")
        return

    stored_password_hash, stored_salt, fname, lname = user
    entered_password_hash = bcrypt.hashpw(entered_password.encode('utf-8'), stored_salt)

    if stored_password_hash == entered_password_hash:
        # Check for 'II' in name and titlecase other parts
        formatted_fname = ' '.join([part if part.lower() == 'ii' else part.title() for part in fname.split()])
        formatted_lname = ' '.join([part if part.lower() == 'ii' else part.title() for part in lname.split()])

        c.execute('SELECT access FROM users WHERE username = ?', (username,))
        user_access = c.fetchone()

    if user_access is None:
        messagebox.showerror("Error", "User access category not found.")
        return

    user_access = user_access[0]

    if user_access.lower() == 'supervisor':
        # Redirect to the supervisor menu
        messagebox.showinfo("Login successful", f"Welcome, Supervisor {formatted_fname} {formatted_lname}!")
        
        login_transition_sup_main(window)

    elif user_access.lower() == 'staff':
        # Redirect to the staff menu
        messagebox.showinfo("Login successful", f"Welcome, Staff {formatted_fname} {formatted_lname}!")
    elif user_access.lower() == 'education':
        # Redirect to the education menu
        messagebox.showinfo("Login successful", f"Welcome, Education Officer {formatted_fname} {formatted_lname}!")
    elif user_access.lower() == 'officer':
        # Redirect to the officer menu
        messagebox.showinfo("Login successful", f"Welcome, Officer {formatted_fname} {formatted_lname}!")
    else:
        messagebox.showinfo("Login successful", f"Welcome, {formatted_fname} {formatted_lname}!")

        
# Create the main window
window = tk.Tk()
window.title("Aspire Login")
window.geometry('400x200')
window.configure(bg='#483D8B')
window.state('zoomed')
window.iconbitmap(r'images\icons\futuristic.ico')

# Create title label
title_label = tk.Label(window, text="Ascend Aspire Log in Page", bg='#483D8B', fg='#D3D3D3', font=('Arial', 60, 'bold italic'))
title_label.pack(pady=20)

# Create frame for fields
fields_frame = tk.Frame(window, bg='#483D8B')
fields_frame.pack()

# Create labels and entry widgets
tk.Label(fields_frame, text="Username:", bg='#483D8B', font=('Arial', 15, 'bold italic')).grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(fields_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(fields_frame, text="Password:", bg='#483D8B', font=('Arial', 15, 'bold italic')).grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(fields_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Bind the login function to the Enter key event
window.bind("<Return>", login)

# Create login button
login_button = tk.Button(window, text="Login", command=login)
login_button.pack(pady=10)

photo = tk.PhotoImage(file=r"images\doc_shield.png")
photo_label = tk.Label(window, image=photo, bg='#483D8B')
photo_label.pack(pady=10)

# Bind the login function to the Enter key event
window.bind("<Return>", login)

# Start the Tkinter event loop
window.mainloop()

# Close the connection
conn.close()