# Name: Valary Musibega
# Project: Credit Application Program
# Course: CS 3321
# Description: This class implements all the tasks handled by the program's interface, including user login, validation
# functions shared by the user classes and .csv filepath and initial parameter configuration.

import pandas as pd             # Importing pandas DataFrame library for data processing
from datetime import datetime   # Importing datetime library for functions using current system date and time.
from time import sleep          # Importing the sleep library to implement delay between functions.
import sys                      # Importing the sys library to detect operating system running the program.
import subprocess               # Importing the subprocess library for functions requiring access to subprocesses.
import re                       # Importing the re library to handle regular expressing for data validation.

#  Defined paths for .csv files.
AUTHORIZED_USERS_FILEPATH = "authorized_users.csv"
CREDIT_SCORES_FILEPATH = "credit_scores.csv"
THRESHOLDS_FILEPATH = "thresholds.csv"
APPLICATIONS_FILEPATH = "applications.csv"
APPROVALS_FILEPATH = "approvals.csv"

# Defined lists for constructing .csv files if none exist at program start time.
AUTHORIZED_USERS_COLUMNS = ["User ID",
                            "Name",
                            "Password"]
CREDIT_SCORES_COLUMNS = ["SSN",
                         "Credit Score"]
THRESHOLDS_COLUMNS = ["CSART",
                      "DtIRT",
                      "PFRLfC",
                      "MCL"]
APPLICATIONS_COLUMNS = ["Timestamp",
                        "Name",
                        "User ID",
                        "SSN",
                        "Monthly Income",
                        "Monthly Debts",
                        "Credit Score",
                        "Approval Status",
                        "Approved by ID"]
APPROVALS_COLUMNS = ["Timestamp",
                     "User ID",
                     "Credit Line Limit"]


#  Used by the program to obtain input and prompt in one single console line.
def get_input_with_prompt(prompt):
    print(prompt, end="")
    return input()


#  Used by the program to sleep the processor for x amount of seconds (default is 1) anc clear console screen.
def sleep_and_clear_screen(secs=1):
    sleep(secs)
    operating_system = sys.platform
    if operating_system == 'win32':
        subprocess.run('cls', shell=True)
    elif operating_system == 'linux' or operating_system == 'darwin':
        subprocess.run('clear', shell=True)


#  Used by the program to obtain a Timestamp object to add new rows in DataFrame object that require a timestamp.
def get_pandas_timestamp():
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp = pd.Timestamp(current_datetime)
    return timestamp


#  Opens a DataFrame object based on existing .csv filepaths. Otherwise, creates a new DataFrame object based on
#  existing .csv column lists.
def open_or_create_csv(filepath, column_names):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        df = pd.DataFrame(columns=column_names)
        df.to_csv(filepath, index=False)
    return df


#  Used by the program to validate login data provided by the session user. If successfully validated, the function
#  allows the session user to login by creating a respective class object based on the entered login data and its
#  respective DataFrame objects.
def validate_login(df, user_id, password):
    try:
        filtered_df = df[df['User ID'] == user_id]
        if len(filtered_df) == 1 and filtered_df['Password'].values[0] == password:
            return True
        else:
            print("\nIncorrect login information!")
            return False
    except KeyError:
        print("Error: Username or password column not found in DataFrame.")
        return False


#  Used by the program to inquire a session user for their user ID and password.
def login_prompt(users_list_df):
    sleep_and_clear_screen(1)
    print("Welcome to the system! Please insert your credentials below.\n")
    user_id = get_input_with_prompt("Enter your user ID: ")
    password = get_input_with_prompt("Enter your password: ")

    while validate_login(users_list_df, user_id, password) is False:
        print("Login failed.")
        sleep_and_clear_screen(1)
        print("Welcome to the system! Please insert your credentials below.\n")
        user_id = get_input_with_prompt("Enter your user ID: ")
        password = get_input_with_prompt("Enter your password: ")

    filtered_df = users_list_df[users_list_df['User ID'] == user_id]
    name = filtered_df['Name'].values[0]
    print(f"\nLogin successful! Welcome, {name}!")
    return name, user_id


# Used by the program to validate new SSN data.
def validate_ssn(ssn):
    pattern = r'^\d{3}-\d{2}-\d{4}$'
    if re.match(pattern, ssn):
        return True
    else:
        return False


# Used by the program to validate new user ID data.
def validate_user_id(user_id):
    pattern = r'^[A-C][0-9]{5}$'
    if re.match(pattern, user_id):
        return True
    else:
        return False


# Used by the program to validate new user's name date.
def validate_name(name):
    pattern = r'^[A-Z][a-z]+ [A-Z][a-z]+$'
    if re.match(pattern, name):
        return True
    else:
        return False
