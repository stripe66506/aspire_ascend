import sqlite3
import datetime
import tkinter
from tkinter import messagebox, Label, Frame, Button, filedialog, ttk
from tkcalendar import Calendar, DateEntry
import pandas as pd
import os
from PIL import Image, ImageTk
import glob
import subprocess
from transitions import login_transition_sup_main
import runpy
from transitions import sp_trans_ind

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
filemenu.add_command(label="Client Intake (Individual)", command= lambda: sp_trans_ind(sp_cm_window))
filemenu.add_command(label="Client Intake (Bulk)", command=lambda: cm_trans_bulk(sp_cm_window))
filemenu.add_command(label="Enrollment", command=lambda: sp_trans_enroll(sp_cm_window))
filemenu.add_command(label="Discharge", command=lambda: print("Option 3 selected"))
filemenu.add_command(label="Graduation", command=lambda: print("Option 4 selected"))
filemenu.add_command(label="Post-Graduation", command=lambda: print("Option 4 selected"))
filemenu.add_command(label="Main Menu", command=lambda: login_transition_sup_main(sp_cm_window))

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

def get_officer_id(cursor, officer_name):
     cursor.execute("SELECT id FROM probation_officers WHERE officer_full_name = ?", (officer_name,))
     result = cursor.fetchone()
     
     return result[0] if result else None

def get_group_id(cursor, officer_name):
     cursor.execute("SELECT id FROM probation_officers WHERE officer_full_name = ?", (officer_name,))
     result = cursor.fetchone()
     
     return result[0] if result else None

def back_to_cm(current_window):
     
        current_window.destroy()

def cm_trans_bulk(current_window):
    current_window.destroy()

    bulk_intake()

def bulk_intake():
    bulk_window = tkinter.Tk()
    bulk_window.title("Bulk Intake")
    bulk_window.configure(bg='#000000')
    bulk_window.state('zoomed')
    bulk_window.iconbitmap(r'images\icons\futuristic.ico')

    # Create the top level menu
    menubar = tkinter.Menu(bulk_window)

    # Create a submenu te be part of the top-level menu
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Client Intake (Individual)", command=lambda: sp_trans_ind(bulk_window))
    filemenu.add_command(label="Client Management Menu", command=lambda: back_to_cm(bulk_window))

    # Add the File menu to the menu bar
    menubar.add_cascade(label="Selection", menu=filemenu)

    # Associate the menu bar to the window
    bulk_window.config(menu=menubar)

    img = Image.open(r'images\bulk.png')
    img = img.resize((500, 500), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    # Here the image label is created
    bulk_image = tkinter.Label(bulk_window, image=img, bg='#000000')
    bulk_image.image = img
    bulk_image.pack(side='right')  # This will pack the image to the right

    # Create a frame to hold the labels and use it as a reference in the grid() method.
    labels_frame = tkinter.Frame(bulk_window, bg='#000000')
    labels_frame.pack(side='left')

    # Create the labels
    bulk_label = tkinter.Label(labels_frame, text="Bulk Intake", font=("Arial", 20), bg='#000000', fg='white')
    title = Label(labels_frame, text="Client Intake", font=("Arial", 20), bg='#000000', fg='white')
    instructions_text1 = (f"{'1.'.ljust(3)} {'Click the Import button'.ljust(52)}")
    instructions_text2 = (f"{'2.'.ljust(3)} {'Navigate to the directory of the referral spreadsheets'.ljust(52)}")
    instructions_text3 = (f"{'3.'.ljust(3)} {'Follow on screen instructions'.ljust(52)}")

    instructions1 = Label(labels_frame, text=instructions_text1, font=("Arial", 12), bg='#000000', fg='white')
    instructions2 = Label(labels_frame, text=instructions_text2, font=("Arial", 12), bg='#000000', fg='white')
    instructions3 = Label(labels_frame, text=instructions_text3, font=("Arial", 12), bg='#000000', fg='white')

    # Place the labels
    bulk_label.pack()
    title.pack()
    instructions1.pack()
    instructions2.pack()
    instructions3.pack()

    # Create a spacer
    spacer = Frame(labels_frame, height=10, bg='#483D8B')
    spacer.pack()

    # Create the button without an image
    import_button = Button(labels_frame, text="Import Excel Files", command=import_data)

    # Pack the button
    import_button.pack()

    bulk_window.mainloop()

#function to import referral applications from excel in bulk

def import_data():
    # Open a directory dialog and get the selected directory's path
    dirpath = filedialog.askdirectory()

    # Get a list of all Excel files in the directory
    excel_files = glob.glob(os.path.join(dirpath, '*.xlsm*'))

    # Connect to the database
    conn = sqlite3.connect('database\central_database.db')

    cursor = conn.cursor()

    def new_officer(officer_name):

        connection = sqlite3.connect('database\central_database.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO probation_officers (officer_full_name) VALUES (?) ', (officer_name,))
        connection.commit()

        officer_id = int(get_officer_id(cursor, officer_name))
        data['probation_officer_id'] = officer_id

        connection.close()

    def officer_check(officer_name):
        connection = sqlite3.connect('database\central_database.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM probation_officers WHERE officer_full_name = ? ', (officer_name), )
        check_officer = cursor.fetchone

        if check_officer is None:
            new_officer(officer_name)

        else:

                officer_id = int(get_officer_id(cursor, officer_name))
                data['probation_officer_id'] = officer_id

    for filepath in excel_files:

        # Read the Excel file
        df = pd.read_excel(filepath, header=None)

        # Define quarter information based on "B7"
        date = pd.to_datetime(df.iloc[int("B7"[1:]) - 1, ord("B7"[0]) - 65])
        if 7 <= date.month <= 9:
            quarter = 'Q1'
        elif 10 <= date.month <= 12:
            quarter = 'Q2'
        elif 1 <= date.month <= 3:
            quarter = 'Q3'
        elif 4 <= date.month <= 6:
            quarter = 'Q4'

        # Define cell to column mapping depending on the value in cell A1
        if df.iloc[0, 0] == "JRF":  # cell A1 is at index [0, 0]
            cell_column_mapping = {
                "B9": "client_last",
                "B8": "client_first",
                "B11": 'athena',
                "B10": 'dob',
                "B17": 'gender',
                "B15": 'race',
                "B16": 'ethnicity',
                "B27": 'classification',
                "B37": 'yls',
                "B18": 'referral_type',
                "B7": 'referral_date',
                "E41": "start_living",
                "B20": "ssn",
                "B12": "so",
                "C46": "start_emp",
                "B14": 'start_edu',
                "B45" : 'age',
                "D8" : 'par_gar01',
                "D9" : 'par_gar01_rel',
                "D10" : 'par_gar01_org',
                "D12" : 'par_gar01_add',
                "D13" : 'par_gar01_cell',
                "D14" : 'par_gar01_email',
                "D16" : 'par_gar02',
                "D17" : 'par_gar02_rel',
                "D18" : 'par_gar02_org',
                "D20" : 'par_gar02_add',
                "D21" : 'par_gar02_cell',
                "D22" : 'par_gar02_email',
                'D24' : 'par_proj',
                'G40' : 'eval_needed',
                'G39' : 'csw',
                'D25' : 'safety',
                'A1' : 'jrf',
                'D30' : 'other',
                'D35' : 'gang_affiliations',
                'D40' : 'conflicts'



            }


        else:
            cell_column_mapping = {
                 
                 "B7": 'referral_date',
                 "B9": 'referral_type',
                 'B10' : 'district',
                 'B11' : 'sup_type',
                 'B24' : 'client_cell',
                 "B13": "client_first",
                 "B14": "client_last",
                 "B15": 'dob',
                 "B16": 'athena',
                 'I35' : 'so',
                 "B18": 'classification',
                 "B20": 'race',
                 "B21": 'ethnicity',
                 "B22": 'gender',
                 'B25' : 'client_add',
                 "B26": "start_living",
                 'I34' : 'transport',
                 'I32' : 'groups',
                 'I33' : '1on1',
                 'B30' : 'court_ordered_groups',
                 "B31": 'start_edu',
                 'I30' : 'edu',
                 'B33' : 'edu_detail',
                 "B34": "start_emp",
                 'I31' : 'emp',
                 'I36' : 'csw',
                 'I29' : 'eval_needed',
                 'B38' : 'ssn',
                 "B52": 'yls',
                 'B53' : 'reason',
                 "B60" : 'age',
                 'B61' : 'big_three',
                 "D8" : 'par_gar01',
                 "D9" : 'par_gar01_rel',
                 "D10" : 'par_gar01_org',
                 "D12" : 'par_gar01_add',
                 "D13" : 'par_gar01_cell',
                 "D14" : 'par_gar01_email',
                 "D16" : 'par_gar02',
                 "D17" : 'par_gar02_rel',
                 "D18" : 'par_gar02_org',
                 "D20" : 'par_gar02_add',
                 "D21" : 'par_gar02_cell',
                 "D22" : 'par_gar02_email',
                 'D23' : 'par_proj',
                 'D30' : 'safety',
                 'D25' : 'family',
                 'D35' : 'other',
                 'D40' : 'gang_affiliations',
                 'D41' : 'conflicts',
                 'D47' : 'no_contacts',
                 'D53' : 'barriers',
                 'B19' : 'pro_req',
                 'B24' : 'client_cell'
            }
            

        data = {}
        for cell, column in cell_column_mapping.items():
            # Convert cell reference to row and column index
            row = int(cell[1:]) - 1
            col = ord(cell[0]) - 65
            data[column] = df.iloc[row, col]

        # Now add this code to insert '1' into the 'jrf' column
        if df.iloc[0, 0] == "JRF":

            data['jrf'] = 1
            data['start_living'] = 'Emergency Shelter'

            if df.iloc[12, 1] is not None:
                officer_name = df.iloc[12,1].strip().title()
                print(officer_name)
                officer_id = get_officer_id(cursor, officer_name)
                data['probation_officer_id'] = officer_id

        if df.iloc[0, 0] != "JRF":

            if df.iloc[6, 1] is not None:
                officer_name = df.iloc[7,1].strip()  # cell A1 is at index [0, 0]
                
                officer_check(officer_name)
            
        # Handle 'quarter' separately
        data['rep_qtr'] = quarter

        if df.iloc[0, 0] == "JRF":
             
             # Handle 'referral_date' separately
            data['start_date'] = data['referral_date']

        df_new = pd.DataFrame([data])

        if 'start_date' in df_new.columns:
            df_new['start_date'] = df_new['start_date'].dt.strftime('%Y/%m/%d')

        # Convert dates to YYYY/M/D format
        df_new['referral_date'] = df_new['referral_date'].dt.strftime('%Y/%m/%d')
        df_new['dob'] = df_new['dob'].dt.strftime('%Y/%m/%d')

        df_new.to_sql('clients', conn, if_exists='append', index=False)

        if data['eval_needed'] == 'True':
             # TODO: Create a function to generate the evaluation letter
             print('Evaluation letter generated')
             

        # Close the database connection
    conn.close()

        # Show a message box
    messagebox.showinfo("Import Complete", f"Successfully imported {len(excel_files)} spreadsheets.")

# function for referral source combo box
def fetch_probation_officers():
    conn = sqlite3.connect('database\central_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, officer_full_name FROM probation_officers")
    officers = cursor.fetchall()
    cursor.close()
    conn.close()

    # # Convert list of tuples into dictionary with the officer's full name as the key and ID as the value
    # officers_dict = {officer[1]: officer[0] for officer in officers}
    # return officers_dict

    officers_sorted = sorted(officer[1] for officer in officers)
    return officers_sorted



def fetch_classes():

    # Query the database to get the list of class tables
    conn = sqlite3.connect('database\central_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT group_name FROM groups")
    groups = [row[0] for row in cursor.fetchall()]
    conn.close()

    groups.sort()
   
    # Return the list of class table names as the list of classes
    return groups

def fetch_case_managers():
    # Query the case_managers table to get the list of case managers
    conn = sqlite3.connect('database\central_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM case_managers")
    case_managers = [row[0] for row in cursor.fetchall()]
    conn.close()

    return case_managers

def submit_enrollment(client_id, class_name, case_manager):
    # Connect to the database
    conn = sqlite3.connect('client_database.db')
    cursor = conn.cursor()

    # Update the relevant class table with the client's ID
    cursor.execute(f"INSERT INTO {class_name} (client_id) VALUES (?)", (client_id,))

    # Update the client's case manager in the clients table
    cursor.execute("UPDATE clients SET case_manager = ? WHERE id = ?", (case_manager, client_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Generate the welcome letter
    # generate_welcome_letter(client_id, class_name, case_manager)


def bulk_transition(current_window):
         
        current_window.destroy()
    
        bulk_intake()

def fetch_unenrolled_clients():
    try:
        conn = sqlite3.connect('database\central_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT client_first, client_last, age, big_three, court_ordered_groups, edu_detail, no_contacts, pro_req, gang_affiliations, gender, emp, csw, eval_needed, ssn, dob FROM clients WHERE enrolled = 0")
        
        #Print column names
        column_names = [column[0] for column in cursor.description]
        
        for index, col_name in enumerate(column_names):
             print(f"{index}: {col_name}")
        
        clients = cursor.fetchall()
        cursor.close()
        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        clients = []
        
    return clients



def trans_master_roster(current_window):
             
                current_window.destroy()
            
                master_roster_window()

def master_roster_window():
     
    roster = tkinter.Tk()
    roster.title("Master Roster")
    roster.state('zoomed')
    roster.iconbitmap(r'images\icons\futuristic.ico')

    # Create the top level menu
    menubar = tkinter.Menu(roster)

    # Create a submenu te be part of the top-level menu
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Back To Enrollment", command=lambda: back_to_enroll(roster))
    
    # Add the File menu to the menu bar
    menubar.add_cascade(label="Selection", menu=filemenu)

    # Associate the menu bar to the window
    roster.config(menu=menubar)

    # Days selection
    days_frame = ttk.LabelFrame(roster, text="Days")
    days_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    mon_day_var = tkinter.IntVar()
    tue_day_var = tkinter.IntVar()
    wed_day_var = tkinter.IntVar()
    thu_day_var = tkinter.IntVar()
    fri_day_var = tkinter.IntVar()

    mon_day = ttk.Checkbutton(days_frame, text = 'Monday', variable=mon_day_var)
    mon_day.grid(row=0, column=1, sticky="w", padx=5, pady=2)
    tue_day = ttk.Checkbutton(days_frame,text='Tuesday', variable=tue_day_var)
    tue_day.grid(row=1, column=1, sticky="w", padx=5, pady=2)
    wed_day = ttk.Checkbutton(days_frame, text='Wednesday', variable=wed_day_var)
    wed_day.grid(row=2, column=1, sticky="w", padx=5, pady=2)
    thu_day = ttk.Checkbutton(days_frame, text='Thursday', variable=thu_day_var)
    thu_day.grid(row=3, column=1, sticky="w", padx=5, pady=2)
    fri_day = ttk.Checkbutton(days_frame, text='Friday', variable=fri_day_var)
    fri_day.grid(row=4, column=1, sticky="w", padx=5, pady=2)

    days = []

    if mon_day_var.get() == 1:
        days.append('Monday')

    if tue_day_var.get() == 1:
        days.append('Tuesday')

    if wed_day_var.get() == 1:
        days.append('Wednesday')

    if thu_day_var.get() == 1:
        days.append('Thursday')

    if fri_day_var.get() == 1:
        days.append('Friday')
    

    # Daytime block frame
    daytime_frame = ttk.LabelFrame(roster, text="Daytime Block")
    daytime_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    daytime_classes = ['Education Services', 'GROWTH', 'Courage To Change', 'MRT', 'Life Skills', 'What Got Me Here', 'Employement']
    daytime_classes.sort()
    day_classes = daytime_classes

    edu_day_var = tkinter.IntVar()


    day_f_period = ttk.Label(daytime_frame, text="1st Period (12:30-1:30p)")
    day_f_period.grid(row=0, column=0, sticky="w", padx=5, pady=2)
    day_f_class = ttk.Combobox(daytime_frame, values= day_classes, state="readonly", width=15)
    day_f_class.grid(row=0, column=1, padx=5, pady=2)
    day_s_period = ttk.Label(daytime_frame, text="2nd Period (1:30-2:30p)")
    day_s_period.grid(row=1, column=0, sticky="w", padx=5, pady=2)
    day_s_class = ttk.Combobox(daytime_frame, values=day_classes, state="readonly", width=15)
    day_s_class.grid(row=1, column=1, padx=5, pady=2)
    day_e_period = ttk.Label(daytime_frame, text="Education Service (Noon-3:00p)")
    day_e_period.grid(row=2, column=0, sticky="w", padx=5, pady=2)
    day_e_class = ttk.Checkbutton(daytime_frame, text = "Education Services", variable= edu_day_var)
    day_e_class.grid(row=2, column=1, padx=5, pady=2)

    day_f = day_f_class.get()
    day_s = day_s_class.get()
    
    day_f_class.bind("<<ComboboxSelected>>", lambda event: day_f.update({day_f_class: day_f_class.get()}))
    day_s_class.bind("<<ComboboxSelected>>", lambda event: day_s.update({day_s_class: day_s_class.get()}))
    
    if edu_day_var.get() == 1:
         
         day_e = 'Education Services'

    else:
            
        day_e = ''






    evening_combos = {}

    evening_classes_frame = ttk.LabelFrame(roster, text="Evening Block")
    evening_classes_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    space_label = ttk.Label(evening_classes_frame, text=" ")
    space_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
    a_class_label = ttk.Label(evening_classes_frame, text="A")
    a_class_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
    b_class_label = ttk.Label(evening_classes_frame, text="B")
    b_class_label.grid(row=0, column=2, sticky="w", padx=5, pady=2)
    c_class_label = ttk.Label(evening_classes_frame, text="C")
    c_class_label.grid(row=0, column=3, sticky="w", padx=5, pady=2)
    edu_class_label = ttk.Label(evening_classes_frame, text="Education")
    edu_class_label.grid(row=0, column=4, sticky="w", padx=5, pady=2)
    drug_class_label = ttk.Label(evening_classes_frame, text="Drug Treatment")
    drug_class_label.grid(row=0, column=5, sticky="w", padx=5, pady=2)
    p1_label = ttk.Label(evening_classes_frame, text="1st Period")
    p1_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
    p2_label = ttk.Label(evening_classes_frame, text="2nd Period")
    p2_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
    p3_label = ttk.Label(evening_classes_frame, text="3rd Period")
    p3_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)

    get_classes = fetch_classes()
    get_classes.insert(0, " ")
    
    a1_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    a1_class.grid(row=1, column=1, padx=5, pady=2)
    a2_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    a2_class.grid(row=2, column=1, padx=5, pady=2)
    a3_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    a3_class.grid(row=3, column=1, padx=5, pady=2)
    b1_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    b1_class.grid(row=1, column=2, padx=5, pady=2)
    b2_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    b2_class.grid(row=2, column=2, padx=5, pady=2)
    b3_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    b3_class.grid(row=3, column=2, padx=5, pady=2)
    c1_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    c1_class.grid(row=1, column=3, padx=5, pady=2)
    c2_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    c2_class.grid(row=2, column=3, padx=5, pady=2)
    c3_class = ttk.Combobox(evening_classes_frame, values=get_classes, state="readonly", width=20)
    c3_class.grid(row=3, column=3, padx=5, pady=2)
    edu_class_a = ttk.Combobox(evening_classes_frame, values=[' ', 'Education Services'], state="readonly", width=20)
    edu_class_a.grid(row=1, column=4, padx=5, pady=2)
    edu_class_b = ttk.Combobox(evening_classes_frame, values=[' ', 'Education Services'], state="readonly", width=20)
    edu_class_b.grid(row=2, column=4, padx=5, pady=2)
    edu_class_c = ttk.Combobox(evening_classes_frame, values=[' ', 'Education Services'], state="readonly", width=20)
    edu_class_c.grid(row=3, column=4, padx=5, pady=2)
    drug_class_a = ttk.Combobox(evening_classes_frame, values=[' ', 'Drug Treatment'], state="readonly", width=20)
    drug_class_a.grid(row=1, column=5, padx=5, pady=2)
    drug_class_b = ttk.Combobox(evening_classes_frame, values=[' ', 'Drug Treatment'], state="readonly", width=20)
    drug_class_b.grid(row=2, column=5, padx=5, pady=2)
    drug_class_c = ttk.Combobox(evening_classes_frame, values=[' ', 'Drug Treatment'], state="readonly", width=20)
    drug_class_c.grid(row=3, column=5, padx=5, pady=2)

    def submit_schedule_clicked():
    
        days = []
    
        if mon_day_var.get() == 1:
            days.append("Monday")
        if tue_day_var.get() == 1:
            days.append("Tuesday")
        if wed_day_var.get() == 1:
            days.append("Wednesday")
        if thu_day_var.get() == 1:
            days.append("Thursday")
        if fri_day_var.get() == 1:
            days.append("Friday")

        submit_schedule(days, day_e, day_f, day_s)

            # Fetch the value of day_f_class within this function
        day_class1 = day_f_class.get()
        selected_day_classes = [day_class1, day_s_class.get()]
        selected_edu_day = edu_day_var.get()
        selected_evening_classes = [a1_class.get(), a2_class.get(), a3_class.get()]
        is_summer_time = sum_time_var.get()

        print(day_class1)

        # selected_day_classes = [day_f_class.get(), day_s_class.get()]
        # selected_edu_day = edu_day_var.get()
        # selected_evening_classes = [a1_class.get(), a2_class.get(), a3_class.get()]
        # is_summer_time = sum_time_var.get()

        

        # submit_schedule(selected_days, selected_day_classes, selected_edu_day, selected_evening_classes, is_summer_time)

    
    # Summer time adjustment checkbox
    sum_time_var = tkinter.IntVar()
    summer_chk = ttk.Checkbutton(roster, text="Adjust for Summer Time", variable=sum_time_var)
    summer_chk.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    # Submit and Clear buttons
    btn_frame = ttk.Frame(roster)
    btn_frame.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    submit_btn = ttk.Button(btn_frame, text="Submit", command=submit_schedule_clicked)
    submit_btn.grid(row=0, column=0, padx=5, pady=5)

    def fetch_group_id(group_name):
        conn = sqlite3.connect('database\central_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM groups WHERE group_name = ?", (group_name,))
        result = cursor.fetchone()
     
        return result[0] if result else None

    def fetch_roster():
             
        conn = sqlite3.connect('database\central_database.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT day, block, period, class FROM schedule where class_offered = 1")
        rows = cursor.fetchall()
        
        conn.close()
        return rows

    def update_class_offered_in_db(day, block, period, class_name, class_offered):
        conn = sqlite3.connect('database\central_database.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE schedule SET class_offered = ? WHERE day = ? AND block = ? AND period = ? AND class = ?", (class_offered, day, block, period, class_name))
        
        conn.commit()
        conn.close()

    def load_roster():
        # Clear existing items in the tree
        for item in roster_tree.get_children():
            roster_tree.delete(item)
        
        # Load the roster from the database (assuming you have a fetch_roster function)
        roster_data = fetch_roster()
        # For the sake of this example, I'll use dummy data:
        roster_data = []

        for day, daytime_class, evening_class in roster_data:
            roster_tree.insert(parent='', index='end', iid=None, text='', values=(day, daytime_class, evening_class))

    def save_to_db(day, block, period, class_name, is_summer_time, class_offered):
        conn = sqlite3.connect('database\central_database.db')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO schedule (day, block, period, class, is_summer_time, class_offered) VALUES (?, ?, ?, ?, ?, ? )", (day, block, period, class_name, is_summer_time, class_offered))
        
        conn.commit()
        conn.close()

    def submit_schedule(days, day_e, day_f, day_s):

        conn = sqlite3.connect('database\central_database.db')
        cursor = conn.cursor()

        print(days)
        print(day_e)
        print(day_f)
        print(day_s)

        for day in days:

            # roster_day = ()

            # roster_day[day] = tuple(date,day, ('Daytime_1',day_f_class.get()), ('Daytime_2',day_s_class.get()), ('Daytime_3',day_e_class.get()), ('Evening_A1',a1_class.get()), ('Evening_A2',a2_class.get()), ('Evening_A3',a3_class.get()), ('Evening_B1',b1_class.get()), ('Evening_B2',b2_class.get()), ('Evening_B3',b3_class.get()), ('Evening_C1',c1_class.get()), ('Evening_C2',c2_class.get()), ('Evening_C3',c3_class.get()), ('Evening_Edu_A',edu_class_a.get()), ('Evening_Edu_B',edu_class_b.get()), ('Evening_Edu_C',edu_class_c.get()), ('Evening_Drug_A',drug_class_a.get()), ('Evening_Drug_B',drug_class_b.get()), ('Evening_Drug_C',drug_class_c.get()))

            print(day)

            



        



        # cursor.execute("INSERT INTO schedule (date_schedule_made, day, ) VALUES (?, ? )", (date, day))






        # load_roster()
        # messagebox.showinfo("Info", "Schedule submitted successfully!")

    # # Iterate through each day and save the selected classes for that day
    #     for idx, day in enumerate(days):
    #         if days_vars[idx].get():
    #             if idx < len(class_combos):
    #                 daytime_class = class_combos[idx].get()

    #                 if not daytime_class:
    #                     # This means the user removed the class from the combobox. Update the DB to set classes_offered to 0.
    #                     update_class_offered_in_db(day, 'Daytime', daytime_periods[idx], daytime_class, 0)
    #                 else:
    #                     # Otherwise, save or update the class in the DB.
    #                     save_to_db(day, 'Daytime', daytime_periods[idx], daytime_class, summer_time_var.get(), 1)
        #     for idx, day in enumerate(days):
        #         if days_vars[idx].get():
        #             for period_idx, period in enumerate(daytime_periods):
        #                 daytime_class = class_combos[idx*len(daytime_periods) + period_idx].get()
        #                 if daytime_class:  # if there's a class selected
        #                     save_to_db(day, 'Daytime', period, daytime_class, summer_time_var.get(), 1)

        # starting_index_for_evening = len(daytime_periods)  # number of daytime comboboxes

        # # Iterate through each evening period and save the selected classes for that period
        # for idx, day in enumerate(days):
        #     if days_vars[idx].get():
        #         daytime_class = class_combos[idx].get()

        #         for j, period in enumerate(evening_periods):
                    
        #             index = starting_index_for_evening + j*5 + idx
        #             class_name = class_combos[index].get()  # Adjust this index logic according to your comboboxes' order

        #             if not class_name:
        #                 # This means the user removed the class from the combobox. Update the DB to set classes_offered to 0.
        #                 update_class_offered_in_db(day, 'Evening', period, class_name, 0)
        #             else:
        #                 # Otherwise, save or update the class in the DB.
        #                 save_to_db(day, 'Evening', period, class_name, summer_time_var.get(), 1)
                
        # # Load the roster from the database
        # load_roster()

        # messagebox.showinfo("Info", "Schedule submitted successfully!")

    def clear_schedule():
        print("Clearing schedule")



    clear_btn = ttk.Button(btn_frame, text="Clear", command=clear_schedule)
    clear_btn.grid(row=0, column=1, padx=5, pady=5)

    # Roster Display
    roster_frame = ttk.LabelFrame(roster, text="Roster")
    roster_frame.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

    # Create a Treeview widget
    roster_tree = ttk.Treeview(roster_frame)
    roster_tree.pack()

    # Configure the Treeview widget
    roster_tree['columns'] = ('Day', 'Daytime Block', 'Evening Block')
    roster_tree.column('#0', width=0, stretch='no')
    roster_tree.column('Day', anchor='center', width=100)
    roster_tree.column('Daytime Block', anchor='center', width=100)
    roster_tree.column('Evening Block', anchor='center', width=100)




    # Start the tkinter mainloop
    roster.mainloop()

def client_enrollment_window():
    # Create a new tkinter window
    window = tkinter.Tk()
    window.title("Client Enrollment")
    window.configure(bg='#483D8B')
    window.state('zoomed')

    listbox = tkinter.Listbox(window, bg="#6E63A6",            # Background color
                     fg="#EAE6F2",            # Text color
                     selectbackground="#8B77CF",   # Background color of selected item
                     selectforeground="#2C2752",
                     highlightbackground="#EAE6F2",
                     highlightcolor="#8B77CF",
                     bd=0,
                     highlightthickness=0, font=('Arial', 16), width=30)   # Text color of selected item
    
    listbox.grid(row = 4, column= 0, sticky = 'e')

    # Create a top-level menu
    menubar = tkinter.Menu(window)

    # Create a submenu te be part of the top-level menu
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Client Intake (Individual)", command= lambda: sp_trans_ind(window))
    filemenu.add_command(label="Client Intake (Bulk)", command=lambda: cm_trans_bulk(window))
    filemenu.add_command(label="Master Roster", command=lambda: trans_master_roster(window))
    filemenu.add_command(label="Go Back", command=lambda: back_to_cm(window))

    # Add the File menu to the menu bar
    menubar.add_cascade(label="Selection", menu=filemenu)

    # Associate the menu bar to the window
    window.config(menu=menubar)

    img = Image.open(r'images\first_day.png')
    img = img.resize((500, 500), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    # Here the image label is created
    enroll_image = tkinter.Label(window, image=img, bg='#483D8B')
    enroll_image.image = img
    
     # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Assuming the size of the image is (500, 500) as specified earlier
    img_width = 500
    img_height = 500

    # Calculate the center position
    x = (screen_width / 2) - (img_width / 2)
    y = (screen_height / 2) - (img_height / 2)

    # Place the image at the center
    enroll_image.place(x=x, y=y)

    # Fetch unenrolled clients from the database
    unenrolled_clients = fetch_unenrolled_clients()

    # Populate Listbox
    for client in unenrolled_clients:

        capitalized_name = f"{client[0]} {client[1]}".title()

        listbox.insert(tkinter.END, f"{capitalized_name}") 

    # Bind double click to the listbox
    listbox.bind("<Double-Button-1>", lambda event: show_client_info(window,listbox, unenrolled_clients))

    # profile_outer_frame = tkinter.LabelFrame(window, text='Client Profile', padx = 10, pady = 10)
    # profile_outer_frame.grid(row = 0, column = 1, pady = 0, padx = 0, sticky = 'nsew')

    # global profile_inner_frame

    # profile_inner_frame = tkinter.LabelFrame(profile_outer_frame, padx = 10, pady = 10)
    # profile_inner_frame.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'nsew')

    # global treatment_frame
    # treatment_frame = tkinter.LabelFrame(profile_outer_frame, text='Drug Treatment', padx = 10, pady = 10)
    # treatment_frame.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'nsew')

    # Add a button to submit the form

    # Fetch available classes and case managers from the database
    classes = fetch_classes()  # Replace with your function to fetch classes
    case_managers = fetch_case_managers()  # Replace with your function to fetch case managers

    

    window.mainloop()

def show_client_info(window, listbox, unenrolled_clients):

    def days_until_birthday(dob_str):
        """Return the number of days until next birthday."""
        
        # Try to parse the DOB string using the hyphen format
        try:
            dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            # If that fails, try the slash format
            dob = datetime.datetime.strptime(dob_str, '%Y/%m/%d').date()
        
        month, day = dob.month, dob.day
        today = datetime.date.today()
        this_year_birthday = datetime.date(today.year, month, day)
        
        # If the birthday has already passed this year, set it for next year
        if today > this_year_birthday:
            this_year_birthday = datetime.date(today.year + 1, month, day)
        
        # Calculate the difference in days
        delta = this_year_birthday - today
        return delta.days

    select_index = listbox.curselection()[0]

    # Get the position of the previous window
    prev_window_x = window.winfo_x()
    prev_window_y = window.winfo_y()

    window.destroy()

    def boolean_parser(variable):
        if variable == 1:
            return 'Yes'
        else:
            return 'No'

    # Create main window
    schedule_window = tkinter.Tk()
    schedule_window.title("Class Schedule")
    schedule_window.state('zoomed')

    offset_x = 20  # adjust as needed
    offset_y = 20  # adjust as needed
    schedule_window.geometry(f"+{prev_window_x + offset_x}+{prev_window_y + offset_y}")

    schedule_window.iconbitmap(r'images\icons\futuristic.ico')

    # Create a top-level menu
    menubar = tkinter.Menu(schedule_window)

    # Create a submenu te be part of the top-level menu
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Go Back", command= lambda: back_to_enroll(schedule_window))
    filemenu.add_command(label="Client Management Menu", command=lambda: back_to_cm(schedule_window))

    # Add the File menu to the menu bar
    menubar.add_cascade(label="Selection", menu=filemenu)

    # Associate the menu bar to the window
    schedule_window.config(menu=menubar)

    selected_client = unenrolled_clients[select_index]

    # Create frames

    client_frame = tkinter.LabelFrame(schedule_window, text="Client Information", padx=10, pady=10)
    client_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    drug_treatment_frame = tkinter.LabelFrame(schedule_window, text="Drug Treatment", padx=10, pady=10)
    drug_treatment_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

    proj_frame = tkinter.LabelFrame(schedule_window, text="Program Information", padx=10, pady=10)
    proj_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

    monday_frame = tkinter.LabelFrame(schedule_window, text="Monday", padx=10, pady=10)
    monday_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

    tuesday_frame = tkinter.LabelFrame(schedule_window, text="Tuesday", padx=10, pady=10)
    tuesday_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

    wednesday_frame = tkinter.LabelFrame(schedule_window, text="Wednesday", padx=10, pady=10)
    wednesday_frame.grid(row=1, column=2, padx=0, pady=0, sticky="nsew")

    thursday_frame = tkinter.LabelFrame(schedule_window, text="Thursday", padx=10, pady=10)
    thursday_frame.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

    friday_frame = tkinter.LabelFrame(schedule_window, text="Friday", padx=10, pady=10)
    friday_frame.grid(row=2, column=1, padx=0, pady=0, sticky="nsew")

    submit_frame = tkinter.LabelFrame(schedule_window,text="Enroll Client", padx=10, pady=10)
    submit_frame.grid(row=2, column=2, padx=0, pady=0, sticky="nsew")

    # Client Frame
    full_name = f"{selected_client[0]} {selected_client[1]}".title()

    name_label = tkinter.Label(client_frame, text=f"Name: {full_name}")
    name_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')

    age_label = tkinter.Label(client_frame, text=f"Age: {selected_client[2]} ({days_until_birthday(selected_client[14])} Days till next birthday)")
    age_label.grid(row = 0, column = 1, pady = 0, padx = 0, sticky = 'w')

    gender_label = tkinter.Label(client_frame, text= f"Gender: {selected_client[9]}")
    gender_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')

    big_three_label = tkinter.Label(client_frame, text=f"Big Three Total: {selected_client[3]}")
    big_three_label.grid(row = 1, column = 1, pady = 0, padx = 0, sticky = 'w')

    court_ordered_groups_label = tkinter.Label(client_frame, text=f"Court Ordered Groups: {selected_client[4]}")
    court_ordered_groups_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')

    gang_affiliations_label = tkinter.Label(client_frame, text=f"Gang Affiliations: {selected_client[8]}")
    gang_affiliations_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')

    no_contacts_label = tkinter.Label(client_frame, text=f"No Contact Orders: {selected_client[6]}")
    no_contacts_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')

    # Drug Treatment Frame

    if selected_client[12] == 1:
        drug_treatment_label = tkinter.Label(drug_treatment_frame, text=f"Drug/Alcohol Evaluation Requested: Yes")
        drug_treatment_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
        ssn_label = tkinter.Label(drug_treatment_frame, text=f"SSN: {selected_client[13]}")
        ssn_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')
        projeceted_start_date_label = tkinter.Label(drug_treatment_frame, text=f"Projected Start Date: ")
        projeceted_start_date_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')
        pro_sd_entry = tkinter.Entry(drug_treatment_frame, width=30)
        pro_sd_entry.grid(row = 2, column = 1, pady = 0, padx = 0, sticky = 'w')


    else:
        drug_treatment_label = tkinter.Label(drug_treatment_frame, text=f"Drug/Alcohol Evaluation Requested:No")
        drug_treatment_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')

    def get_selected_date():
        selected_date = cal.get_date()
        print("Selected date:", selected_date)

# Function to highlight the dates
    def highlight_dates(event):
        selected_date = cal.selection_get()
        today = date.today()
        
        for child in cal.children.values():
            if isinstance(child, ttk.Button):
                selected_date = child["text"]
                
            # If the button's date is today, always apply the "Today.TButton" style.
            elif selected_date == str(today.day):
                child.configure(style="Today.TButton")
            # If the button's date is the selected date (and it's not today), apply the "Selected.TButton" style.
            elif selected_date == str(selected_date.day) and selected_date != str(today.day):
                child.configure(style="Selected.TButton")
            # Otherwise, apply the default style.
            else:
                child.configure(style="TButton")

    def get_selected_date(DateEntry):
        selected_date = cal.get_date()
        print("Selected date:", selected_date)
        
        # Get the current date from prog_start_entry
        date = selected_date

        formatted_date = date.strftime('%A %B %d, %Y')

        # Set this date to pro_sd_entry
        pro_sd_entry.delete(0, 'end')
        pro_sd_entry.insert(0, formatted_date)  

    projeceted_start_date = tkinter.Label(proj_frame, text="Projected Start Date: ")
    projeceted_start_date.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')

    

    cal = DateEntry(proj_frame, selectmode="day")
    cal.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    date = cal.get_date()

    style = ttk.Style()
    style.configure("Today.TButton", background="yellow")

    today = cal.get_date()
    print(today)

    calendar_instance = cal._calendar

    today = datetime.date.today()
    calendar_instance.calevent_create(today, "Today", "current")
    calendar_instance.tag_config("current", background="yellow", foreground="black")
    
    # highlight_dates(None)

    cal.bind("<<DateEntrySelected>>", get_selected_date)

    csw_label = tkinter.Label(proj_frame, text=f"CSW: {boolean_parser(selected_client[11])}")
    csw_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')

    emp_label = tkinter.Label(proj_frame, text=f"Employment: {boolean_parser(selected_client[10])}")
    emp_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')

    edu_label = tkinter.Label(proj_frame, text=f"Education: {selected_client[5]}")
    edu_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')

    iso_requested_label = tkinter.Label(proj_frame, text=f"ISO Requested Groups: {selected_client[7]}")
    iso_requested_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')

    # Groups

    dt_groups = ["growth", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"]
    dt_groups.sort()
    daytime_groups = dt_groups

    # Monday Frame
    daytime_label = tkinter.Label(monday_frame, text="Daytime Groups", font=('bold'))
    daytime_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_label = tkinter.Label(monday_frame, text="1st Period: ")
    fdaytime_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_entry = ttk.Combobox(monday_frame, width=30, values= daytime_groups)
    fdaytime_entry.grid(row = 1, column = 1, pady = 0, padx = 0, sticky = 'w')
    sdaytime_label = tkinter.Label(monday_frame, text="2nd Period: ")
    sdaytime_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')
    sdaytime_entry = ttk.Combobox(monday_frame, width=30, values= daytime_groups)
    sdaytime_entry.grid(row = 2, column = 1, pady = 0, padx = 0, sticky = 'w')
    edu_label = tkinter.Label(monday_frame, text="Education: ")
    edu_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')
    edu_entry = ttk.Combobox(monday_frame, width=30, values = ["Noon-3pm", "1:30pm-3pm"])
    edu_entry.grid(row = 3, column = 1, pady = 0, padx = 0, sticky = 'w')
    space_label = tkinter.Label(monday_frame, text=" ")
    space_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')
    evening_label = tkinter.Label(monday_frame, text="Evening Groups", font=('bold'))
    evening_label.grid(row = 5, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_label = tkinter.Label(monday_frame, text="1st Period: ")
    fevening_label.grid(row = 6, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_entry = ttk.Combobox(monday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    fevening_entry.grid(row = 6, column = 1, pady = 0, padx = 0, sticky = 'w')
    seveing_label = tkinter.Label(monday_frame, text="2nd Period: ")
    seveing_label.grid(row = 7, column = 0, pady = 0, padx = 0, sticky = 'w')
    seveing_entry = ttk.Combobox(monday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    seveing_entry.grid(row = 7, column = 1, pady = 0, padx = 0, sticky = 'w')
    teveing_label = tkinter.Label(monday_frame, text="3rd Period: ")
    teveing_label.grid(row = 8, column = 0, pady = 0, padx = 0, sticky = 'w')
    teveing_entry = ttk.Combobox(monday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    teveing_entry.grid(row = 8, column = 1, pady = 0, padx = 0, sticky = 'w')

    # Tuesday Frame
    daytime_label = tkinter.Label(tuesday_frame, text="Daytime Groups", font=('bold'))
    daytime_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_label = tkinter.Label(tuesday_frame, text="1st Period: ")
    fdaytime_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_entry = ttk.Combobox(tuesday_frame, width=30, values= daytime_groups)
    fdaytime_entry.grid(row = 1, column = 1, pady = 0, padx = 0, sticky = 'w')
    sdaytime_label = tkinter.Label(tuesday_frame, text="2nd Period: ")
    sdaytime_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')
    sdaytime_entry = ttk.Combobox(tuesday_frame, width=30, values= daytime_groups)
    sdaytime_entry.grid(row = 2, column = 1, pady = 0, padx = 0, sticky = 'w')
    edu_label = tkinter.Label(tuesday_frame, text="Education: ")
    edu_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')
    edu_entry = ttk.Combobox(tuesday_frame, width=30, values = ["Noon-3pm", "1:30pm-3pm"])
    edu_entry.grid(row = 3, column = 1, pady = 0, padx = 0, sticky = 'w')
    space_label = tkinter.Label(tuesday_frame, text=" ")
    space_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')
    evening_label = tkinter.Label(tuesday_frame, text="Evening Groups", font=('bold'))
    evening_label.grid(row = 5, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_label = tkinter.Label(tuesday_frame, text="1st Period: ")
    fevening_label.grid(row = 6, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_entry = ttk.Combobox(tuesday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    fevening_entry.grid(row = 6, column = 1, pady = 0, padx = 0, sticky = 'w')
    seveing_label = tkinter.Label(tuesday_frame, text="2nd Period: ")
    seveing_label.grid(row = 7, column = 0, pady = 0, padx = 0, sticky = 'w')
    seveing_entry = ttk.Combobox(tuesday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    seveing_entry.grid(row = 7, column = 1, pady = 0, padx = 0, sticky = 'w')
    teveing_label = tkinter.Label(tuesday_frame, text="3rd Period: ")
    teveing_label.grid(row = 8, column = 0, pady = 0, padx = 0, sticky = 'w')
    teveing_entry = ttk.Combobox(tuesday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    teveing_entry.grid(row = 8, column = 1, pady = 0, padx = 0, sticky = 'w')

    # Wednesday Frame
    daytime_label = tkinter.Label(wednesday_frame, text="Daytime Groups", font=('bold'))
    daytime_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_label = tkinter.Label(wednesday_frame, text="1st Period: ")
    fdaytime_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_entry = ttk.Combobox(wednesday_frame, width=30, values= daytime_groups)
    fdaytime_entry.grid(row = 1, column = 1, pady = 0, padx = 0, sticky = 'w')
    sdaytime_label = tkinter.Label(wednesday_frame, text="2nd Period: ")
    sdaytime_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')
    sdaytime_entry = ttk.Combobox(wednesday_frame, width=30, values= daytime_groups)
    sdaytime_entry.grid(row = 2, column = 1, pady = 0, padx = 0, sticky = 'w')
    edu_label = tkinter.Label(wednesday_frame, text="Education: ")
    edu_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')
    edu_entry = ttk.Combobox(wednesday_frame, width=30, values = ["Noon-3pm", "1:30pm-3pm"])
    edu_entry.grid(row = 3, column = 1, pady = 0, padx = 0, sticky = 'w')
    space_label = tkinter.Label(wednesday_frame, text=" ")
    space_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')
    evening_label = tkinter.Label(wednesday_frame, text="Evening Groups", font=('bold'))
    evening_label.grid(row = 5, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_label = tkinter.Label(wednesday_frame, text="1st Period: ")
    fevening_label.grid(row = 6, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_entry = ttk.Combobox(wednesday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    fevening_entry.grid(row = 6, column = 1, pady = 0, padx = 0, sticky = 'w')
    seveing_label = tkinter.Label(wednesday_frame, text="2nd Period: ")
    seveing_label.grid(row = 7, column = 0, pady = 0, padx = 0, sticky = 'w')
    seveing_entry = ttk.Combobox(wednesday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    seveing_entry.grid(row = 7, column = 1, pady = 0, padx = 0, sticky = 'w')
    teveing_label = tkinter.Label(wednesday_frame, text="3rd Period: ")
    teveing_label.grid(row = 8, column = 0, pady = 0, padx = 0, sticky = 'w')
    teveing_entry = ttk.Combobox(wednesday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    teveing_entry.grid(row = 8, column = 1, pady = 0, padx = 0, sticky = 'w')

    # Thursday Frame
    daytime_label = tkinter.Label(thursday_frame, text="Daytime Groups", font=('bold'))
    daytime_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_label = tkinter.Label(thursday_frame, text="1st Period: ")
    fdaytime_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_entry = ttk.Combobox(thursday_frame, width=30, values= daytime_groups)
    fdaytime_entry.grid(row = 1, column = 1, pady = 0, padx = 0, sticky = 'w')
    sdaytime_label = tkinter.Label(thursday_frame, text="2nd Period: ")
    sdaytime_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')
    sdaytime_entry = ttk.Combobox(thursday_frame, width=30, values= daytime_groups)
    sdaytime_entry.grid(row = 2, column = 1, pady = 0, padx = 0, sticky = 'w')
    edu_label = tkinter.Label(thursday_frame, text="Education: ")
    edu_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')
    edu_entry = ttk.Combobox(thursday_frame, width=30, values = ["Noon-3pm", "1:30pm-3pm"])
    edu_entry.grid(row = 3, column = 1, pady = 0, padx = 0, sticky = 'w')
    space_label = tkinter.Label(thursday_frame, text=" ")
    space_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')
    evening_label = tkinter.Label(thursday_frame, text="Evening Groups", font=('bold'))
    evening_label.grid(row = 5, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_label = tkinter.Label(thursday_frame, text="1st Period: ")
    fevening_label.grid(row = 6, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_entry = ttk.Combobox(thursday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    fevening_entry.grid(row = 6, column = 1, pady = 0, padx = 0, sticky = 'w')
    seveing_label = tkinter.Label(thursday_frame, text="2nd Period: ")
    seveing_label.grid(row = 7, column = 0, pady = 0, padx = 0, sticky = 'w')
    seveing_entry = ttk.Combobox(thursday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    seveing_entry.grid(row = 7, column = 1, pady = 0, padx = 0, sticky = 'w')
    teveing_label = tkinter.Label(thursday_frame, text="3rd Period: ")
    teveing_label.grid(row = 8, column = 0, pady = 0, padx = 0, sticky = 'w')
    teveing_entry = ttk.Combobox(thursday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    teveing_entry.grid(row = 8, column = 1, pady = 0, padx = 0, sticky = 'w')

    # Friday Frame
    daytime_label = tkinter.Label(friday_frame, text="Daytime Groups", font=('bold'))
    daytime_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_label = tkinter.Label(friday_frame, text="1st Period: ")
    fdaytime_label.grid(row = 1, column = 0, pady = 0, padx = 0, sticky = 'w')
    fdaytime_entry = ttk.Combobox(friday_frame, width=30, values= daytime_groups)
    fdaytime_entry.grid(row = 1, column = 1, pady = 0, padx = 0, sticky = 'w')
    sdaytime_label = tkinter.Label(friday_frame, text="2nd Period: ")
    sdaytime_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')
    sdaytime_entry = ttk.Combobox(friday_frame, width=30, values= daytime_groups)
    sdaytime_entry.grid(row = 2, column = 1, pady = 0, padx = 0, sticky = 'w')
    edu_label = tkinter.Label(friday_frame, text="Education: ")
    edu_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')
    edu_entry = ttk.Combobox(friday_frame, width=30, values = ["Noon-3pm", "1:30pm-3pm"])
    edu_entry.grid(row = 3, column = 1, pady = 0, padx = 0, sticky = 'w')
    space_label = tkinter.Label(friday_frame, text=" ")
    space_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')
    evening_label = tkinter.Label(friday_frame, text="Evening Groups", font=('bold'))
    evening_label.grid(row = 5, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_label = tkinter.Label(friday_frame, text="1st Period: ")
    fevening_label.grid(row = 6, column = 0, pady = 0, padx = 0, sticky = 'w')
    fevening_entry = ttk.Combobox(friday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    fevening_entry.grid(row = 6, column = 1, pady = 0, padx = 0, sticky = 'w')
    seveing_label = tkinter.Label(friday_frame, text="2nd Period: ")
    seveing_label.grid(row = 7, column = 0, pady = 0, padx = 0, sticky = 'w')
    seveing_entry = ttk.Combobox(friday_frame, width=30, values= ["set up master roster function", "ls", "wgmh", "pym", "ua", "ss", "gc", "bc", "mrt", "crt"])
    seveing_entry.grid(row = 7, column = 1, pady = 0, padx = 0, sticky = 'w')

    # Submit Frame

    cm = fetch_case_managers()
    cm.sort()
    case_managers = cm


    assign_cm_label = tkinter.Label(submit_frame, text="Assign Case Manager: ")
    assign_cm_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
    assign_cm_entry = ttk.Combobox(submit_frame, width=30, values= case_managers)
    assign_cm_entry.grid(row = 0, column = 1, pady = 0, padx = 0, sticky = 'w')
    space_label = tkinter.Label(submit_frame, text=" ")
    space_label.grid(row = 1, column = 1, pady = 0, padx = 0, sticky = 'w')
    submit_button = tkinter.Button(submit_frame, text="Enroll and Generate Letter", command=lambda: print(assign_cm_entry.get()))
    submit_button.grid(row = 2, column = 1, pady = 0, padx = 0, sticky = 'w')






    

 
    
    # submit_button = tkinter.Button(schedule_window, text="Enroll and Generate Letter", command=lambda: print("Enroll and Generate Letter"))
    # submit_button.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')

    # schedule_window.mainloop()


# client_enrollment_window()

    # client_profile_window = tkinter.Tk()
    # client_profile_window.title("Client Profile")
    # client_profile_window.configure(bg='#483D8B')
    # client_profile_window.state('zoomed')





     # Create widgets for client details



    





    # num_str = str(selected_client[13])
    # formatted_str = num_str[0:3] + "-" + num_str[3:5] + "-" + num_str[5:]

    
    # dob_label = tkinter.Label(profile_inner_frame, text=f"Age: {selected_client[2]}")
    # big_three_label = tkinter.Label(profile_inner_frame, text=f"Big Three Total: {selected_client[3]}")
    # court_ordered_groups_label = tkinter.Label(profile_inner_frame, text=f"Court Ordered Groups: {selected_client[4]}")
    # edu_detail_label = tkinter.Label(profile_inner_frame, text=f"Needed Education Services: {selected_client[5]}")
    # no_contacts_label = tkinter.Label(profile_inner_frame, text=f"No Contact Orders: {selected_client[6]}")
    # pro_req_label = tkinter.Label(profile_inner_frame, text=f"ISO Requested Groups: {selected_client[7]}")
    # gang_affiliations_label = tkinter.Label(profile_inner_frame, text=f"Gang Affiliations: {selected_client[8]}")
    # gender_lable = tkinter.Label(profile_inner_frame, text=f"Gender: {selected_client[9]}")
    # emp_label = tkinter.Label(profile_inner_frame, text=f"Employment: {emp_needed_text}")
    # csw_label = tkinter.Label(profile_inner_frame, text=f"CSW: {csw_needed_text}")
    # eval_needed_label = tkinter.Label(profile_inner_frame, text=f"Drug/Alcohol Evaluation Requested: {eval_needed_text}")

    # # Place widgets
    
    # dob_label.grid(row = 2, column = 0, pady = 0, padx = 0, sticky = 'w')
    # big_three_label.grid(row = 3, column = 0, pady = 0, padx = 0, sticky = 'w')
    # court_ordered_groups_label.grid(row = 4, column = 0, pady = 0, padx = 0, sticky = 'w')
    # edu_detail_label.grid(row = 5, column = 0, pady = 0, padx = 0, sticky = 'w')
    # no_contacts_label.grid(row = 6, column = 0, pady = 0, padx = 0, sticky = 'w')
    # pro_req_label.grid(row = 7, column = 0, pady = 0, padx = 0, sticky = 'w')
    # gang_affiliations_label.grid(row = 8, column = 0, pady = 0, padx = 0, sticky = 'w')
    # gender_lable.grid(row = 9, column = 0, pady = 0, padx = 0, sticky = 'w')
    # emp_label.grid(row = 10, column = 0, pady = 0, padx = 0, sticky = 'w')
    # csw_label.grid(row = 11, column = 0, pady = 0, padx = 0, sticky = 'w')
    # eval_needed_label.grid(row = 12, column = 0, pady = 0, padx = 0, sticky = 'w')


def create_client_row(window, client, classes, case_managers):
    # Create widgets for client details
    id_label = tkinter.Label(window, text=f"ID: {client[0]}")
    name_label = tkinter.Label(window, text=f"Name: {client[1]} {client[2]}")

    # Create widgets for class enrollment and case manager assignment
    class_label = tkinter.Label(window, text="Class")
    class_combo = ttk.Combobox(window, values=classes)

    case_manager_label = tkinter.Label(window, text="Case Manager")
    case_manager_combo = ttk.Combobox(window, values=case_managers)

    # Add a button to submit the form
    # submit_button = tkinter.Button(window, text="Enroll and Generate Letter", command=lambda: submit_enrollment(client[0], class_combo.get(), case_manager_combo.get()))

    # Return all widgets
   # return id_label, name_label, class_label, class_combo, case_manager_label, case_manager_combo, submit_button

def sp_trans_enroll(current_window):
      
      current_window.destroy()
    
      client_enrollment_window()


# sp_cm_menu()



# def clear_schedule():
   # class_combos = [monday_class_combo, tuesday_class_combo, wednesday_class_combo, thursday_class_combo, friday_class_combo]



    # Clear comboboxes
   # for combo in class_combos:
     #   combo.set('')
    
    # Clear projected start date entry
    # projected_start_date_entry.delete(0, tkinter.END)



##### Take from here down
# def roster():


#     # Placeholder for the class dropdowns
#     classes = ["Class A", "Class B", "Class C", "Class D"]

#     days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
#     class_combos = []

#     schedule_window = tkinter.Tk()

#     for idx, day in enumerate(days):
#         day_frame = ttk.LabelFrame(schedule_window, text=day)
#         day_frame.grid(row=idx, column=0, padx=10, pady=10, sticky="w")
        
#         daytime_periods = ["1st Period (12:30-1:30 PM)", "2nd Period (1:30-2:30 PM)", "Education Services (Noon-3 PM)"]
#         for i, period in enumerate(daytime_periods):
#             lbl = ttk.Label(day_frame, text=period)
#             lbl.grid(row=i, column=0, sticky="w", padx=5, pady=2)
#             class_combo = ttk.Combobox(day_frame, values=classes, state="readonly", width=15)
#             class_combo.grid(row=i, column=1, padx=5, pady=2)
#             class_combos.append(class_combo)
        
#         evening_periods = ["1st Period", "2nd Period", "3rd Period"]
#         for i, period in enumerate(evening_periods):
#             lbl = ttk.Label(day_frame, text=period)
#             lbl.grid(row=i + len(daytime_periods), column=0, sticky="w", padx=5, pady=2)
#             class_combo = ttk.Combobox(day_frame, values=classes, state="readonly", width=15)
#             class_combo.grid(row=i + len(daytime_periods), column=1, padx=5, pady=2)
#             class_combos.append(class_combo)

#     # Projected start date
#     projected_start_date_label = ttk.Label(schedule_window, text="Projected Start Date:")
#     projected_start_date_label.grid(row=5, column=2, padx=10, pady=5, sticky="e")  # Align label to the right

#     projected_start_date_entry = ttk.Entry(schedule_window)
#     projected_start_date_entry.grid(row=5, column=3, padx=10, pady=5, sticky="w")  # Align entry to the left



#     # Uncomment the below lines if you have tkcalendar installed
#     cal = Calendar(schedule_window, selectmode="day")
#     cal.grid(row=6, column=0, padx=10, pady=5, sticky="w")

#     # Submit and Clear buttons
#     btn_frame = ttk.Frame(schedule_window)
#     btn_frame.grid(row=7, column=0, padx=10, pady=10, sticky="w")

#     submit_btn = ttk.Button(btn_frame, text="Submit", command=submit_schedule)
#     submit_btn.grid(row=0, column=0, padx=5, pady=5)

#     clear_btn = ttk.Button(btn_frame, text="Clear", command=clear_schedule)
#     clear_btn.grid(row=0, column=1, padx=5, pady=5)

#     # Start the tkinter mainloop
#     schedule_window.mainloop()

# roster()

# if __name__ == "__main__":
#         sp_cm_menu()

#     #     roster()

#     # client_enrollment_window()

#     # # Create widgets for client details
#     # id_label = tkinter.Label(profile_inner_frame, text=f"ID: {client[0]}")
#     # name_label = tkinter.Label(profile_inner_frame, text=f"Name: {client[1]} {client[2]}")
#     # dob_label = tkinter.Label(profile_inner_frame, text=f"DOB: {client[3]}")

#     # id_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'nsew')

#     # # Create widgets for class enrollment and case manager assignment
#     # class_label = tkinter.Label(profile_inner_frame, text="Class")
#     # class_combo = ttk.Combobox(profile_inner_frame, values= fetch_classes())
#     # case_manager_label = tkinter.Label(profile_inner_frame, text="Case Manager")
#     # case_manager_combo = ttk.Combobox(profile_inner_frame, values=fetch_case_managers())


#     # # Create widget for drug treatment box
#     # if selected_client[12] == 1:
#     #     drug_treatment_label = tkinter.Label(treatment_frame, text="Assesment Requested: Yes")
#     #     ssn_label = tkinter.Label(treatment_frame, text= f"SSN: {formatted_str}")
#     #     drug_treatment_label.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'w')
#     #     ssn_label.grid(row = 1, column = 0, sticky= 'w')

#     # else:
#     #     drug_treatment_label = tkinter.Label(treatment_frame, text="Assesment Requested: No")
         

#     # # Create widgets for class enrollment and case manager assignment
#     # class_label = tkinter.Label(profile_inner_frame, text="Class")
#     # class_combo = ttk.Combobox(profile_inner_frame, values= fetch_classes())
#     # case_manager_label = tkinter.Label(profile_inner_frame, text="Case Manager")
#     # case_manager_combo = ttk.Combobox(profile_inner_frame, values=fetch_case_managers())

#     # # Add a button to submit the form
#     # submit_button = tkinter.Button(profile_inner_frame, text="Enroll and Generate Letter", command=lambda: submit_enrollment(client[0], class_combo.get(), case_manager_combo.get()))