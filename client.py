# Name: William Mock
# Project: Credit Application Program
# Course: CS 3321
# Description: This class implements all the tasks assigned to the client user, as well as auxiliary functions
# necessary for the correct functioning of the class' main functions.

import pandas as pd  # Importing pandas DataFrame library for data processing
import interface  # Importing for access to auxiliary functions.


# Client class constructor and parameter definitions.
class Client:
    def __init__(self, name, user_id, applications_df, approvals_df):
        self.__name = name
        self.__user_id = user_id
        self.__applications_df = applications_df
        self.__approvals_df = approvals_df

    def get_name(self):
        return self.__name

    def get_user_id(self):
        return self.__user_id

    def get_applications_df(self):
        return self.__applications_df

    def get_approvals_df(self):
        return self.__approvals_df

    def set_applications_df(self, applications_df):
        self.__applications_df = applications_df

    #  Main menu GUI and navigation logic.
    def main_menu(self):
        option = 0
        try:
            condition = True
            while condition is True:
                interface.sleep_and_clear_screen(1)
                print("Welcome, " + self.get_name() + "!")
                print("-------------------------------------------------------------------------------------------")
                print("1. Open an Application")
                print("2. View Previous Applications")
                print("3. View Approved Lines of Credit")
                print("4. Logout")
                print("-------------------------------------------------------------------------------------------")
                option = interface.get_input_with_prompt("Select your option: ")
                condition = int(option) < 1 or int(option) > 4
        except ValueError:
            print("Input is not valid. Please try again.")
            interface.sleep_and_clear_screen(1)
            self.main_menu()

        match option:
            case "1":
                self.new_application()
            case "2":
                self.previous_applications()
            case "3":
                self.approved_lines_of_credit()
            case "4":
                self.logout()

    #  'New application' menu GUI and navigation logic, including logic to open a new application.
    def new_application(self):
        new_row = pd.DataFrame({"Timestamp": [interface.get_pandas_timestamp()],
                                "Name": [self.get_name()],
                                "User ID": [self.get_user_id()],
                                "SSN": [self.enter_ssn()],
                                "Monthly Income": [self.enter_monthly_income()],
                                "Monthly Debts": [self.enter_monthly_debts()],
                                "Credit Score": -1,
                                "Approval Status": "Pending",
                                "Approved by ID": "System"})
        modified_df = self.get_applications_df()
        modified_df['Timestamp'] = pd.to_datetime(modified_df['Timestamp'])
        modified_df = pd.concat([modified_df, new_row], ignore_index=True)
        modified_df['Timestamp'] = pd.to_datetime(modified_df['Timestamp'])
        modified_df = modified_df.sort_values(by='Timestamp', ascending=False)
        modified_df = modified_df.reset_index(drop=True)
        self.set_applications_df(modified_df)
        interface.sleep_and_clear_screen(1)
        print("New Application for " + self.get_name())
        print("-------------------------------------------------------------------------------------------")
        input("Application finished. Press any key to return to the main menu.")
        self.main_menu()

    #  GUI and validation logic for entering new application SSN data.
    def enter_ssn(self):
        ssn = 0
        try:
            condition = False
            while condition is False:
                interface.sleep_and_clear_screen(1)
                print("New Application for " + self.get_name())
                print("-------------------------------------------------------------------------------------------")
                ssn = interface.get_input_with_prompt("Enter SSN (include hyphens): ")
                ssn = str(ssn)
                condition = interface.validate_ssn(ssn)
        except TypeError:
            print("Input is not valid. Please try again.")
            interface.sleep_and_clear_screen(1)
            self.enter_ssn()
        return ssn

    #  GUI and validation logic for entering new application monthly income data.
    def enter_monthly_income(self):
        monthly_income = 0
        try:
            condition = False
            while condition is False:
                interface.sleep_and_clear_screen(1)
                print("New Application for " + self.get_name())
                print("-------------------------------------------------------------------------------------------")
                monthly_income = interface.get_input_with_prompt("Enter monthly income (no negative numbers): ")
                monthly_income = int(monthly_income)
                condition = monthly_income > 0
        except TypeError:
            print("Input is not valid. Please try again.")
            interface.sleep_and_clear_screen(1)
            self.enter_monthly_income()
        return monthly_income

    #  GUI and validation logic for entering new application monthly debt data.
    def enter_monthly_debts(self):
        monthly_debts = 0
        try:
            condition = False
            while condition is False:
                interface.sleep_and_clear_screen(1)
                print("New Application for " + self.get_name())
                print("-------------------------------------------------------------------------------------------")
                monthly_debts = interface.get_input_with_prompt("Enter monthly debts (no negative numbers): ")
                monthly_debts = int(monthly_debts)
                condition = monthly_debts > 0
        except TypeError:
            print("Input is not valid. Please try again.")
            interface.sleep_and_clear_screen(1)
            self.enter_monthly_debts()
        return monthly_debts

    #  'Previous applications' menu GUI and navigation logic.
    def previous_applications(self):
        interface.sleep_and_clear_screen(1)
        print("Previously Completed Applications for " + self.get_name())
        print("-------------------------------------------------------------------------------------------")
        previous_applications = self.user_previous_applications()
        if previous_applications.empty is True:
            print("No previous applications have been completed.")
        else:
            print(previous_applications.to_string())
        print("-------------------------------------------------------------------------------------------")
        input("Press any key to return to the main menu.")
        self.main_menu()

    #  Filtering and visualizing session client's existing applications and sorting by timestamp.
    def user_previous_applications(self):
        filtered_df = self.get_applications_df()[self.get_applications_df()['User ID'] == self.get_user_id()]
        filtered_df = filtered_df.sort_values(by=['Timestamp'], ascending=False)
        filtered_df = filtered_df.reset_index(drop=True)
        return filtered_df

    #  GUI for visualizing session client's approvals (if existing).
    def approved_lines_of_credit(self):
        interface.sleep_and_clear_screen(1)
        print("Approved Lines of Credit for " + self.get_name())
        print("-------------------------------------------------------------------------------------------")
        previous_lines_of_credit = self.user_approved_lines_of_credit()
        if previous_lines_of_credit.empty is True:
            print("No lines of credit have been approved.")
        else:
            print(previous_lines_of_credit.to_string())
        print("-------------------------------------------------------------------------------------------")
        input("Press any key to return to the main menu.")
        self.main_menu()

    #  Filtering and visualizing session client's approvals and sorting by timestamp.
    def user_approved_lines_of_credit(self):
        filtered_df = self.get_approvals_df()[self.get_approvals_df()['User ID'] == self.get_user_id()]
        filtered_df = filtered_df.sort_values(by=['Timestamp'], ascending=False)
        filtered_df = filtered_df.reset_index(drop=True)
        return filtered_df

    #  Saves the current application DataFrame object to originating .csv file.
    def logout(self):
        interface.sleep_and_clear_screen(1)
        self.get_applications_df().to_csv(interface.APPLICATIONS_FILEPATH, index=False)
        print("Thank you for choosing us as your credit provider, " + self.get_name() + ". Have a great day!")
