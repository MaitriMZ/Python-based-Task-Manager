"""
Program to do user registration and maintain a list of Tasks
It also has the functionality to generate reports on user and tasks
Notes:
    1. I amended the class definition to add the index - primary for the tasks
    2. tasks.txt file is now using the ; as separator
"""
# os to be used for existing file - if not then we go ahead creating a new one
import os
# datetime library to be used for date formats and functionalities around dates
from datetime import datetime, date

# Changed the formt to match to the tasks.py file
# Also removed leading spaces from the dates on tasks.py file
DATETIME_STRING_FORMAT = "%d %b %Y"

# Added the attribute 'index' to maintain primary key on the tasks
# This class has all the attribute for the tasks and
# functions for string operations and displaying it


class Task:
    def __init__(self, index=None, username=None, title=None,
                 description=None, due_date=None, assigned_date=None,
                 completed=None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.index = index
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(";")     # splitting it by , as per tasks.txt
        index = tasks[0]
        username = tasks[1]
        title = tasks[2]
        description = tasks[3]
        due_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[5], DATETIME_STRING_FORMAT)
        completed = True if tasks[6] == "Yes" else False
        self.__init__(index, username, title, description, due_date,
                      assigned_date, completed)

    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.index,      # Adding a primary key to the task.py file
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        # Added proper alignments so that values are aligned properly
        disp_str = f"Index: \t\t\t\t{self.index}\n"
        disp_str += f"Task: \t\t\t\t{self.title}\n"
        disp_str += f"Assigned to: \t\t{self.username}\n"
        disp_str += (f"Date Assigned: \t\t"
                     f"{self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n")
        disp_str += (f"Due Date: \t\t\t"
                     f"{self.due_date.strftime(DATETIME_STRING_FORMAT)}\n")
        disp_str += f"Task Description: \t{self.description}\n"
        disp_str += f"Completion Status: \t{self.completed}\n"
        return disp_str


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Read data into task_list of type class
task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    # print(user_data)

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')   # Splitting by , as per the file
    username_password[username] = password

# Keep trying until a successful login
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


def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True


def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True


def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))


# Function to register a user
def reg_user(curr_user):
    # Only admin users can create new users
    if curr_user != 'admin':
        print("Registering new users requires admin privileges")
        return
    # Initializing variables for duplicate user check
    duplicate_user = 'No'
    setup_new_user_flag = 'YES'
    # Request input of a new username and password
    while setup_new_user_flag == 'YES':
        new_username = input("New Username: ")
        setup_new_user_flag = 'NO'
        # Duplicate user check
        for u_name in username_password.keys():
            if new_username == u_name:
                # print message for the duplicate user
                print("User name you entered already exists")
                duplicate_user = 'Yes'
        if duplicate_user == 'Yes':
            duplicate_user = 'No'
            # Ask user if he/she wishes to continue
            setup_new_user_flag = input("Do you want to continue?"
                                        "(Yes / No):").upper()
            if setup_new_user_flag == 'YES':
                # while loop will continue if user wishes to add more users
                continue
            elif setup_new_user_flag == 'NO':
                # Return to main menu if user does not want to continue
                return
            else:
                # display invalid input message and return to main menu
                print("Invalid Input")
                return

        new_password = input("New Password: ")
        # Condition to validate Username or password is not safe for storage
        if not check_username_and_password(new_username, new_password):
            return
        # Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
            # Add to dictionary and write to file
            username_password[new_username] = new_password
            write_usernames_to_file(username_password)
            # Once everything is successful, display the confirmation
            print("New user added")
        # Otherwise you present a relevant message.
        else:
            print("Passwords do no match")


# Function to add a task
def add_task():
    # Prompt a user for the following:
    #     A username of the person whom the task is assigned to,
    #     A title of a task,
    #     A description of the task and
    #     the due date of the task.

    # Ask for username
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    # Get title of task and ensure safe for storage
    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break

    # Get description of task and ensure safe for storage
    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break

    # Obtain and parse due date
    while True:
        try:
            # Changing the date format to DD MON YYYY to match tasks.py
            task_due_date = input("Due date of task (DD MON YYYY): ")
            due_date_time = datetime.strptime(task_due_date,
                                              DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Obtain and parse current date
    curr_date = date.today()

    # Create a new Task object and append to list of tasks
    new_task = Task(str(len(task_list)+1), task_username, task_title,
                    task_description, due_date_time, curr_date, False)
    task_list.append(new_task)

    # Write to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")


# Function to view all tasks
def view_all():
    print("-----------------------------------")
    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")


# Function to view my tasks - tasks specific to user who is logged in
def view_mine():
    print("-----------------------------------")
    has_task = False
    for t in task_list:
        if t.username == curr_user:     # checks the current user
            has_task = True
            print(t.display())
            print("-----------------------------------")

    if not has_task:                    # no tasks to be displayed
        print("You have no tasks.")
        print("-----------------------------------")

    # Condition to check whether the user has tasks
    # Only then display the option to edit it
    if has_task is True:
        edit_y_n = input("Do you want to edit the task? (Yes / No): ").upper()
        if edit_y_n == 'YES':
            edit_index = input("Please enter task index you want to edit"
                               " or enter -1 to return to the main menu: ")
        else:
            return

        # Return if the option selected is -1
        if edit_index == '-1':
            return
        else:
            task_found = 'No'
            # logic to locate the task number and accept the new values
            for t in task_list:
                if (t.index == edit_index) and (t.username == curr_user):
                    task_found = 'Yes'
                    if t.completed is True:
                        # Allows amend only when the task is not complete
                        print("\nSorry this task is already marked as "
                              "completed. You cannot edit it further")
                    # Calls a separate function to amend the task
                    else:
                        amend_task(t)
            # display a message if the asked task is not found
            if task_found == 'No':
                print("Task with this index is not assigned to you")
                return


# Function to amend the task
def amend_task(t):
    # Accept the actions
    user_input = input("Select Action: (Complete / Edit): ").upper()
    # If action is complete
    if user_input == 'COMPLETE':
        user_response = input("Mark as Complete (Yes / No)? ").upper()
        # sets the new value
        t.completed = True if user_response == "YES" else False

    # If action is edit then accept and assign new values
    elif user_input == 'EDIT':
        t.username = input("Enter the new assigned to: ")
        if t.username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            return
        task_due_date = input("Due date of task (DD MON YYYY): ")
        t.due_date = datetime.strptime(task_due_date,
                                       DATETIME_STRING_FORMAT)
    else:
        print("Invalid input")

    # Write to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully edited.")


# Generate report function
def generate_reports():
    with open("task_overview.txt", "w") as task_file:
        # Initilize variables
        completed_tasks = 0
        overdue_tasks = 0
        # Start writing the file
        task_file.write("This file gives you tasks overview\n")
        task_file.write("----------------------------------\n")
        # Calculate total tasks
        task_file.write(f"{'Total Tasks':<30}{len(task_list):.0f}\n")
        for t in task_list:
            if t.completed is True:     # Calculate complete tasks
                completed_tasks += 1
            if ((t.completed is not True) and
               (t.due_date < datetime.now())):
                overdue_tasks += 1      # Calculate overdue tasks

        task_file.write(f"{'Completed Tasks':<30}{completed_tasks:.0f}\n")
        # Calculate INcomplete tasks
        task_file.write(f"{'Incomplete Tasks':<30}"
                        f"{len(task_list) - completed_tasks:.0f}\n")
        task_file.write(f"{'Overdue Tasks':<30}{overdue_tasks:.0f}\n")
        # Calculate incomplete tasks percentage
        inco_perc = ((len(task_list) - completed_tasks) * 100) / len(task_list)
        task_file.write(f"{'Incomplete Tasks Percentage':<30}{inco_perc:.2f}\n")
        # Calculate overdue tasks percentage
        overdue_perc = (overdue_tasks * 100) / len(task_list)
        task_file.write(f"{'Overdue Tasks Percentage':<30}{overdue_perc:.2f}\n")

    # user_overview.txt file in write mode
    with open("user_overview.txt", "w") as task_file1:
        task_file1.write("This file gives you user and tasks Overview\n")
        task_file1.write("-------------------------------------------\n")

        # calculate Total registered user
        task_file1.write(f"{'Total Registered users':<50}"
                         f"{len(username_password):.0f}\n")
        # Calculate total tasks
        task_file1.write(f"{'Total Tasks':<50}{len(task_list):.0f}\n")

        for user in username_password.keys():
            # Initializing variables
            total_user_tasks, user_comp_tasks, user_incomp_tasks = 0, 0, 0
            user_overdue_tasks = 0
            user_tasks_perc = 0
            user_task_comp_perc = 0
            user_task_must_comp_perc = 0
            user_tasks_overdue_perc = 0
            for task in task_list:
                if task.username == user:
                    total_user_tasks += 1   # Count total user tasks
                    if task.completed is True:
                        user_comp_tasks += 1  # Count user completed tasks
                    else:
                        user_incomp_tasks += 1  # User incomplete tasks
                    if ((task.completed is not True) and
                       (task.due_date < datetime.now())):
                        user_overdue_tasks += 1  # User overdue tasks
            # Calculate the stats only when the tasks are assigned to the user
            # This is to avoid devide by zero error
            if total_user_tasks > 0:
                user_tasks_perc = (total_user_tasks * 100) / len(task_list)
                user_task_comp_perc = ((user_comp_tasks * 100) /
                                       total_user_tasks)
                user_task_must_comp_perc = ((user_incomp_tasks * 100) /
                                            total_user_tasks)
                user_tasks_overdue_perc = ((user_overdue_tasks * 100) /
                                           total_user_tasks)

            task_file1.write(f"\nUser {user} Overview\n")
            task_file1.write("---------------------\n")
            task_file1.write(f"{'Total Tasks':<50}{total_user_tasks:.0f}\n")
            task_file1.write(f"{'User Tasks percentage':<50}"
                             f"{user_tasks_perc:.2f}\n")
            task_file1.write(f"{'User Tasks Completed Percentage':<50}"
                             f"{user_task_comp_perc:.2f}\n")
            task_file1.write(f"{'User Tasks Must be Completed Percentage':<50}"
                             f"{user_task_must_comp_perc:.2f}\n")
            task_file1.write(f"{'User Tasks Overdue Percentage':<50}"
                             f"{user_tasks_overdue_perc:.2f}\n")
        print("Reports generated successfully")


def display_stats():
    # Check whether the file exists. If not then call generate_report function
    if not (os.path.exists("task_overview.txt") and
            os.path.exists("task_overview.txt")):
        generate_reports()

    # Read and print the task_overview.txt file
    with open("task_overview.txt", "r") as task_file:
        print("\n\n*****************************************")
        print("This is the task_overview.txt file report")
        print("*****************************************")
        for line_task in task_file:
            print(line_task, end="")
    # Read and print the user_overview.txt file
    with open("user_overview.txt", "r") as task_file1:
        print("\n\n*****************************************")
        print("This is the user_overview.txt file report")
        print("*****************************************")
        for line_user in task_file1:
            print(line_user, end="")


#########################
# Main Program
#########################
while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    if menu == 'r':  # Register new user (if admin)
        reg_user(curr_user)
    elif menu == 'a':  # call add a new task function
        add_task()
    elif menu == 'va':  # call view all tasks function
        view_all()
    elif menu == 'vm':  # Call view my tasks function
        view_mine()
    elif menu == 'gr':  # Call generate reports function
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':  # If admin, display statistics
        display_stats()  # Call display_stats function

    elif menu == 'e':  # Exit program
        print('Goodbye!!!')
        break       # break keyword needs to be used to come out of the loop
        # exit
    else:  # Default case
        print("You have made a wrong choice, Please Try again")
