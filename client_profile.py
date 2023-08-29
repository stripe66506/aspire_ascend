import tkinter as tk
from tkinter import Label, messagebox
from tkcalendar import DateEntry
import win32com.client as client
import sys
import sqlite3
import os
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ClientProfile:
    def __init__(self, window, client_id):
        self.window = window
        self.window.title("Client Enrollment Page")
        self.window.state('zoomed')

        # Define the variables to be used
        self.name = tk.StringVar()
        self.gender = tk.StringVar()
        self.enroll_date = tk.StringVar()
        self.probation_officer = tk.StringVar()
        self.yls_info = tk.StringVar()
        self.parent_name = tk.StringVar()
        self.parent_email = tk.StringVar()
        self.parent_phone = tk.StringVar()
        self.programming_days = tk.StringVar()
        self.ssn = tk.StringVar()
        self.projected_start_date = tk.StringVar()  # Initialize this variable
        self.dob = tk.StringVar()

        # Fetch the student's data from the database
        conn = sqlite3.connect('database\central_database.db')
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT clients.*, probation_officers.officer_full_name 
            FROM clients
            JOIN probation_officers
            ON clients.probation_officer_id = probation_officers.id
            WHERE clients.id ={client_id}
        """)
        student_data = cursor.fetchone()
        print(f"student_data: {student_data}")  # Add this line
        conn.close()

        date_string = student_data[12]
        date_object = datetime.strptime(date_string, '%Y/%m/%d')
        formatted_date_string = date_object.strftime('%m/%d/%Y')

        # Populate the form fields
        self.name.set(student_data[2] + " " + student_data[1])
        self.gender.set(student_data[6])
        self.enroll_date.set(formatted_date_string)
        self.probation_officer.set(student_data[75])
        self.yls_info.set(student_data[10])
        self.parent_name.set(student_data[30])
        self.parent_email.set(student_data[34])
        self.parent_phone.set(student_data[35])
        self.ssn.set(student_data[53])
        self.dob.set(student_data[4])

        # Client profile section
        tk.Label(window, text="Client Enrollment Page", font=("Arial", 24)).grid(row=0, column=1, columnspan=2)
        tk.Label(window, text="Client Picture", borderwidth=2, relief="groove").grid(row=1, rowspan=5, column=0)
        tk.Label(window, text="Client Name:").grid(row=1, column=1, sticky="w")
        tk.Entry(window, textvariable=self.name).grid(row=1, column=2)
        tk.Label(window, text="Gender:").grid(row=2, column=1, sticky="w")
        tk.Entry(window, textvariable=self.gender).grid(row=2, column=2)
        tk.Label(window, text="Enrollment Date:").grid(row=3, column=1, sticky="w")
        tk.Entry(window, textvariable=self.enroll_date).grid(row=3, column=2)
        tk.Label(window, text="Probation Officer:").grid(row=4, column=1, sticky="w")
        tk.Entry(window, textvariable=self.probation_officer).grid(row=4, column=2)
        tk.Label(window, text="YLS Information:").grid(row=5, column=1, sticky="w")
        tk.Entry(window, textvariable=self.yls_info).grid(row=5, column=2)
        tk.Label(window, text="Parent Name:").grid(row=6, column=1, sticky="w")
        tk.Entry(window, textvariable=self.parent_name).grid(row=6, column=2)
        tk.Label(window, text="Parent Email:").grid(row=7, column=1, sticky="w")
        tk.Entry(window, textvariable=self.parent_email).grid(row=7, column=2)
        tk.Label(window, text="Parent Phone:").grid(row=8, column=1, sticky="w")
        tk.Entry(window, textvariable=self.parent_phone).grid(row=8, column=2)

        # Programming and Groups section
        tk.Label(window, text="Programming Days", font=("", 14, 'bold', 'underline')).grid(row=9, column=0)
        start_date = DateEntry(window, width=12, background='darkblue', foreground='white', borderwidth=10)
        Label(window, text="Choose start date", font=("", 12, 'bold', 'underline')).grid(row=10, column=0)
        start_date.grid(row=11, column=0)
        start_date.bind("<<DateEntrySelected>>", lambda e: self.update_projected_start_date(start_date))
        Label(window, text="Choose Programming Days", font=("", 12, 'bold', 'underline')).grid(row=12, column=0)
        tk.Checkbutton(window, text="MW").grid(row=13, column=0)
        tk.Checkbutton(window, text="TTH").grid(row=14, column=0)
        tk.Checkbutton(window, text="MWF").grid(row=15, column=0)
        tk.Checkbutton(window, text="TTHF").grid(row=16, column=0)
        tk.Checkbutton(window, text="Daily").grid(row=17, column=0)
        tk.Checkbutton(window, text="M").grid(row=18, column=0)
        tk.Checkbutton(window, text="T").grid(row=19, column=0)
        tk.Checkbutton(window, text="W").grid(row=20, column=0)
        tk.Checkbutton(window, text="TH").grid(row=21, column=0)
        tk.Checkbutton(window, text="F").grid(row=22, column=0)

        # Daytime group selection
        tk.Label(window, text="Programming Schedule", font=("", 14, 'bold', 'underline')).grid(row=9, column=3)
        tk.Label(window, text="Choose Daytime Programming", font=("", 12, 'bold', 'underline')).grid(row=10, column=1)
        tk.Checkbutton(window, text="Education").grid(row=11, column=1)
        tk.Checkbutton(window, text="CRT").grid(row=12, column=1)
        tk.Checkbutton(window, text="Job Skills").grid(row=13, column=1)
        tk.Checkbutton(window, text="GROWTH").grid(row=14, column=1)

        # Drug Treatment
        tk.Label(window, text="Drug Treatment Eval", font=("", 12, 'bold', 'underline')).grid(row=16, column=1)
        tk.Entry(window, textvariable=self.ssn).grid(row=17, column=1)
        tk.Label(window, text="SSN").grid(row=18, column = 1)

        projected_start_date = start_date.get_date()
        formatted_proj_date = projected_start_date.strftime('%B %d, %Y')
        start_date.bind("<<DateEntrySelected>>", lambda e: self.update_projected_start_date(start_date))
        self.projected_start_date.set(formatted_proj_date)
        tk.Entry(window, textvariable=self.projected_start_date).grid(row=19, column=1)
        tk.Label(window, text="Projected Start Date").grid(row=20, column=1)

        date_string = self.dob.get()
        date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        formatted_date_string = date_object.strftime('%m/%d/%Y')
        self.dob.set(formatted_date_string)

        formatted_date_string = formatted_date_string.lstrip('0')
        formatted_date_string = formatted_date_string.replace('/0', '/')
        self.dob.set(formatted_date_string)

        tk.Button(window, text="Submit to Treatment", command=self.evaluation).grid(row=21, column=1)
        tk.Button(window, text="Enroll Client", command=print('Client enrolled!')).grid(row=24, column=3)

         # Evening group selection
        tk.Label(window, text="First Evening Group", font=("", 12, 'bold', 'underline')).grid(row=10, column=2)
        tk.Checkbutton(window, text="Boy's Council").grid(row=11, column=2)
        tk.Checkbutton(window, text="Drug Treatment").grid(row=12, column=2)
        tk.Checkbutton(window, text="Education").grid(row=13, column=2)
        tk.Checkbutton(window, text="Girl's Circle").grid(row=14, column=2)
        tk.Checkbutton(window, text="GROWTH").grid(row=15, column=2)
        tk.Checkbutton(window, text="LifeSkills").grid(row=16, column=2)
        tk.Checkbutton(window, text="MRT").grid(row=17, column=2)
        tk.Checkbutton(window, text="Safe Dates").grid(row=18, column=2)
        tk.Checkbutton(window, text="Seeking Safety").grid(row=19, column=2)
        tk.Checkbutton(window, text="Strengthen Your Mind").grid(row=20, column=2)
        tk.Checkbutton(window, text="Substance Abuse").grid(row=21, column=2)
        tk.Checkbutton(window, text="Thinking for a Change").grid(row=22, column=2)

        # Evening group selection
        tk.Label(window, text="Second Evening Group", font=("", 12, 'bold', 'underline')).grid(row=10, column=3)
        tk.Checkbutton(window, text="Boy's Council").grid(row=11, column=3)
        tk.Checkbutton(window, text="Drug Treatment").grid(row=12, column=3)
        tk.Checkbutton(window, text="Education").grid(row=13, column=3)
        tk.Checkbutton(window, text="Girl's Circle").grid(row=14, column=3)
        tk.Checkbutton(window, text="GROWTH").grid(row=15, column=3)
        tk.Checkbutton(window, text="LifeSkills").grid(row=16, column=3)
        tk.Checkbutton(window, text="MRT").grid(row=17, column=3)
        tk.Checkbutton(window, text="Safe Dates").grid(row=18, column=3)
        tk.Checkbutton(window, text="Seeking Safety").grid(row=19, column=3)
        tk.Checkbutton(window, text="Strengthen Your Mind").grid(row=20, column=3)
        tk.Checkbutton(window, text="Substance Abuse").grid(row=21, column=3)
        tk.Checkbutton(window, text="Thinking for a Change").grid(row=22, column=3)
        tk.Label(window, text=" ").grid(row=23, column=3)

        # Evening group selection
        tk.Label(window, text="Third Evening Group", font=("", 12, 'bold', 'underline')).grid(row=10, column=4)
        tk.Checkbutton(window, text="Boy's Council").grid(row=11, column=4)
        tk.Checkbutton(window, text="Drug Treatment").grid(row=12, column=4)
        tk.Checkbutton(window, text="Education").grid(row=13, column=4)
        tk.Checkbutton(window, text="Girl's Circle").grid(row=14, column=4)
        tk.Checkbutton(window, text="GROWTH").grid(row=15, column=4)
        tk.Checkbutton(window, text="LifeSkills").grid(row=16, column=4)
        tk.Checkbutton(window, text="MRT").grid(row=17, column=4)
        tk.Checkbutton(window, text="Safe Dates").grid(row=18, column=4)
        tk.Checkbutton(window, text="Seeking Safety").grid(row=19, column=4)
        tk.Checkbutton(window, text="Strengthen Your Mind").grid(row=20, column=4)
        tk.Checkbutton(window, text="Substance Abuse").grid(row=21, column=4)
        tk.Checkbutton(window, text="Thinking for a Change").grid(row=22, column=4)

        # Evening group selection
        tk.Label(window, text="Friday Evening Group", font=("", 12, 'bold', 'underline')).grid(row=10, column=5)
        tk.Checkbutton(window, text="CSW").grid(row=11, column=5)
        tk.Checkbutton(window, text="Untamed Athletes").grid(row=12, column=5)

    def update_projected_start_date(self, start_date_widget):
        selected_date = start_date_widget.get_date()
        formatted_date = selected_date.strftime('%B %d, %Y')
        self.projected_start_date.set(formatted_date)

    def evaluation(self):

        outlook = client.Dispatch("Outlook.Application")

        message = outlook.CreateItem(0)
        message.Display()
        message.To = "larry.burks@sedgwick.gov;dlizarraga@seventhdirectioninc.com;Lanora.Franck@sedgwick.gov;hburt@seventhdirectioninc.com;nmagruder@seventhdirectioninc.com;recker@seventhdirectioninc.com;rkaser@seventhdirectioninc.com"
        message.Subject = 'Run Coverage'
        message.HTMLBody = f"""\
        Please run coverage for the following:<br><br>
        <b>Name:</b> {self.name.get()}<br>
        <b>SSN:</b> {self.ssn.get()}<br>
        <b>DOB:</b> {self.dob.get()}<br>
        <b>Projected Start Date:</b> {self.projected_start_date.get()}<br>
        """

        messagebox.showinfo("message", "Eval Request Sent!")

if __name__ == "__main__":
    root = tk.Tk()
    print(sys.argv[1])
    client_id = sys.argv[1]
    app = ClientProfile(root, client_id)
    root.mainloop()
