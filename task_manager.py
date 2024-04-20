'''Pseudo code:
Define DATETIME_STRING_FORMAT as "%Y-%m-%d"

Function check_and_create_file(file_name):
    If file_name does not exist:
        Create file_name

Function read_tasks_from_file():
    Open "tasks.txt" for reading
    Read task data and split by newline
    Filter out empty strings from task data
    For each task string in task data:
        Split task string by semicolon into task components
        If there are exactly 6 components:
            Create a task dictionary with username, title, description, due_date, assigned_date, and completed status
            Add task dictionary to task list
        Else:
            Print an error message indicating an invalid task line
    Return task list

Function read_users_from_file():
    Open "user.txt" for reading
    Read user data and split by newline
    For each user string in user data:
        Split user string by semicolon into username and password
        If there are exactly 2 components:
            Add username and password to username_password dictionary
        Else:
            Print an error message indicating an invalid user line
    Return username_password dictionary

Function login(username_password):
    While not logged_in:
        Prompt for username and password
        If username is in username_password and password matches:
            Print login successful message
            Set logged_in to True
        Else:
            Print error message and continue loop

Function main_menu():
    While True:
        Display menu options
        Get user input for menu selection
        If menu selection is 'r':
            Call function to register a new user
        If menu selection is 'a':
            Call function to add a new task
        If menu selection is 'va':
            Call function to view all tasks
        If menu selection is 'vm':
            Call function to view tasks assigned to the current user
        If menu selection is 'gr' and user is admin:
            Call function to generate reports
        If menu selection is 'ds' and user is admin:
            Call function to display statistics
        If menu selection is 'e':
            Exit the program

Function reg_user(username_password):
    Prompt for new username and password
    If new username does not exist in username_password:
        Add new username and password to username_password
        Write updated username_password to "user.txt"
    Else:
        Print error message and prompt again

Function add_task(task_list):
    Prompt for task details (username, title, description, due date)
    If username exists in username_password:
        Create a new task dictionary with the provided details and current date as assigned_date
        Add new task to task_list
        Write updated task_list to "tasks.txt"
    Else:
        Print error message

Function view_all(task_list):
    For each task in task_list:
        Display task details in a formatted manner

Function view_mine(task_list, current_user):
    Display tasks assigned to current_user with a corresponding number
    Prompt for task number selection or '-1' to return to main menu
    If a specific task is selected:
        Prompt to mark the task as complete or edit the task
        If marking as complete:
            Update task's completed status to True
            Write updated task_list to "tasks.txt"
        If editing the task:
            Prompt for new username or due date
            Update task details
            Write updated task_list to "tasks.txt"

Function generate_reports(task_list, username_password):
    Calculate and write task and user statistics to "task_overview.txt" and "user_overview.txt"

Function display_statistics():
    Read and display contents of "task_overview.txt" and "user_overview.txt"

// Main program execution starts here
check_and_create_file("tasks.txt")
check_and_create_file("user.txt")
task_list = read_tasks_from_file()
username_password = read_users_from_file()
login(username_password)
main_menu()
'''



import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function Definitions
def check_file_exists(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w") as default_file:
            if file_name == "user.txt":
                default_file.write("admin;password")

def read_tasks():
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
    return task_data

def convert_task_data(task_data):
    task_list = []
    for t_str in task_data:
        task_components = t_str.split(";")
        task_list.append({
            'username': task_components[0],
            'title': task_components[1],
            'description': task_components[2],
            'due_date': datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
            'assigned_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
            'completed': True if task_components[5] == "Yes" else False
        })
    return task_list

def read_users():
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
    return user_data

def convert_user_data(user_data):
    username_password = {}
    for user in user_data:
        parts = user.split(';')
        if len(parts) == 2:
            username, password = parts
            username_password[username] = password
        else:
            print(f"Invalid line in user.txt: {user}")
    return username_password

def convert_task_data(task_data):
    task_list = []
    for t_str in task_data:
        parts = t_str.split(";")
        if len(parts) == 6:
            task_list.append({
                'username': parts[0],
                'title': parts[1],
                'description': parts[2],
                'due_date': datetime.strptime(parts[3], DATETIME_STRING_FORMAT),
                'assigned_date': datetime.strptime(parts[4], DATETIME_STRING_FORMAT),
                'completed': parts[5] == "Yes"
            })
        else:
            print(f"Invalid line in tasks.txt: {t_str}")
    return task_list

def login(username_password):
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password:
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
    return curr_user

def reg_user(username_password):
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username already exists. Try a different username.")
    else:
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print("New user added successfully.")
            username_password[new_username] = new_password
            with open("user.txt", "a") as out_file:  # Open file in append mode
                out_file.write(f"{new_username};{new_password}\n")
        else:
            print("Passwords do not match. Try again.")

def add_task(username_password, task_list):
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    write_tasks(task_list)

def write_tasks(task_list):
    with open("tasks.txt", "w") as task_file:
        for t in task_list:
            task_file.write(f"{t['username']};{t['title']};{t['description']};"
                            f"{t['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                            f"{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                            f"{'Yes' if t['completed'] else 'No'}\n")
    print("Task successfully added.")

def view_all(task_list):
    for t in task_list:
        print(f"Task: \t\t {t['title']}\n"
              f"Assigned to: \t {t['username']}\n"
              f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
              f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
              f"Task Description: \n {t['description']}\n")

def view_mine(task_list, curr_user):
    user_tasks = [t for t in task_list if t['username'] == curr_user]
    for i, task in enumerate(user_tasks):
        print(f"{i + 1} - Task: \t\t {task['title']}\n"
              f"Assigned to: \t {task['username']}\n"
              f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
              f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
              f"Task Description: \n {task['description']}\n")
    task_number = int(input("Enter the number of the task to select it, or '-1' to return to the main menu: "))
    if task_number == -1:
        return
    selected_task = user_tasks[task_number - 1]
    if not selected_task['completed']:
        edit_or_complete = input("Would you like to mark this task as complete (c) or edit the task (e)? ").lower()
        if edit_or_complete == 'c':
            selected_task['completed'] = True
            write_tasks(task_list)
        elif edit_or_complete == 'e':
            edit_task(selected_task, task_list)
    else:
        print("This task is already completed.")

def edit_task(task, task_list):
    edit_choice = input("Would you like to edit the username (u) or the due date (d)? ").lower()
    if edit_choice == 'u':
        new_username = input("Enter the new username for the task: ")
        task['username'] = new_username
    elif edit_choice == 'd':
        new_due_date = input("Enter the new due date for the task (YYYY-MM-DD): ")
        task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
    write_tasks(task_list)

def generate_reports(task_list, username_password):
    with open("task_overview.txt", "w") as task_overview_file:
        total_tasks = len(task_list)
        completed_tasks = len([t for t in task_list if t['completed']])
        uncompleted_tasks = total_tasks - completed_tasks
        overdue_tasks = len([t for t in task_list if not t['completed'] and t['due_date'] < datetime.now()])
        task_overview_file.write(f"Total number of tasks: {total_tasks}\n"
                                 f"Total number of completed tasks: {completed_tasks}\n"
                                 f"Total number of uncompleted tasks: {uncompleted_tasks}\n"
                                 f"Total number of overdue tasks: {overdue_tasks}\n"
                                 f"Percentage of tasks incomplete: {(uncompleted_tasks / total_tasks) * 100:.2f}%\n"
                                 f"Percentage of tasks overdue: {(overdue_tasks / total_tasks) * 100:.2f}%\n")

    with open("user_overview.txt", "w") as user_overview_file:
        total_users = len(username_password)
        user_overview_file.write(f"Total number of users: {total_users}\n"
                                 f"Total number of tasks: {total_tasks}\n")
        for username in username_password:
            user_tasks = [t for t in task_list if t['username'] == username]
            num_user_tasks = len(user_tasks)
            completed_user_tasks = len([t for t in user_tasks if t['completed']])
            uncompleted_user_tasks = num_user_tasks - completed_user_tasks
            overdue_user_tasks = len([t for t in user_tasks if not t['completed'] and t['due_date'] < datetime.now()])
            user_overview_file.write(f"User: {username}\n"
                                     f"Total number of tasks assigned: {num_user_tasks}\n"
                                     f"Percentage of total tasks: {(num_user_tasks / total_tasks) * 100:.2f}%\n"
                                     f"Percentage of tasks completed: {(completed_user_tasks / num_user_tasks) * 100:.2f}% if num_user_tasks > 0 else 0.00%\n"
                                     f"Percentage of tasks incomplete: {(uncompleted_user_tasks / num_user_tasks) * 100:.2f}% if num_user_tasks > 0 else 0.00%\n"
                                     f"Percentage of tasks overdue: {(overdue_user_tasks / num_user_tasks) * 100:.2f}% if num_user_tasks > 0 else 0.00%\n")

def display_statistics(username_password, task_list):
    # Read the most recent user and task data
    username_password = read_users_from_file()
    task_list = read_tasks_from_file()

    # Generate or read the reports if they exist
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports(task_list, username_password)
    
    # Display the contents of the report files
    with open("task_overview.txt", "r") as task_overview_file:
        print(task_overview_file.read())
    with open("user_overview.txt", "r") as user_overview_file:
        print(user_overview_file.read())

# Main Program
check_file_exists("tasks.txt")
check_file_exists("user.txt")

task_data = read_tasks()
task_list = convert_task_data(task_data)

user_data = read_users()
username_password = convert_user_data(user_data)

curr_user = login(username_password)

while True:
    print()
    if curr_user == 'admin':
        menu = input("Select one of the following Options below:\n"
                     "r - Registering a user\n"
                     "a - Adding a task\n"
                     "va - View all tasks\n"
                     "vm - View my task\n"
                     "gr - Generate reports\n"
                     "ds - Display statistics\n"
                     "e - Exit\n: ").lower()
    else:
        menu = input("Select one of the following Options below:\n"
                     "a - Adding a task\n"
                     "va - View all tasks\n"
                     "vm - View my task\n"
                     "e - Exit\n: ").lower()

    if menu == 'r' and curr_user == 'admin':
        reg_user(username_password)
    elif menu == 'a':
        add_task(username_password, task_list)
    elif menu == 'va':
        view_all(task_list)
    elif menu == 'vm':
        view_mine(task_list, curr_user)
    elif menu == 'gr' and curr_user == 'admin':
        generate_reports(task_list, username_password)
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics(username_password, task_list)
    elif menu == 'e':
        print('Goodbye!!!')
        break
    else:
        print("You have made a wrong choice, Please Try again")
