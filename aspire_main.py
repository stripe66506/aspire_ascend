import tkinter
from tkinter import messagebox, Entry, Button, Tk
import os
from PIL import Image, ImageTk, ImageEnhance
# from aspire_functions import sm_transition_cm
import runpy
from transitions import supmain_trans_cm


os.chdir(os.path.dirname(os.path.abspath(__file__)))

def about():
    messagebox.showinfo(title="About", message="Aspire Ascend 1.0.\nProgrammed by LBJ\n July 9, 2023")

def sup_main_menu():

    spmain_menu_window = tkinter.Tk()
    spmain_menu_window.title("Main Menu")
    spmain_menu_window.configure(bg='#000000')
    spmain_menu_window.state('zoomed')
    spmain_menu_window.iconbitmap(r'images\icons\futuristic.ico')
    # Here you would add all the widgets you need in your main menu
    # For demonstration purposes, let's just add a label
    main_label = tkinter.Label(spmain_menu_window, text="Main Menu", font=("Arial", 20), bg='#000000', fg='white')
    main_label.pack()

    # Create a top-level menu
    menubar = tkinter.Menu(spmain_menu_window)

    # Create a submenu te be part of the top-level menu
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Client Management", command=lambda: supmain_trans_cm(spmain_menu_window))
    filemenu.add_command(label="Program Management", command=lambda: print("Option 2 selected"))
    filemenu.add_command(label="Generate Reports", command=lambda: print("Option 3 selected"))
    filemenu.add_command(label="User Management", command=lambda: print("Option 4 selected"))

    aboutmenu = tkinter.Menu(menubar, tearoff=0)
    aboutmenu.add_command(label="Help", command=lambda: print("Option 1 selected"))
    aboutmenu.add_command(label="About", command=about)

    # Add the File menu to the menu bar
    menubar.add_cascade(label="Selection", menu=filemenu)
    menubar.add_cascade(label="About", menu=aboutmenu)

    # Associate the menu bar to the window
    spmain_menu_window.config(menu=menubar)

    # Update the window to ensure correct sizes are retrieved
    spmain_menu_window.update()

    # Window size
    window_width = 1200
    window_height = 700

    # Screen size
    screen_width = spmain_menu_window.winfo_screenwidth()
    screen_height = spmain_menu_window.winfo_screenheight()

    # Center position
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))

    # Set window size and position
    spmain_menu_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    spmain_menu_window.iconbitmap('.\images\icons\\futuristic.ico')

    img = Image.open('images\sup_main1.png')
    img = img.resize((1200, 700), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    main_image = tkinter.Label(spmain_menu_window, image=img, bg='#000000')
    main_image.image = img
    main_image.place(x=50, y=0, relwidth=1, relheight=1)

    spmain_menu_window.mainloop()

if __name__ == "__main__":
    sup_main_menu()