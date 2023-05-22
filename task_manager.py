
#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Functions

# Registers a new user to the user.txt file
def reg_user():

    while True:
        # - Request input of a new username
        new_username = input("New Username: ")
        username_taken = False

        # - Checks if username already exists
        for username in username_password:
            if username == new_username:
                print("Error, Username taken\nPlease try a different username")
                username_taken = True

        # Exits loop if username is not taken        
        if username_taken == False:
            break
        
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
                
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
                        
        with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

# Allows a user to add a new task to the task.txt file
def add_task():

    '''Prompt a user for the following: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - the due date of the task.'''
    
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    else:
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                    print("Invalid datetime format. Please use the format specified")
               # Then get the current date.

        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
            

# Reads the tasks from the task.txt file and prints to the console
def view_all():

    for t in task_list:
         disp_str = f"Task: \t\t {t['title']}\n"
         disp_str += f"Assigned to: \t {t['username']}\n"
         disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
         disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
         disp_str += f"Task Description: \n {t['description']}\n"
         print(disp_str)

# Prints the users tasks and allows them to edit the task
def view_mine():

    counter = 1

    for t in task_list:
        if t['username'] == curr_user:
            disp_str = "\nTask: " + str(counter) + f"\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            counter+=1
            print(disp_str)
        else: 
            counter+=1


    # Loops until the user enters -1 or a valid task number
    while True:

        selected_task = int(input("Enter task number to select a task or enter -1 to exit: "))

        if (selected_task == -1)  or (selected_task > 0 and selected_task <= counter):
            break
        else:
            print("Only enter valid task numbers or -1 to exit, please try again")
    
    # If user does not enter -1 
    if selected_task != -1:
        options_select = input("Enter 'm' to mark task as complete or 'e' to edit task: ")
        options_select = options_select.lower()

        if options_select == 'm':

            task_list[selected_task-1]["completed"] = True

            # Writes updated task information to the file
            with open("tasks.txt", "w") as task_file:
                
                for t in task_list:
                    task_list_to_write = []
                    str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ] 
                    task_list_to_write.append(";".join(str_attrs) + "\n")
                    task_file.write("".join(task_list_to_write))

        
        elif options_select == 'e':

            if task_list[selected_task-1]["completed"] == True:
                print("You cannot edit a task that has been completed")
            
            else:

                new_username = input("Enter the new username: ")

                # Loops until date is entered in correct format
                while True:
                    try:
                        task_due_date = input("Enter new due date of the task (YYYY-MM-DD): ")
                        new_due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                        break

                    except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                    
                # Assigns the new values to the selected task
                task_list[selected_task-1]["username"] = new_username
                task_list[selected_task-1]["due_date"] = new_due_date_time

                # Writes updated task information to the file
                with open("tasks.txt", "w") as task_file:
                    
                    for t in task_list:
                        task_list_to_write = []
                        str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ] 
                        task_list_to_write.append(";".join(str_attrs) + "\n")
                        task_file.write("".join(task_list_to_write))

        # Error message
        elif options_select != 'e' and options_select != 'm':
            print("Error, incorrect input")
               
                    
# Generates the task and user overview files
def generate_reports():

    # Task Overview

    # Creates file
    overview_task_file = open("task_overview.txt", "w")

    total_tasks = len(task_list)
    current_date = datetime.today()
    completed_tasks = 0
    incomplete_tasks = 0
    incomplete_overdue_tasks = 0

    # Loops through task_list 
    for i in range(0, len(task_list)):
        if task_list[i]["completed"] == True:
            completed_tasks += 1
        else:
            incomplete_tasks += 1
            if current_date > task_list[i]["due_date"]:
                incomplete_overdue_tasks += 1

    # Calculates the percentage variables
    percent_tasks_incompleted = (completed_tasks/total_tasks)*100
    percent_tasks_overdue = (incomplete_overdue_tasks/total_tasks) * 100

    # Writes the information to the file
    overview_task_file.write(''' Tasks Overview:
    Total Tasks: {0}
    Completed Tasks: {1}
    Incomplete Tasks: {2}
    Overdue Incomplete Tasks: {3}
    Percentage Of Tasks That Are Incomplete: {4}%
    Percentage Of Tasks That Are Overdue: {5}%
    '''.format(str(total_tasks), str(completed_tasks), str(incomplete_tasks), str(incomplete_overdue_tasks), str(percent_tasks_incompleted), str(percent_tasks_overdue)))

    # Closes file
    overview_task_file.close()

    # User Overview

    # Creates the file
    overview_user_file = open("user_overview.txt", "w")

    total_users = len(username_password)
    user_overview = "User Overview:\n\tNumber Of Users: " + str(total_users) + "\n\tTotal Number Of Tasks: " + str(total_tasks) + "\n"

    # Loops through the users
    for i in username_password:

        total_tasks_user = 0
        completed_user_tasks = 0
        incomplete_user_tasks = 0
        overdue_user_tasks = 0
        percent_task_user= 0
        percent_task_user_completed = 0
        percent_task_user_incomplete = 0
        percent_incomplete_overdue_tasks_user = 0

        # Loops through the tasks
        for j in range(0, total_tasks):
            if task_list[j]["username"] == i:
                total_tasks_user+=1
                
                if task_list[j]["completed"] == True:
                    completed_user_tasks += 1
                else:
                    incomplete_user_tasks += 1
                    if current_date > task_list[j]["due_date"]:
                        overdue_user_tasks += 1
        
        # Calculates the percentage variables
        percent_task_user = (total_tasks_user/total_tasks)*100

        # Makes sure that there is not a division by zero
        if total_tasks_user != 0:
            percent_task_user_completed = (completed_user_tasks/total_tasks_user)*100
            percent_task_user_incomplete = (incomplete_user_tasks/total_tasks_user)*100
            percent_incomplete_overdue_tasks_user = (overdue_user_tasks/total_tasks_user)*100

        user_overview += '''
        User: {0}
        Percentage Of Total Number Of Tasks Assigned: {1}%
        Percentage Of Tasks Assigned To The User Completed: {2}%
        Percentage Of Tasks Assigned To The User That Are Incomplete: {3}%
        Percentage Of Tasks Assigned To The User That Are Incomplete And Overdue: {4}%
        \n
        '''.format(i,str(percent_task_user), str(percent_task_user_completed), str(percent_task_user_incomplete),str(percent_incomplete_overdue_tasks_user))

    # Writes to the file
    overview_user_file.write(user_overview)

    # Closes the file
    overview_user_file.close()

    print("Reports Generated")
        




logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
: ''').lower()
    
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr' and curr_user == 'admin':
        generate_reports()
 
    elif menu == 'ds' and curr_user == 'admin': 
        #If the user is an admin they can display statistics

        generate_reports()

        # Prints the task_overview file
        with open("task_overview.txt", "r") as task_overview:
            print(task_overview.read())

        print("-------------------------------------------------\n")

        # Prints the user_overview file
        with open("user_overview.txt", "r") as user_overview:
            print(user_overview.read())


    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")

