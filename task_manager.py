#=====importing libraries===========
import os 
from datetime import datetime
#=====Define Functions=========
def create_user(new_user, new_pass, confirm_pass):
    existing_users = []
    with open("user.txt", "r") as f:
        for line in f:
            existing_users.append(line.strip().split(", ")[0])
    if new_user in existing_users[0]:
        print("Error! The username " + new_user + " already exists! Please try a different username!")
        return
    if new_pass == confirm_pass:
        with open("user.txt", "a") as f:
            f.write("\n" + new_user + ", " + new_pass)
            print("User created sucessfully!")
    else:
        print("Error: Passwords do not match!")
        return

def create_task(user, title, task_desc, due_date, current_date, task_complete):
    with open("tasks.txt", "a") as f:
        f.write("\n" + user + ", " + title + ", " + task_desc + ", " + str(current_date) + ", " + str(due_date) + ", " + task_complete)
    print("Task added successfully!")

def view_all():
    #Check if file exists.
    if not os.path.exists("tasks.txt"):
        print("File does not exist.")
        return
    #Open file tasks.txt in read mode.
    with open("tasks.txt", "r") as f:
        #Read all the lines of the text file.
        lines = f.readlines()
        #Check if the file is empty
        if not lines:
            print("File is empty.")
            return
        i = 1
        #For every line in lines, split the lines where there is ", ", print output.
        for line in lines:
            task = line.split(", ")
            #Check if the split list is not empty
            if not task:
                continue
            print(f"Task No:\t  {i}")
            print(f"Task:\t\t {task[1]}")
            print(f"Assigned to:\t {task[0]}")
            print(f"Date Assigned:\t {task[3]}")
            print(f"Due Date:\t {task[4]}")
            print(f"Task Complete:\t {task[5]}")
            print(f"Task Description:\n{task[2]}")
            print()
            i += 1



def view_Task():
    #Use os module to check whether file exists.
    if not os.path.exists("tasks.txt"):
        print("File does not exist.")
        return
    with open("tasks.txt", "r") as task_file:
        lines = task_file.readlines()
        if not lines:
            print("File is empty.")
            return
        #Create a dictionary to store task numbers and their corresponding line numbers
        task_numbers = {} 
        for i in range(len(lines)):
            line = lines[i]
            tasks = line.strip().split(", ")
            if tasks[0] == username:
                #Add task number and line to dictionary
                task_numbers[i+1] = line 
                print(f"Task No:\t  {i+1}")
                print(f"Task:\t\t {tasks[1]}")
                print(f"Assigned to:\t  {tasks[0]}")
                print(f"Date Assigned:\t {tasks[3]}")
                print(f"Due Date:\t {tasks[4]}")
                print(f"Task Complete:\t {tasks[5]}")
                print(f"Task Description:\n{tasks[2]}")
                print()
        #Ask user if they want to edit a task or return to main menu.        
        task_num = input("Enter task number to edit details or -1 to return to main menu:\n")
        if task_num == "-1":
            print("Returning to main menu!")
            return
        elif int(task_num) in task_numbers:
            task_line = task_numbers[int(task_num)]
            tasks = task_numbers[int(task_num)].strip().split(", ")
            print(tasks)
            print(f"Task No:\t  {task_num}")
            print(f"Task:\t\t {tasks[1]}")
            print(f"Assigned to:\t  {tasks[0]}")
            print(f"Date Assigned:\t {tasks[3]}")
            print(f"Due Date:\t {tasks[4]}")
            print(f"Task Complete:\t {tasks[5]}")
            print(f"Task Description:\n{tasks[2]}")
            print()
            
            #Ask user to mark the task as complete or edit the task, defensive if the task is already marked as complete.
            user_choice = input("Enter 1 to mark task as complete, 2 to edit task, or -1 to return to main menu:\n")
            if user_choice == "1":
                if tasks[5] == "No":
                    tasks[5] = "Yes"
                    task_numbers[int(task_num)] = ", ".join(tasks)
                    with open("tasks.txt", "w") as task_file:
                        task_file.write("\n".join(task_numbers.values()))
                    print("Task marked as complete.")
                else:
                    print("Task already marked as complete.")
            elif user_choice == "2":
                if tasks[5] == "Yes":
                    print("Task is already completed and cannot be edited.")
                else:
                    #Ask user to edit the user assigned to task or the due date.
                    edit_choice = input("Enter 1 to edit assigned to, 2 to edit due date:\n")
                    if edit_choice == "1":
                        tasks[0] = input("Enter new assigned to:\n")
                    elif edit_choice == "2":
                        tasks[4] = input("Enter new due date:\n")
                    task_numbers[int(task_num)] = ", ".join(tasks)
                    task_line = ",".join(tasks)
                    task_numbers[int(task_num)] = task_line
                    with open("tasks.txt", "w") as task_file:
                        task_file.write("\n".join(task_numbers.values()))
                    print("Task edited.")
            elif user_choice == "-1":
                return
            else:
                print("Invalid Task Number!")
        else:
            print("Invalid Task Number!")

def generate_report():
    try:
        #Open the tasks.txt file and read the lines
        with open("tasks.txt", "r") as f:
            task_lines = f.readlines()  
        if not task_lines:
            print("File is empty.")
            return         
        #Open the user.txt file and read the lines
        with open("user.txt", "r") as f:
            user_lines = f.readlines()
        if not user_lines:
            print("File is empty.")
            return

        completed_tasks = 0
        uncompleted_tasks = 0
        overdue_tasks = 0
        #Count the number of completed and uncompleted tasks, and overdue tasks
        for task_line in task_lines:
            task = task_line.strip().split(", ")
            if not task:
                continue
            #This took me ages to figure out how to do. COnvert format of date in .txt file to a readable format for datetime.
            due_date_object = datetime.strptime(task[4], '%d %b %Y')
            due_date_object = due_date_object.date()
            if task[5] == "Yes":
                completed_tasks += 1
            else:
                uncompleted_tasks += 1
                if due_date_object < datetime.now().date():
                    overdue_tasks += 1

        #Open the task_overview.txt file in write mode and write the report to the file
        with open("task_overview.txt", "w") as f:
            f.write("Total tasks: " + str(len(task_lines)) + "\n")
            f.write("Completed tasks: " + str(completed_tasks) + "\n")
            f.write("Uncompleted tasks: " + str(uncompleted_tasks) + "\n")
            f.write("Overdue tasks: " + str(overdue_tasks) + "\n")
            f.write("Uncomplete Percentage: " + str(round(uncompleted_tasks/len(task_lines)*100, 2)) + " % \n")
            f.write("Overdue Percentage: " + str(round(overdue_tasks/len(task_lines)*100, 2)) + " % \n")
        print("Task Overview Report generated in task_overview.txt")
        
        user_overview = {}
        user_overview["total_users"] = len(user_lines)
        user_overview["total_tasks"] = len(task_lines)
        
        #Tried the method of creating a dictionary to store the information for each user. This was very hard for me and i used a few resources like Stack Overflow.
        users = {}
        for user_line in user_lines:
            user = user_line.strip().split(", ")[0]
            users[user] = {"total_tasks": 0, "completed_tasks": 0, "uncompleted_tasks": 0, "overdue_tasks": 0}
        
        #Count the number of tasks assigned to each user, and completed/uncompleted/overdue tasks.
        for task_line in task_lines:
            task = task_line.strip().split(", ")
            if not task:
                continue
            due_date_object = datetime.strptime(task[4], '%d %b %Y')
            due_date_object = due_date_object.date()
            user = task[0]
            users[user]["total_tasks"] += 1
            if task[5] == "Yes":
                users[user]["completed_tasks"] += 1
            else:
                users[user]["uncompleted_tasks"] += 1
                if due_date_object < datetime.now().date():
                    users[user]["overdue_tasks"] += 1

        #Calculate the percentages for each user
        for user in users:
            users[user]["task_percentage"] = (users[user]["total_tasks"] / user_overview["total_tasks"]) * 100
            users[user]["completed_percentage"] = (users[user]["completed_tasks"] / users[user]["total_tasks"]) * 100
            users[user]["uncompleted_percentage"] = (users[user]["uncompleted_tasks"] / users[user]["total_tasks"]) * 100
            try:
               users[user]["overdue_percentage"] = (users[user]["overdue_tasks"] / users[user]["uncompleted_tasks"]) * 100
            except ZeroDivisionError:
                users[user]["overdue_percentage"] = ("0.0 %")

        #Open the user_overview.txt file in write mode and write the report to the file.
        with open("user_overview.txt", "w") as f:
            f.write("Total users: " + str(user_overview["total_users"]) + "\n")
            f.write("Total tasks: " + str(user_overview["total_tasks"]) + "\n")
            for user in users:
                f.write("\n" + user + "\n")
                f.write("Total tasks: " + str(users[user]["total_tasks"]) + "\n")
                f.write("Task percentage: " + str(users[user]["task_percentage"]) + "% \n")
                f.write("Completed tasks: " + str(users[user]["completed_tasks"]) + "\n")
                f.write("Completed percentage: " + str(users[user]["completed_percentage"]) + "% \n")
                f.write("Uncompleted tasks: " + str(users[user]["uncompleted_tasks"]) + "\n")
                f.write("Uncompleted percentage: " + str(users[user]["uncompleted_percentage"]) + "% \n")
                f.write("Overdue tasks: " + str(users[user]["overdue_tasks"]) + "\n")
                f.write("Overdue percentage: " + str(users[user]["overdue_percentage"]) + "% \n")
        print("User Overview Report generated in user_overview.txt")    
    except FileNotFoundError:
        print("File does not exist.")

def display_stats():
    #Check if task_overview.txt and user_overview.txt exist, if not call the function to create.
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_report()
    #If they exist, open both file in read mode.
    with open("task_overview.txt", "r") as task_file:
        with open("user_overview.txt", "r") as user_file:
            task_lines = task_file.readlines()
            user_lines = user_file.readlines()
        #Check oif file is empty.
        if not task_lines or not user_lines:
            print("Statistics files are empty.")
            return
        print("Task Statistics:")
        #For every line in task_lines, print the line.
        for line in task_lines:
           print(line)
        #For every line in user_lines, print the line.
        print("\nUser Statistics:")
        for line in user_lines:
           print(line)

#====Login Section====
#Open the user text file.
with open("user.txt", "r") as f:
    #Read all the lines of the text file.
    lines = f.readlines()
    #Define two empty lists, one for usernames and one for passwords.
    usernames_list = []
    passwords_list = []

    #For every line in lines.
    for line in lines:
        #Strip the username and password of the whitespace and split using (","").
        #Took me ages to figure out why my program wasnt working because of the whitespace so i used .strip to remove whitespace from password.
        username1, password1 = line.strip().split(", ")
        password1 = password1.strip()
        #Append the username and password to the right list.
        usernames_list.append(username1)
        passwords_list.append(password1)
    
    #Define being logged in as false.
    logged_in = False
    #While not to continually execute loop until condition is met.
    while not logged_in:
        username = input("Enter your username:\n")
        password = input("Enter your password:\n")
        #If username is in username_list and password is in password_list.
        if username in usernames_list and password in passwords_list:
            #Change logged_in to True.
            logged_in = True
            print(f"Welcome {username}. You are now logged in!")
        #Else re-loop and print error message.  
        else:
            print("Invalid username or password! Please try again!")
        
while True:
    if username == usernames_list[0]:
        menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate Reports
        st - Statistics
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

    if menu == 'r':
        
        print()
        print("Registering a new user!")
        #Request new user, password and to confirm password.
        if username == usernames_list[0]:
            new_user = input("Enter a new username:\n")
            new_pass = input("Enter a new password:\n")
            confirm_pass = input("Confirm the password!\n")
            #Call function create_user.
            create_user(new_user, new_pass, confirm_pass)
        else:
            print("Only user admin can create a new username! Please log in as admin!")

    elif menu == 'a':

        print()
        print = ("Adding a task!")
        #Ask user for user, task title, description of task, due date, current date and whether task is complete.
        user = input("Which user is this task to be assigned to?\n")
        title = input("What is the title of the task?\n")
        task_desc = input("What does the task entail?\n")
        due_date = input("When is the task due by? (Eg 01 Jan 2023)\n")
        current_date = input("What is the current date? (Eg 01 Jan 2023)\n")
        task_complete = input("Is the task complete (Yes or No)\n")
        #Call function create_task.
        create_task(user, title, task_desc, due_date, current_date, task_complete)

    elif menu == 'va':
        
        print()
        print("View all Tasks!")
        #Call function "view_all".
        view_all()


    elif menu == 'vm':        

        print()
        print("View your Tasks!")
        #Call function "view_Task".
        view_Task()

    elif menu == 'gr':
        #Call function "generate_report".
        generate_report()

    elif menu == 'st':
        #Call funtion to "display_stats".
        display_stats()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")