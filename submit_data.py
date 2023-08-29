import tkinter
from tkinter import messagebox, ttk, StringVar, Entry
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3
import os
import win32com.client as client
from aspire_functions import ind_transition_bulk

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB_Path = 'database/central_database.db'

# Create the main ind_window
ind_window = tkinter.Tk()
ind_window.title("Add Client Manually")
ind_window.geometry('1200x900')
ind_window.configure(bg='#f0f0f0')
ind_window.iconbitmap('.\images\icons\\futuristic.ico')
ind_window.state('zoomed')

# Create frames for different sections
personal_info_frame = tkinter.LabelFrame(ind_window, text="Client Information", padx=10, pady=10)
personal_info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

parent_info_frame = tkinter.LabelFrame(ind_window, text="Primary Parent/Guardian Contact", padx=10, pady=10)
parent_info_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

parent_info2_frame = tkinter.LabelFrame(ind_window, text="Auxilary Parent/Guardian Contact", padx=10, pady=10)
parent_info2_frame.grid(row=0, column=3, padx=20, pady=20, sticky="nsew")

other_info_frame = tkinter.LabelFrame(ind_window, text="Other Information", padx=10, pady=10)
other_info_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=2, sticky="nsew")

drug_treatment_frame = tkinter.LabelFrame(ind_window, text="Drug Treatment (Skip if no treatment)", padx=10, pady=10)
drug_treatment_frame.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

button_frame = tkinter.Frame(ind_window, padx=10, pady=10)
button_frame.grid(row=3, column=0, columnspan=4, pady=20, sticky="nsew")

# Create the top level menu
menubar = tkinter.Menu(ind_window)

# Create a submenu te be part of the top-level menu
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Client Intake (Bulk)", command=lambda: ind_transition_bulk(ind_window))

# Add the File menu to the menu bar
menubar.add_cascade(label="Selection", menu=filemenu)

# Associate the menu bar to the window
ind_window.config(menu=menubar)

def get_officer_id(officer):
    # Connect to the SQLite database
    conn = sqlite3.connect('database/central_database.db')
    cursor = conn.cursor()

    # Query the ID of the officer with the given name
    query = "SELECT id FROM probation_officers WHERE officer_full_name = ?"
    cursor.execute(query, (officer,))
    officer_id = cursor.fetchone()

    # Close the connection
    cursor.close()
    conn.close()

    # Return the ID (or None if not found)
    return officer_id[0] if officer_id else None

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

def validate_ssn(ssn):
    if len(ssn) != 9:
        return False
    elif len(ssn) == 9:
        return True
    
def ind_client():

    # Create labels, entries, and combos inside personal_info_frame
    # Example:
    athena_label = tkinter.Label(personal_info_frame, text="Athena:")
    athena_label.grid(row=0, column=0, padx=5, pady=5)
    athena_entry = tkinter.Entry(personal_info_frame)
    athena_entry.grid(row=0, column=1, padx=5, pady=5)
    client_first_label = tkinter.Label(personal_info_frame, text="First Name:")
    client_first_label.grid(row=1, column=0, padx=5, pady=5)
    client_last_label = tkinter.Label(personal_info_frame, text="Last Name:")
    client_last_label.grid(row=2, column=0, padx=5, pady=5)
    client_first_entry = tkinter.Entry(personal_info_frame)
    client_first_entry.grid(row=1, column=1, padx=5, pady=5)
    client_last_entry = tkinter.Entry(personal_info_frame)
    client_last_entry.grid(row=2, column=1, padx=5, pady=5)
    dob_label = tkinter.Label(personal_info_frame, text="Date of Birth:")
    dob_label.grid(row=3, column=0, padx=5, pady=5)
    dob_entry = DateEntry(personal_info_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='MM/dd/yyyy')
    dob_entry.grid(row=3, column=1, padx=5, pady=5)
    gender_label = tkinter.Label(personal_info_frame, text ="Gender:")
    gender_label.grid(row=4, column=0, padx=5, pady=5)
    gender_combo = ttk.Combobox(personal_info_frame, values=["Female", "Male"])
    gender_combo.grid(row=4, column=1, padx=5, pady=5)
    race_combo = ttk.Combobox(personal_info_frame, values=["Alaskan Native", "American Indian", "Asian", "Black", "Native Hawaiian/Pacific Islander", "White"])
    race_combo.grid(row=5, column=1, padx=5, pady=5)
    race_label = tkinter.Label(personal_info_frame, text = "Race:")
    race_label.grid(row=5, column=0, padx=5, pady=5)
    ethnicity_label = tkinter.Label(personal_info_frame, text = "Ethnicity:")
    ethnicity_label.grid(row=6, column=0, padx=5, pady=5)
    ethnicity_combo = ttk.Combobox(personal_info_frame, values=["Hispanic", "Non-Hispanic"])
    ethnicity_combo.grid(row=6, column=1, padx=5, pady=5)
    referral_source_combo = ttk.Combobox(personal_info_frame, values=fetch_probation_officers())
    referral_source_combo.grid(row=7, column=1, padx=5, pady=5)
    referral_source_label = tkinter.Label(personal_info_frame, text = "Officer Name:")
    referral_source_label.grid(row=7, column=0, padx=5, pady=5)

    officer = referral_source_combo.get()
    print(officer)
    officer_id = get_officer_id(officer)

    # Create labels, entries, and combos inside parent_info_frame
    par_gar01_label = tkinter.Label(parent_info_frame, text="Full Name:")
    par_gar01_label.grid(row=0, column=0, padx=5, pady=5)
    par_gar01_entry = tkinter.Entry(parent_info_frame)
    par_gar01_entry.grid(row=0, column=1, padx=5, pady=5)
    par_gar01_rel_label = tkinter.Label(parent_info_frame, text="Relationship:")
    par_gar01_rel_label.grid(row=1, column=0, padx=5, pady=5)
    par_gar01_rel_combo = ttk.Combobox(parent_info_frame, values=["Mother", "Father", "Grandmother", "Grandfather", "Aunt", "Uncle", "Agency Rep. (Complete Below)"])
    par_gar01_rel_combo.grid(row=1, column=1, padx=5, pady=5)
    par_gar01_org_label = tkinter.Label(parent_info_frame, text="Organization:")
    par_gar01_org_label.grid(row=2, column=0, padx=5, pady=5)
    par_gar01_org_entry = tkinter.Entry(parent_info_frame)
    par_gar01_org_entry.grid(row=2, column=1, padx=5, pady=5)
    par_gar01_address_label = tkinter.Label(parent_info_frame, text="Address:")
    par_gar01_address_label.grid(row=3, column=0, padx=5, pady=5)
    par_gar01_address_entry = tkinter.Entry(parent_info_frame)
    par_gar01_address_entry.grid(row=3, column=1, padx=5, pady=5)
    par_gar01_email_label = tkinter.Label(parent_info_frame, text="Email:")
    par_gar01_email_label.grid(row=4, column=0, padx=5, pady=5)
    par_gar01_email_entry = tkinter.Entry(parent_info_frame)
    par_gar01_email_entry.grid(row=4, column=1, padx=5, pady=5)
    par_gar01_phone_label = tkinter.Label(parent_info_frame, text="Phone:")
    par_gar01_phone_label.grid(row=5, column=0, padx=5, pady=5)
    par_gar01_phone_entry = tkinter.Entry(parent_info_frame)
    par_gar01_phone_entry.grid(row=5, column=1, padx=5, pady=5)

    # Create labels, entries, and combos inside parent_info_frame
    # Example:
    par_gar02_label = tkinter.Label(parent_info2_frame, text="Full Name:")
    par_gar02_label.grid(row=0, column=0, padx=5, pady=5)
    par_gar02_entry = tkinter.Entry(parent_info2_frame)
    par_gar02_entry.grid(row=0, column=1, padx=5, pady=5)
    par_gar02_rel_label = tkinter.Label(parent_info2_frame, text="Relationship:")
    par_gar02_rel_label.grid(row=1, column=0, padx=5, pady=5)
    par_gar02_rel_combo = ttk.Combobox(parent_info2_frame, values=["Mother", "Father", "Grandmother", "Grandfather", "Aunt", "Uncle", "Agency Rep. (Complete Below)"])
    par_gar02_rel_combo.grid(row=1, column=1, padx=5, pady=5)
    par_gar02_org_label = tkinter.Label(parent_info2_frame, text="Organization:")
    par_gar02_org_label.grid(row=2, column=0, padx=5, pady=5)
    par_gar02_org_entry = tkinter.Entry(parent_info2_frame)
    par_gar02_org_entry.grid(row=2, column=1, padx=5, pady=5)
    par_gar02_address_label = tkinter.Label(parent_info2_frame, text="Address:")
    par_gar02_address_label.grid(row=3, column=0, padx=5, pady=5)
    par_gar02_address_entry = tkinter.Entry(parent_info2_frame)
    par_gar02_address_entry.grid(row=3, column=1, padx=5, pady=5)
    par_gar02_email_label = tkinter.Label(parent_info2_frame, text="Email:")
    par_gar02_email_label.grid(row=4, column=0, padx=5, pady=5)
    par_gar02_email_entry = tkinter.Entry(parent_info2_frame)
    par_gar02_email_entry.grid(row=4, column=1, padx=5, pady=5)
    par_gar02_phone_label = tkinter.Label(parent_info2_frame, text="Phone:")
    par_gar02_phone_label.grid(row=5, column=0, padx=5, pady=5)
    par_gar02_phone_entry = tkinter.Entry(parent_info2_frame)
    par_gar02_phone_entry.grid(row=5, column=1, padx=5, pady=5)
    blank_label = tkinter.Label(parent_info2_frame, text="")
    blank_label.grid(row=6, column=0, padx=5, pady=5)
    blank_label = tkinter.Label(parent_info2_frame, text="")
    blank_label.grid(row=7, column=0, padx=5, pady=5)

    # Define the variables in the global scope
    csw_state = tkinter.BooleanVar()
    edu_state = tkinter.BooleanVar()
    emp_state = tkinter.BooleanVar()
    jrf_state = tkinter.BooleanVar()
    preadjudicated_state = tkinter.BooleanVar()
    da_state = tkinter.BooleanVar()

    csw_checkbutton = tkinter.Checkbutton(other_info_frame, text="CSW", variable = csw_state)
    edu_checkbutton = tkinter.Checkbutton(other_info_frame, text="Education", variable = edu_state)
    emp_checkbutton = tkinter.Checkbutton(other_info_frame, text="Employment", variable = emp_state)
    jrf_checkbutton = tkinter.Checkbutton(other_info_frame, text="JRF", variable = jrf_state)
    preadjudicated_checkbutton = tkinter.Checkbutton(other_info_frame, text="Pre-Adjudicated", variable = preadjudicated_state)
    da_check = tkinter.Checkbutton(other_info_frame, text="Drug Treatment", variable = da_state)

    # Create labels, entries, and combos inside other_info_frame
    # Example:
    classification_label = tkinter.Label(other_info_frame, text="Classification:")
    classification_label.grid(row=4, column=0, padx=5, pady=5)
    classification_combo = ttk.Combobox(other_info_frame, values=["Crossover", "JO"])
    classification_combo.grid(row=4, column=1, padx=5, pady=5)
    yls_combo = ttk.Combobox(other_info_frame, values=["Comm. M: Low 0-9", "Comm. M: Mod. 10-21", "Comm. M: High 22-31", "Comm. M: Very High 32-42", "Comm. F: Low 0-8", "Comm. F: Mod. 9-19", "Comm. F: High 20-28", "Comm. F: Very High 29-42", "Cust. M/F: Low 0-19", "Cust. M/F: Mod. 20-29", "Cust. M/F: High 30-36", "Cust. M/F: Very High 37-42", "No YLS Score", 
                                     "IIP: Low 0-2", "IIP: Moderate 3-5", "IIP: High 6-8"])
    yls_combo.grid(row=1, column=1, padx=5, pady=5)
    yls_label = tkinter.Label(other_info_frame, text="YLS:")
    yls_label.grid(row=1, column=0, padx=5, pady=5)
    los_combo = ttk.Combobox(other_info_frame, values=["Case Management", "Conditional Release", "Immediate Intervention Program", "Juvenile Intensive Supervised Probation", "Standard Probation",
                                     "Not Under Supervision"])
    los_combo.grid(row=2, column=1, padx=5, pady=5)
    los_label = tkinter.Label(other_info_frame, text="Level of Service:")
    los_label.grid(row=2, column=0, padx=5, pady=5)
    referral_date_label = tkinter.Label(other_info_frame, text="Referral Date:")
    referral_date_label.grid(row=3, column=0, padx=5, pady=5)
    referral_date_entry = DateEntry(other_info_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern = 'MM/dd/yyyy')
    referral_date_entry.grid(row=3, column=1, padx=5, pady=5)
    district_combo = ttk.Combobox(other_info_frame,
                                  values=["18th", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th",
                                          "11th CR", "11th LB/CK", "12th", "13th", "14th", "15th/17th/23rd", "16th",
                                          "19th", "20th", "21st", "22nd", "24th", "25th", "26th", "27th", "28th",
                                          "29th", "30th SCKCCA", "30th SU", "31st"])
    district_combo.grid(row=0, column=1, padx=5, pady=5)
    district_label = tkinter.Label(other_info_frame, text="District:")
    district_label.grid(row=0, column=0, padx=5, pady=5)
    prog_start_entry = DateEntry(other_info_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern = 'MM/dd/yyyy')
    prog_start_entry.grid(row=7, column=1, padx=5, pady=5)
    prog_start_label = tkinter.Label(other_info_frame, text = "Projected Start Date:")
    prog_start_label.grid(row=7, column=0, padx=5, pady=5)
    start_living_combo = ttk.Combobox(other_info_frame, values=["AWOL", "Adult Jail", "Community Integration Program",
                                                          "Emergency Shelter", "Foster Care/Foster Home",
                                                          "Home (Family Member)", "Home (Other Responsible Adult)",
                                                          "Home (Parent/Guardian)", "Hospital (Medical)",
                                                          "Hospital (Psychiatric)", "Juvenile Correctional Facility",
                                                          "Juvenile Detention Center", "Living Independently (Self)",
                                                          "Psychiatric Residential Treatment Facility",
                                                          "Qualified Residential Treatment Program",
                                                          "Residential D/A Center", "Transitional Living Program",
                                                          "Youth Residential Facility", "Unknown"])
    start_living_combo.grid(row=8, column=1, padx=5, pady=5)
    start_living_label = tkinter.Label(other_info_frame, text="Living Arrangement:")
    start_living_label.grid(row=8, column=0, padx=5, pady=5)
    start_edu_combo = ttk.Combobox(other_info_frame, values=["Currently Enrolled and Attending", "Enrolled and Not Attending",
                                                       "Dropped Out/Withdrawn", "Graduated", "Unknown"])
    start_edu_combo.grid(row=9, column=1, padx=5, pady=5)
    start_edu_label = tkinter.Label(other_info_frame, text="Education Status:")
    start_edu_label.grid(row=9, column=0, padx=5, pady=5)
    start_emp_combo = ttk.Combobox(other_info_frame,
                                   values=["Employed", "Not Employed", "Not Employed due to Age", "Unknown"])
    start_emp_combo.grid(row=10, column=1, padx=5, pady=5)
    start_emp_label = tkinter.Label(other_info_frame, text="Employment Status:")
    start_emp_label.grid(row=10, column=0, padx=5, pady=5)
    blank_label = tkinter.Label(other_info_frame, text="")
    blank_label.grid(row=11, column=0, padx=5, pady=5)
    case_label = tkinter.Label(other_info_frame, text="Special Case:")
    case_label.grid(row=12, column=0, padx=5, pady=5, sticky="W")
    jrf_checkbutton.grid(row=13, column=0, padx=5, pady=5, sticky="W")
    preadjudicated_checkbutton.grid(row=14, column=0, padx=5, pady=5, sticky="W")
    blank_label2 = tkinter.Label(other_info_frame, text="")
    blank_label2.grid(row=15, column=0, padx=5, pady=5)
    service_request_label = tkinter.Label(other_info_frame, text="Services Requested:")
    service_request_label.grid(row=16, column=0, padx=5, pady=5, sticky="W")
    csw_checkbutton.grid(row=17, column=0, padx=5, pady=5, sticky="W")
    edu_checkbutton.grid(row=18, column=0, padx=5, pady=5, sticky="W")
    emp_checkbutton.grid(row=19, column=0, padx=5, pady=5, sticky="W")

    # Create labels, entries, and combos drug_treatment_frame
    def update_date_entry():
     if da_state.get(): # If the checkbox is checked
          
          # Get the current date from prog_start_entry
        date = prog_start_entry.get_date()

        formatted_date = date.strftime('%A %B %d, %Y')

          # Set this date to pro_sd_entry
        pro_sd_entry.delete(0, 'end')
        pro_sd_entry.insert(0, formatted_date)

    da_check = tkinter.Checkbutton(drug_treatment_frame, text="DA", padx=5, pady=5, variable = da_state, command = update_date_entry)
    da_check.grid(row=0, column=0, padx=5, pady=5)
    ssn_label = tkinter.Label(drug_treatment_frame, text="SSN:")
    ssn_label.grid(row=1, column=0, padx=5, pady=5)

    ssn_entry = tkinter.Entry(drug_treatment_frame)
    ssn_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")

    pro_sd_label = tkinter.Label(drug_treatment_frame, text="Projected Start Date:")
    pro_sd_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")
    pro_sd_entry = tkinter.Entry(drug_treatment_frame, textvariable= prog_start_entry, width = 23)
    pro_sd_entry.grid(row=2, column=1, columnspan= 2, padx=5, pady=5, sticky="W")

    notify_label = tkinter.Label(drug_treatment_frame, text="* Click submit to email eval request")
    notify_label.grid(row=3, column=0, padx=5, pady=5, sticky="W")

    def get_officer_email(officer_name):
        conn = sqlite3.connect(DB_Path)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM probation_officers WHERE officer_full_name = ?", (officer_name,))
        officer_email = cursor.fetchone()
        return officer_email[0]
    
    def clear_form():
        athena_entry.delete(0, 'end')
        client_last_entry.delete(0, 'end')
        client_first_entry.delete(0, 'end')
        dob_entry.delete(0, 'end')
        referral_date_entry.delete(0, 'end')
        prog_start_entry.delete(0, 'end')
        par_gar01_entry.delete(0, 'end')
        par_gar01_org_entry.delete(0, 'end')
        par_gar01_address_entry.delete(0, 'end')
        par_gar01_email_entry.delete(0, 'end')
        par_gar01_phone_entry.delete(0, 'end')
        par_gar02_entry.delete(0, 'end')
        par_gar02_org_entry.delete(0, 'end')
        par_gar02_address_entry.delete(0, 'end')
        par_gar02_email_entry.delete(0, 'end')
        par_gar02_phone_entry.delete(0, 'end')

        # Clear combobox widgets
        gender_combo.set('')
        race_combo.set('')
        ethnicity_combo.set('')
        yls_combo.set('')
        los_combo.set('')
        district_combo.set('')
        start_living_combo.set('')
        start_edu_combo.set('')
        start_emp_combo.set('')
        referral_source_combo.set('')
        classification_combo.set('')
        par_gar01_rel_combo.set('')
        par_gar02_rel_combo.set('') 
        ssn_entry.delete(0, 'end')
        pro_sd_entry.delete(0, 'end')

        # Clear checkboxes
        csw_state.set(False)
        edu_state.set(False)
        emp_state.set(False)
        jrf_state.set(False)
        preadjudicated_state.set(False)
        da_state.set(False)

    def submit_ind():

            conn = sqlite3.connect(DB_Path)
            cursor = conn.cursor()

            # Getting data from the form
            dob = datetime.strptime(dob_entry.get(), '%m/%d/%Y').date()
            referral_date = datetime.strptime(referral_date_entry.get(), '%m/%d/%Y').date()

            formatted_dob = dob.strftime('%m/%d/%Y')

            # Calculating age
            age = (referral_date - dob).days // 365.25

            prog_start_date_str = prog_start_entry.get()
            prog_start_date = datetime.strptime(prog_start_date_str, '%m/%d/%Y').date()

            find_quarter = prog_start_date.month        

            def find_reporting_quarter(find_quarter):
                if find_quarter == 7 or find_quarter == 8 or find_quarter == 9:
                    reporting_quarter = 'Q1'
                elif find_quarter == 10 or find_quarter == 11 or find_quarter == 12:
                    reporting_quarter = 'Q2'
                elif find_quarter == 1 or find_quarter == 2 or find_quarter == 3:
                    reporting_quarter = 'Q3'
                elif find_quarter == 4 or find_quarter == 5 or find_quarter == 6:
                    reporting_quarter = 'Q4'
                return reporting_quarter
            
            reporting_quarter = find_reporting_quarter(find_quarter)

            officer = referral_source_combo.get()
            officer_id = get_officer_id(officer)
            officer_email = get_officer_email(officer)

            def drug_treatment(officer):

                    num_str = str(ssn_entry.get())
                    formatted_str = num_str[0:3] + "-" + num_str[3:5] + "-" + num_str[5:]

                    formatted_proj_start = prog_start_date.strftime('%A %B %d, %Y')

                    outlook = client.Dispatch("Outlook.Application")

                    message = outlook.CreateItem(0)
                    message.Display()
                    message.To = "larry.burks@sedgwick.gov;dlizarraga@seventhdirectioninc.com;lanora.franck@sedgwick.gov;hburt@seventhdirectioninc.com;nmagruder@seventhdirectioninc.com;recker@seventhdirectioninc.com;rkaser@seventhdirectioninc.com"
                    
                    if officer_email is not None:
                        message.CC = officer_email

                    message.Subject = 'Run Coverage'
                                      
                    message.HTMLBody = f"""\
                    Please run coverage for the following:<br><br>
                    <b>Name:</b> {client_first_entry.get() + " " + client_last_entry.get()}<br>
                    <b>SSN:</b> {formatted_str}<br>
                    <b>DOB:</b> {formatted_dob}<br>
                    <b>Projected Start Date:</b> {formatted_proj_start}<br>
                    """

                    messagebox.showinfo("message", "Eval Request Sent!")

            if da_state.get() == True:
                 
                 drug_treatment(officer)

            client_data = (
                athena_entry.get(),
                client_last_entry.get(),
                client_first_entry.get(),
                dob,
                gender_combo.get(),
                race_combo.get(),
                ethnicity_combo.get(),
                officer_id, 
                district_combo.get(),
                yls_combo.get(),
                los_combo.get(),
                referral_date,
                classification_combo.get(),
                prog_start_date,
                start_living_combo.get(),
                start_edu_combo.get(),
                start_emp_combo.get(),
                jrf_state.get(),
                preadjudicated_state.get(),
                csw_state.get(),
                edu_state.get(),
                emp_state.get(),
                par_gar01_entry.get(),
                par_gar01_rel_combo.get(),
                par_gar01_org_entry.get(),
                par_gar01_address_entry.get(),
                par_gar01_email_entry.get(),
                par_gar01_phone_entry.get(),
                par_gar02_entry.get(),
                par_gar02_rel_combo.get(),
                par_gar02_org_entry.get(),
                par_gar02_address_entry.get(),
                par_gar02_email_entry.get(),
                par_gar02_phone_entry.get(),
                reporting_quarter,
                age,
                da_state.get()
            )

            try:
                    client_data = list(client_data)

                    sql = '''
                        INSERT INTO clients ( 
                            athena,
                            client_last, 
                            client_first,                            
                            dob,
                            gender,
                            race,
                            ethnicity,
                            probation_officer_id,
                            district,
                            yls,
                            referral_type,
                            referral_date,
                            classification,
                            start_date,
                            start_living,
                            start_edu,
                            start_emp,
                            jrf,
                            preadjudicated,
                            csw,
                            edu,
                            emp,
                            par_gar01,
                            par_gar01_rel,
                            par_gar01_org,
                            par_gar01_add,
                            par_gar01_email,
                            par_gar01_cell,
                            par_gar02,
                            par_gar02_rel,
                            par_gar02_org,
                            par_gar02_add,
                            par_gar02_email,
                            par_gar02_cell,
                            rep_qtr,
                            age,
                            eval_needed
                                                      
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
                    cursor.execute(sql, client_data)
                    conn.commit()

                    # Clear entry widgets
                    athena_entry.delete(0, 'end')
                    client_last_entry.delete(0, 'end')
                    client_first_entry.delete(0, 'end')
                    dob_entry.delete(0, 'end')
                    referral_date_entry.delete(0, 'end')
                    prog_start_entry.delete(0, 'end')
                    par_gar01_entry.delete(0, 'end')
                    par_gar01_org_entry.delete(0, 'end')
                    par_gar01_address_entry.delete(0, 'end')
                    par_gar01_email_entry.delete(0, 'end')
                    par_gar01_phone_entry.delete(0, 'end')
                    par_gar02_entry.delete(0, 'end')
                    par_gar02_org_entry.delete(0, 'end')
                    par_gar02_address_entry.delete(0, 'end')
                    par_gar02_email_entry.delete(0, 'end')
                    par_gar02_phone_entry.delete(0, 'end')
                    ssn_entry.delete(0, 'end')
                    pro_sd_entry.delete(0, 'end')

                    # Clear combobox widgets
                    gender_combo.set('')
                    race_combo.set('')
                    ethnicity_combo.set('')
                    yls_combo.set('')
                    los_combo.set('')
                    district_combo.set('')
                    start_living_combo.set('')
                    start_edu_combo.set('')
                    start_emp_combo.set('')
                    referral_source_combo.set('')
                    classification_combo.set('')
                    par_gar01_rel_combo.set('')
                    par_gar02_rel_combo.set('') 

                    # Clear checkboxes
                    csw_state.set(False)
                    edu_state.set(False)
                    emp_state.set(False)
                    jrf_state.set(False)
                    preadjudicated_state.set(False)
                    da_state.set(False)

                    clear_form()
                    messagebox.showinfo("Success", "Data submitted successfully!")
                    cursor.close()
                    conn.close()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    submit_button = tkinter.Button(ind_window, text="Submit", command=submit_ind)
    submit_button.grid(row=8, column=2, padx=5, pady=5)

    # Start the Tkinter event loop
    ind_window.mainloop()

# Run the main function to start the application
ind_client()

#  import tkinter
# from tkinter import messagebox, ttk
# from tkcalendar import DateEntry
# import os
# from datetime import datetime
# import sqlite3
# import runpy
# from aspire_functions import ind_transition_bulk

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# # function for referral source combo box
# def fetch_probation_officers():
#     conn = sqlite3.connect('database\central_database.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT full_name FROM probation_officers")
#     officers = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     # Convert list of tuples into list
#     officers = [officer[0] for officer in officers]
#     return officers 

# def bulk_transition(current_window):
         
#         current_window.destroy()
    
#         runpy.run_path('submit_bulk.py')

# def ind_client():

#     # Create the main ind_window
#     ind_window = tkinter.Tk()
#     ind_window.title("Add Client Manually")
#     ind_window.geometry('1200x900')
#     ind_window.configure(bg='#483D8B')
#     ind_window.iconbitmap('.\images\icons\\futuristic.ico')
#     ind_window.state('zoomed')

#     for i in range(0, 16):
#         ind_window.grid_rowconfigure(i, weight=1)

#     for i in range(0, 2):
#         ind_window.grid_columnconfigure(i, weight=1)

#     # Create the top level menu
#     menubar = tkinter.Menu(ind_window)

#     # Create a submenu te be part of the top-level menu
#     filemenu = tkinter.Menu(menubar, tearoff=0)
#     filemenu.add_command(label="Client Intake (Bulk)", command=lambda: ind_transition_bulk(ind_window))

#     # Add the File menu to the menu bar
#     menubar.add_cascade(label="Selection", menu=filemenu)

#     # Associate the menu bar to the window
#     ind_window.config(menu=menubar)

#     # Create the Entry widgets
#     athena_entry = tkinter.Entry(ind_window)
#     client_last_entry = tkinter.Entry(ind_window)
#     client_first_entry = tkinter.Entry(ind_window)
#     dob_entry = DateEntry(ind_window, date_pattern='m/d/yyyy')  # Repalce Entry with DateEntry for 'dob'
#     referral_date_entry = DateEntry(ind_window, date_pattern='m/d/yyyy')  # Repalce Entry with DateEntry for 'refferal date'
#     referral_source_combo = ttk.Combobox(ind_window, values=fetch_probation_officers())
#     prog_start_entry = DateEntry(ind_window, date_pattern='m/d/yyyy')  # Repalce Entry with DateEntry for 'program start date'

#     # Create the Combobox widgets
#     gender_combo = ttk.Combobox(ind_window, values=["Female", "Male"])
#     race_combo = ttk.Combobox(ind_window, values=["American Indian/Alaskan Native", "Asian/Pacific Islander", "Black",
#                                                   "Multi-Racial", "White"])
#     ethnicity_combo = ttk.Combobox(ind_window, values=["Hispanic", "Non-Hispanic"])
#     yls_combo = ttk.Combobox(ind_window,
#                              values=["IIP: Low 0-2", "IIP: Moderate 3-5", "IIP: High 6-8", "Cust. M/F: Low 0-19",
#                                      "Cust. M/F: Mod. 20-29", "Cust. M/F: High 30-36", "Cust. M/F: Very High 37-42",
#                                      "Comm. F: Low 0-8", "Comm. F: Mod. 9-19", "Comm. F: High 20-28",
#                                      "Comm. F: Very High 29-42", "Comm. M: Low 0-9", "Comm. M: Mod. 10-21",
#                                      "Comm. M: High 22-31", "Comm. M: Very High 32-42", "No YLS Score"])
#     employment_combo = ttk.Combobox(ind_window,
#                                     values=["Employed", "Not Employed", "Not Employed due to Age", "Unknown"])
#     los_combo = ttk.Combobox(ind_window,
#                              values=["Case Management", "Conditional Release", "Immediate Intervention Program",
#                                      "Juvenile Intensive Supervised Probation", "Standard Probation",
#                                      "Not Under Supervision"])
#     district_combo = ttk.Combobox(ind_window,
#                                   values=["18th", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th",
#                                           "11th CR", "11th LB/CK", "12th", "13th", "14th", "15th/17th/23rd", "16th",
#                                           "19th", "20th", "21st", "22nd", "24th", "25th", "26th", "27th", "28th",
#                                           "29th", "30th SCKCCA", "30th SU", "31st"])
#     start_living_combo = ttk.Combobox(ind_window, values=["AWOL", "Adult Jail", "Community Integration Program",
#                                                           "Emergency Shelter", "Foster Care/Foster Home",
#                                                           "Home (Family Member)", "Home (Other Responsible Adult)",
#                                                           "Home (Parent/Guardian)", "Hospital (Medical)",
#                                                           "Hospital (Psychiatric)", "Juvenile Correctional Facility",
#                                                           "Juvenile Detention Center", "Living Independently (Self)",
#                                                           "Psychiatric Residential Treatment Facility",
#                                                           "Qualified Residential Treatment Program",
#                                                           "Residential D/A Center", "Transitional Living Program",
#                                                           "Youth Residential Facility", "Unknown"])
#     start_edu_combo = ttk.Combobox(ind_window, values=["Currently Enrolled and Attending", "Enrolled and Not Attending",
#                                                        "Dropped Out/Withdrawn", "Graduated", "Unknown"])
#     start_emp_combo = ttk.Combobox(ind_window,
#                                    values=["Employed", "Not Employed", "Not Employed due to Age", "Unknown"])
    
#     referral_source_combo = ttk.Combobox(ind_window, values=fetch_probation_officers())
    
#     # Create the labels
#     athena_label = tkinter.Label(ind_window, text="Athena:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     client_last_label = tkinter.Label(ind_window, text="Client Last:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     client_first_label = tkinter.Label(ind_window, text="Client First:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     dob_label = tkinter.Label(ind_window, text="DOB:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     referral_date_label = tkinter.Label(ind_window, text="Referral Date:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     referral_source_label = tkinter.Label(ind_window, text="Referral Source (Probation Officer):", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     gender_label = tkinter.Label(ind_window, text="Gender:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     race_label = tkinter.Label(ind_window, text="Race:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     ethnicity_label = tkinter.Label(ind_window, text="Ethnicity:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     yls_label = tkinter.Label(ind_window, text="YLS/CMI Score:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     los_label = tkinter.Label(ind_window, text="Level Of Service:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     district_label = tkinter.Label(ind_window, text="Judicial District:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     prog_start_label = tkinter.Label(ind_window, text="Program Start Date:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     start_living_label = tkinter.Label(ind_window, text="Current Living ArrangementL", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     start_education_label = tkinter.Label(ind_window, text="Education Status:", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     start_emp_label = tkinter.Label(ind_window, text="Employment Status:", bg='#483D8B', font=("Helvetica", 13, "bold"))

#     # Create checkboxes
#     csw_checkbutton = tkinter.Checkbutton(ind_window, text="CSW", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     edu_checkbutton = tkinter.Checkbutton(ind_window, text="Education", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     emp_checkbutton = tkinter.Checkbutton(ind_window, text="Employment", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     jrf_checkbutton = tkinter.Checkbutton(ind_window, text="JRF", bg='#483D8B', font=("Helvetica", 13, "bold"))
#     preadjuicated_checkbutton = tkinter.Checkbutton(ind_window, text="Pre-Adjudicated", bg='#483D8B', font=("Helvetica", 13, "bold"))

#     # Create IntVar objects
#     csw_state = tkinter.IntVar()
#     edu_state = tkinter.IntVar()
#     emp_state = tkinter.IntVar()
#     jrf_state = tkinter.IntVar()
#     preadjuicated_state = tkinter.IntVar()

#     # TODO: Create more labels here

#     # Arrange the widgets using grid layout
#     athena_label.grid(row=0, column=0, sticky='nswe')
#     athena_entry.grid(row=0, column=1, sticky='nswe')
#     client_last_label.grid(row=1, column=0, sticky='nswe')
#     client_last_entry.grid(row=1, column=1, sticky='nswe')
#     client_first_label.grid(row=2, column=0, sticky='nswe')
#     client_first_entry.grid(row=2, column=1, sticky='nswe')
#     dob_label.grid(row=3, column=0, sticky='nswe')
#     dob_entry.grid(row=3, column=1, sticky='nswe')
#     referral_date_label.grid(row=4, column=0, sticky='nswe')
#     referral_date_entry.grid(row=4, column=1, sticky='nswe')
#     referral_source_label.grid(row=5, column=0, sticky='nswe')
#     referral_source_combo.grid(row=5, column=1, sticky='nswe')
#     gender_label.grid(row=6, column=0, sticky='nswe')
#     gender_combo.grid(row=6, column=1, sticky='nswe')
#     race_label.grid(row=7, column=0, sticky='nswe')
#     race_combo.grid(row=7, column=1, sticky='nswe')
#     ethnicity_label.grid(row=8, column=0, sticky='nswe')
#     ethnicity_combo.grid(row=8, column=1, sticky='nswe')
#     yls_label.grid(row=9, column=0, sticky='nswe')
#     yls_combo.grid(row=9, column=1, sticky='nswe')
#     los_label.grid(row=10, column=0, sticky='nswe')
#     los_combo.grid(row=10, column=1, sticky='nswe')
#     district_label.grid(row=11, column=0, sticky='nswe')
#     district_combo.grid(row=11, column=1, sticky='nswe')
#     prog_start_label.grid(row=12, column=0, sticky='nswe')
#     prog_start_entry.grid(row=12, column=1, sticky='nswe')
#     start_living_label.grid(row=13, column=0, sticky='nswe')
#     start_living_combo.grid(row=13, column=1, sticky='nswe')
#     start_education_label.grid(row=14, column=0, sticky='nswe')
#     start_edu_combo.grid(row=14, column=1, sticky='nswe')
#     start_emp_label.grid(row=15, column=0, sticky='nswe')
#     start_emp_combo.grid(row=15, column=1, sticky='nswe')
#     csw_checkbutton.grid(row=16, column=0, sticky='we')
#     edu_checkbutton.grid(row=17, column=0, sticky='we')
#     emp_checkbutton.grid(row=18, column=0, sticky='we')
#     jrf_checkbutton.grid(row=19, column=0, sticky='we')
#     preadjuicated_checkbutton.grid(row=20, column=0, sticky='we')
  

#     def submit_ind():

#         conn = sqlite3.connect('database\central_database.db')
#         cursor = conn.cursor()

#         # Getting data from the form
#         dob = datetime.strptime(dob_entry.get(), '%m/%d/%Y').date()
#         referral_date = datetime.strptime(referral_date_entry.get(), '%m/%d/%Y').date()

#         # Calculating age
#         age = (referral_date - dob).days // 365.25

#         client_data = (
#             client_last_entry.get(),
#             client_first_entry.get(),
#             athena_entry.get(),
#             dob_entry.get(),
#             gender_combo.get(),
#             race_combo.get(),
#             ethnicity_combo.get(),
#             yls_combo.get(),
#             los_combo.get(),
#             referral_date_entry.get(),
#             age,
#             district_combo.get(),
#             prog_start_entry.get(),
#             start_living_combo.get(),
#             start_edu_combo.get(),
#             start_emp_combo.get(),
#             referral_source_combo.get(),    
#         )

#         try:
#                 client_data = list(client_data)

#                 sql = '''
#                     INSERT INTO clients ( 
#                         client_last, 
#                         client_first,
#                         athena,
#                         dob,
#                         gender,
#                         race,
#                         ethnicity,
#                         yls, 
#                         referral_type,
#                         referral_date,
#                         age,
#                         district,
#                         start_date, 
#                         start_living, 
#                         start_edc, 
#                         start_emp,  
#                         referral_source 
#                     ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
# '''
#                 cursor.execute(sql, client_data)
#                 conn.commit()
#                 messagebox.showinfo("Success", "Data submitted successfully!")
#                 cursor.close()
#                 conn.close()

#         except Exception as e:
#             messagebox.showerror("Error", str(e))

#     # Create the Submit button
#     submit_button = tkinter.Button(ind_window, text="Submit", command=submit_ind)
#     submit_button.grid(row=25, column=0, columnspan=2)

#     # Start the Tkinter event loop
#     ind_window.mainloop()



# ind_client()