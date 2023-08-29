import os
import runpy
from aspire_main import sup_main_menu
from sp_cman import client_enrollment_window, sp_cm_menu


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Sup Functions

# Transition login to supervisor main menu
def login_transition_sup_main(current_window):

    current_window.destroy()

    sup_main_menu()

def back_to_enroll(current_window):
         
            current_window.destroy()
        
            client_enrollment_window()




def bulk_transition_ind(current_window):

    current_window.destroy()

    runpy.run_path('submit_data.py')

def sm_transition_bulk(current_window):

    current_window.destroy()

    runpy.run_path('submit_bulk.py')

def bulk_transition_cm(current_window):

    current_window.destroy()

    sp_cm_menu()

def ind_transition_cm(current_window):

    current_window.destroy()

    create_cm_menu()

def ind_transition_bulk(current_window):

    current_window.destroy()

    runpy.run_path('submit_bulk.py')