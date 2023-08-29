import runpy
import subprocess
from tkinter import messagebox
import os
import subprocess

# Transition window to supervisor main menu
def login_transition_sup_main(current_window):
    current_window.destroy()
    from aspire_main import sup_main_menu
    sup_main_menu()   

# Transition supervisor individual client add to client management main menu
def ind_transition_cm(current_window):
    from sp_cman import sp_cm_menu
    current_window.destroy()
    sp_cm_menu()

def supmain_trans_cm(current_window):
     
     current_window.destroy()

     # Run the client_intake_ind.py as a subprocess
     try:
          subprocess.run(["python", "sp_cman.py"])

     except Exception as e:
          messagebox.showerror("Error", f"An error occurred: {e}")
          

def sp_trans_ind(current_window):
     
     current_window.destroy()

     # Run the client_intake_ind.py as a subprocess
     try:
            subprocess.run(["python", "client_intake_ind.py"])

     except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

#transition supervisor bulk client add to client management main menu
def bulk_transition_cm(current_window):
    from sp_cman import sp_cm_menu
    current_window.destroy()
    sp_cm_menu()

# transition to bulk intake window
def ci_trans_blk(current_window):
    from sp_cman import bulk_intake
    current_window.destroy()
    bulk_intake()

# transition supervisor main menu to individual client add
def sm_transition_ind(current_window):
    from sp_cman import client_enrollment_window
    current_window.destroy()
    client_enrollment_window()

