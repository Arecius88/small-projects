import tkinter as tk
from tkinter import ttk
import sqlite3
from icecream import ic
from tkinter.messagebox import showwarning

"""
This is a tkinter project, for me to learn the basics och tkinter. 
It is a tutorial project. I got the visual of the data entry form
from codefirstio's youtube channel. Then I wrote the code with as 
little help from codefirstio's sourcecode as possible. 

Credit: https://github.com/codefirstio
Repository: https://github.com/codefirstio/tkinter-data-entry
Youtube Tutorial: https://youtu.be/vusUfPBsggw

"""






#Confuguration
root_window_title = "Data entry form"
window_height = 350
window_width = 550


def create_database(database_name: str) -> None:
    """Creates the database and also the tables. 

    Arguments:
        database_name -- give the database a name. 
    """    
    connector = sqlite3.connect(database_name)
    cursor = connector.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS students(title, 
                first_name, 
                last_name, 
                age, 
                nationality,
                registration_status,
                num_courses,
                num_semesters,
                accept_terms_cons)
                """)

    connector.commit()
    connector.close()

def insert_to_database(data_list: list[tuple[str,int,bool]]) -> None:
    """Function to insert rows in the database. 

    Arguments:
        data_list -- a list of tuples with the elements that should go to the db.
    """    
    # Create a connector to the db
    connector = sqlite3.connect("Entryform.db")
    
    # Create the cursor to db
    cursor = connector.cursor()
    
    # db query
    cursor.executemany("""INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?)""", data_list)
    
    # Commit the changes
    connector.commit()
    
    #Close the db
    connector.close()

def define_root_window(root_window: tk, root_window_height: int, root_window_width: int, center_root_window : bool = False)-> tk:
    """A function to define the root window in this Tkinter app and position the window in the middle of the screen

    Arguments:
        root_window -- _name of root window_
        root_window_height -- num of px in height
        root_window_width -- num of px in width

    Keyword Arguments:
        center_root_window -- Choose True of you want the window to be centerd (default: {False})

    Returns:
        TK genometry of the window
    """    
    if center_root_window:

        # Get sceen size
        screen_height = root_window.winfo_screenheight()
        screen_width = root_window.winfo_screenheight()
        
        # Placement coordinates
        x_coordinate = int((screen_width//2) - (root_window_width//2))
        y_coordinate = int((screen_height//2) - (root_window_height//2))
        
        return root_window.geometry(f"{root_window_width}x{root_window_height}+{x_coordinate}+{y_coordinate}")
    return root_window.geometry(f"{root_window_width}x{root_window_height}")

def enter_data():
    """Function for the button in this app. Gets all the nessesary variables. Print them to the terminal.

    Returns:
        List[Tuples[str,int,bool]] - a list of tuple that contains all the nessesary elements for insert it to the db. 
    """    
    # Grab the values that are needed
    accepted_terms = accept_var.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    user_title = title_combobox.get()
    age = int(age_spinbox.get())
    nationalitet = nationalitet_combobox.get()
    
    
    # Inverted checks to make the code more readable
    if accept_var.get() != "Accepted":
        showwarning(title="Accept terms and condition", message="You have not accepted terms and condition")
    
    # Using all() instead of writing an long OR-statement. 
    elif not all((first_name, last_name, user_title, age, nationalitet)):
        showwarning(title="Name missing", message="Please fill all the fields in User data section")
    
    else:
        courses = int(courses_spinbox.get())
        semesters = int(semesters_spinbox.get())
        registration_status = reg_var.get()
        print(f"First Name:{first_name}, Last Name: {last_name}")
        print(f"Title: {user_title}, Age: {age}")
        print(f"Registred on Courses: {courses}, Number of semesters: {semesters}")
        print(f"Terms and Conditions: {accepted_terms}")
        
    return [(user_title, first_name, last_name, age, nationalitet,registration_status, courses, semesters, accepted_terms)]

# Main app starts!
window = tk.Tk()
window.title(root_window_title)
define_root_window(root_window=window, center_root_window=True, root_window_height=window_height, root_window_width=window_width )

# create the root frame
root_frame = ttk.Frame(window)
root_frame.pack()

# User info
user_info_frame= tk.LabelFrame(master=root_frame, text="User data")
user_info_frame.pack(fill="both")

#First name
first_name_label = ttk.Label(master=user_info_frame, text="Förnamn")
first_name_label.grid(column=0, row=0)
first_name_entry = ttk.Entry(master=user_info_frame,)
first_name_entry.grid(column=0, row=1)

# Last name
last_name_label = ttk.Label(master=user_info_frame, text="Efternamn")
last_name_label.grid(column=1, row=0)
last_name_entry = ttk.Entry(master=user_info_frame)
last_name_entry.grid(column=1, row=1)

# Title
title_label = ttk.Label(master=user_info_frame, text="Title")    
title_label.grid(column=2, row=0)
title_combobox = ttk.Combobox(master=user_info_frame)
title_combobox["values"] = ("Herr", 
                            "Fru", 
                            "Frk", 
                            "Dr.",)   
title_combobox.grid(column=2, row=1)

# Age
age_label = ttk.Label(master=user_info_frame, text="Ålder")
age_label.grid(column=0, row=2)


age_spinbox = ttk.Spinbox(master=user_info_frame, from_=18, to=100,)
age_spinbox.grid(column=0, row=3)

# Nationality
nationalitet_label = ttk.Label(master=user_info_frame, text="Nationalitet")
nationalitet_label.grid(column = 1, row = 2)
continents = ("Europa","Asien", "Africa", "North America", "South America", "Antartica")
nationalitet_combobox = ttk.Combobox(master=user_info_frame, values=continents,)
nationalitet_combobox.grid(column=1, row=3)

# Create all padding for all the widgets. 
for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)


# Registration status
reg_frame = tk.LabelFrame(master=root_frame, text= "Registration")
reg_frame.pack(fill="both")

# Registration 
reg_label = ttk.Label(master=reg_frame, text="Registration Status").grid(column=0, row=0)
reg_var = tk.IntVar(value=0)
reg_checkbox = ttk.Checkbutton(master=reg_frame, text="Currently Registrated",variable=reg_var)
reg_checkbox.grid(column=0, row=1 )

# Courses
courses_label = ttk.Label(master=reg_frame, text="No. Completed Courses").grid(column=1, row=0)
courses_spinbox = ttk.Spinbox(master=reg_frame, from_=1, to="infinity")
courses_spinbox.grid(column=1, row=1)

semesters_label = ttk.Label(master=reg_frame, text="No. Semester").grid(column=2, row=0)
semesters_spinbox = ttk.Spinbox(master=reg_frame, from_=1, to="infinity")
semesters_spinbox.grid(column=2, row=1)

for widget in reg_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Terms and Conditions
terms_condition_frame = tk.LabelFrame(master=root_frame, text="Terms & Condition")
terms_condition_frame.pack(fill="both")
accept_var = tk.StringVar(value="Not Accepted")
accept_btn = ttk.Checkbutton(master=terms_condition_frame, text="I accept terms and condition", variable=accept_var, offvalue="Not Accepted", onvalue="Accepted")
accept_btn.grid(column=0, row=0, sticky="nesw")

for widget in terms_condition_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

#Submit button
submit_btn = ttk.Button(root_frame, text="Enter Data", command=lambda: insert_to_database(enter_data()))
submit_btn.pack(padx=10, pady= 5,fill="both")


if __name__=="__main__":
    # Run
    window.mainloop()