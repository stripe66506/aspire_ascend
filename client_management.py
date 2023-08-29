import sqlite3
from datetime import datetime
import tkinter
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from aspire_functions import sm_transition_bulk

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def sp_cm_menu():

    sp_cm_window = tkinter.Tk()
    sp_cm_window.title("Client Management")
    sp_cm_window.configure(bg='#000000')
    sp_cm_window.state('zoomed')
    sp_cm_window.iconbitmap(r'images\icons\futuristic.ico')

    # Here you would add all the widgets you need in your main menu
    # For demonstration purposes, let's just add a label
    cm_label = tkinter.Label(sp_cm_window, text="Client Management", font=("Arial", 20), bg='#000000', fg='white')
    cm_label.pack()

    # Create a top-level menu
    menubar = tkinter.Menu(sp_cm_window)

    # Create a submenu te be part of the top-level menu
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Client Intake (bulk)", command=lambda: sm_transition_bulk(sp_cm_window))
    filemenu.add_command(label="Client Intake (Individual)", command= lambda: transition(main_menu_window,create_cm_menu))
    filemenu.add_command(label="Discharge", command=lambda: print("Option 3 selected"))
    filemenu.add_command(label="Graduation", command=lambda: print("Option 4 selected"))
    filemenu.add_command(label="Post-Graduation", command=lambda: print("Option 4 selected"))
    filemenu.add_command(label="Main Menu", command=lambda: main_menu_window.mainloop())

    aboutmenu = tkinter.Menu(menubar, tearoff=0)
    aboutmenu.add_command(label="Help", command=lambda: print("Option 1 selected"))
    aboutmenu.add_command(label="About", command=lambda: print("Option 2 selected"))

    # Add the File menu to the menu bar
    menubar.add_cascade(label="Selection", menu=filemenu)

    # Associate the menu bar to the window
    sp_cm_window.config(menu=menubar)

    # Update the window to ensure correct sizes are retrieved
    sp_cm_window.update()

    # Window size
    window_width = 1200
    window_height = 700

    # Screen size
    screen_width = sp_cm_window.winfo_screenwidth()
    screen_height = sp_cm_window.winfo_screenheight()

    # Center position
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))

    img = Image.open(r'images\sp_cm.png')
    img = img.resize((1200, 700), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    cm_image = tkinter.Label(sp_cm_window, image=img, bg='#000000')
    cm_image.image = img
    cm_image.place(x=50, y=0, relwidth=1, relheight=1)

    # Set window size and position
    sp_cm_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    sp_cm_window.mainloop()

class ClientManagement:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_form(self, root):

        # Create a callback function to be called when the user submits the form
        def submit_form():



            client_data = (
                athena_var.get(),
                client_last_var.get(),
                client_first_var.get(),
                dob_var.get(),
                referral_source_var.get(),
                referral_type_var.get(),
                referral_date_var.get(),
                district_var.get(),
                race_var.get(),
                ethnicity_var.get(),
                gender_var.get(),
                csw_var.get(),
                yls_var.get(),
                start_date_var.get(),
                start_living_var.get(),
                start_edc_var.get(),
                start_emp_var.get(),
                case_manager_id_var.get(),
                group_id_var.get()
            )

            try:
                # Call the add_client method with the data
                self.add_client(client_data)
                messagebox.showinfo("Success", "Client added successfully")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Create variables to hold the form data
        athena_var = tk.StringVar()
        client_last_var = tk.StringVar()
        client_first_var = tk.StringVar()
        dob_var = tk.StringVar()
        referral_source_var = tk.StringVar()
        referral_type_var = tk.StringVar()
        referral_date_var = tk.StringVar()
        district_var = tk.StringVar()
        race_var = tk.StringVar()
        ethnicity_var = tk.StringVar()
        gender_var = tk.StringVar()
        csw_var = tk.StringVar()
        yls_var = tk.StringVar()
        start_date_var = tk.StringVar()
        start_living_var = tk.StringVar()
        start_edc_var = tk.StringVar()
        start_emp_var = tk.StringVar()
        case_manager_id_var = tk.StringVar()
        group_id_var = tk.StringVar()

        label_style = {"font": ("Arial", 12)}

        # Labels with common style
        tk.Label(root, text="Athena", **label_style).grid(row=0)
        tk.Label(root, text="Last Name", **label_style).grid(row=1)
        tk.Label(root, text="First Name", **label_style).grid(row=2)
        tk.Label(root, text="Date of Birth", **label_style).grid(row=3)
        tk.Label(root, text="Referral Source", **label_style).grid(row=4)
        tk.Label(root, text="Referral Type", **label_style).grid(row=5)
        tk.Label(root, text="Referral Date", **label_style).grid(row=6)
        tk.Label(root, text="District", **label_style).grid(row=7)
        tk.Label(root, text="Race", **label_style).grid(row=8)
        tk.Label(root, text="Ethnicity", **label_style).grid(row=9)
        tk.Label(root, text="Gender", **label_style).grid(row=10)
        tk.Label(root, text="CSW", **label_style).grid(row=11)
        tk.Label(root, text="YLS", **label_style).grid(row=12)
        tk.Label(root, text="Start Date", **label_style).grid(row=13)
        tk.Label(root, text="Start Living", **label_style).grid(row=14)
        tk.Label(root, text="Start EDC", **label_style).grid(row=15)
        tk.Label(root, text="Start Employment", **label_style).grid(row=16)
        tk.Label(root, text="Case Manager ID", **label_style).grid(row=17)
        tk.Label(root, text="Group ID", **label_style).grid(row=18)

        # Entry Fields
        tk.Entry(root, textvariable=athena_var).grid(row=0, column=1)
        tk.Entry(root, textvariable=client_last_var).grid(row=1, column=1)
        tk.Entry(root, textvariable=client_first_var).grid(row=2, column=1)
        tk.Entry(root, textvariable=dob_var).grid(row=3, column=1)
        tk.Entry(root, textvariable=referral_source_var).grid(row=4, column=1)
        tk.Entry(root, textvariable=referral_type_var).grid(row=5, column=1)
        tk.Entry(root, textvariable=referral_date_var).grid(row=6, column=1)
        tk.Entry(root, textvariable=district_var).grid(row=7, column=1)
        tk.Entry(root, textvariable=race_var).grid(row=8, column=1)
        tk.Entry(root, textvariable=ethnicity_var).grid(row=9, column=1)
        tk.Entry(root, textvariable=gender_var).grid(row=10, column=1)
        tk.Entry(root, textvariable=csw_var).grid(row=11, column=1)
        tk.Entry(root, textvariable=yls_var).grid(row=12, column=1)
        tk.Entry(root, textvariable=start_date_var).grid(row=13, column=1)
        tk.Entry(root, textvariable=start_living_var).grid(row=14, column=1)
        tk.Entry(root, textvariable=start_edc_var).grid(row=15, column=1)
        tk.Entry(root, textvariable=start_emp_var).grid(row=16, column=1)
        tk.Entry(root, textvariable=case_manager_id_var).grid(row=17, column=1)
        tk.Entry(root, textvariable=group_id_var).grid(row=18, column=1)

        # repeat the above two lines for each field...

        # Add a submit button
        tk.Button(root, text="Submit", command=submit_form).grid()

    def import_clients(self):
        # your import code goes here
        print("Importing clients...")

    # You can add more methods related to client management here, such as:
    def add_client(self, client_data):
        client_data = list(client_data)


        sql = '''
            INSERT INTO clients (
                athena, 
                client_last, 
                client_first, 
                referral_source, 
                referral_type, 
                referral_date, 
                age, 
                district, 
                race, 
                ethnicity, 
                gender, 
                csw, 
                yls, 
                start_date, 
                start_living, 
                start_edc, 
                start_emp, 
                end_date, 
                end_status, 
                end_living, 
                end_edu, 
                end_emp, 
                end_arrest, 
                follow_up, 
                fu_living, 
                fu_edu, 
                fu_emp, 
                fu_arrest, 
                case_manager_id, 
                group_id, 
                alumni_status, 
                terminated
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        self.cursor.execute(sql, client_data)
        self.conn.commit()

    def calculate_age(self, dob, referral_date):
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        referral_date = datetime.strptime(referral_date, "%Y-%m-%d")

        age = referral_date.year - dob_date.year - (
                    (referral_date.month, referral_date.day) < (dob_date.month, dob_date.day))

        return age

    def close(self):
        self.conn.close()

    def remove_client(self, client):
        self.clients.remove(client)

    def list_clients(self):
        for client in self.clients:
            print(client)
            
sp_cm_menu()