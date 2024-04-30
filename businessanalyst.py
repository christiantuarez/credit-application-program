# Name: Christian Tuarez
# Project: Credit Application Program
# Course: CS 3321
# Description: This class implements all the tasks assigned to the business analyst user, as well as auxiliary functions
# necessary for the correct functioning of the class' main functions.

import pandas as pd  # Importing pandas DataFrame library for data processing
import interface  # Importing for access to auxiliary functions.


# Business analyst class constructor and parameter definitions.
class BusinessAnalyst:
    def __init__(self, name, user_id, applications_df, approvals_df, credit_scores_df, thresholds_df):
        self.__name = name
        self.__user_id = user_id
        self.__applications_df = applications_df
        self.__approvals_df = approvals_df
        self.__credit_scores_df = credit_scores_df
        self.__thresholds_df = thresholds_df

    def get_name(self):
        return self.__name

    def get_user_id(self):
        return self.__user_id

    def get_applications_df(self):
        return self.__applications_df

    def get_approvals_df(self):
        return self.__approvals_df

    def get_credit_scores_df(self):
        return self.__credit_scores_df

    def get_thresholds_df(self):
        return self.__thresholds_df

    def set_applications_df(self, applications_df):
        self.__applications_df = applications_df

    def set_approvals_df(self, approvals_df):
        self.__approvals_df = approvals_df

    #  When a session is initiated by a business manager, the program automatically rejects selected pending
    #  applications based on thresholds set by the administrator.
    def application_preprocessing(self):

        # Populating SSN numbers on existing applications.
        applications_df = self.sort_applications_df()
        credit_scores_df = self.get_credit_scores_df()
        merged_df = applications_df.merge(credit_scores_df, how='left', on='SSN', indicator=True)
        applications = merged_df.drop(columns=['Credit Score_x', '_merge'])
        applications = applications.rename(columns={"Credit Score_y": "Credit Score"})
        applications = applications[['Timestamp',
                                     'Name',
                                     'User ID',
                                     'SSN',
                                     'Monthly Income',
                                     'Monthly Debts',
                                     'Credit Score',
                                     'Approval Status',
                                     'Approved by ID']]

        # Separating pending applications from already processed applications.
        pending_applications = applications[applications['Approval Status'] == "Pending"]
        processed_applications = applications[applications['Approval Status'] != "Pending"]

        #  Rejecting applications not meeting minimum credit score requirements.
        rejected_by_credit_score = pending_applications['Credit Score'] < self.get_thresholds_df()['CSART'].values[0]
        pending_applications.loc[rejected_by_credit_score, 'Approval Status'] = 'Rejected'
        pending_applications.loc[rejected_by_credit_score, 'Approved by ID'] = self.get_user_id()

        #  Calculating debt to income ratio and rejecting applications surpassing debt to ratio threshold ratio set by
        # administrator.
        dtir_col = pd.DataFrame([], columns=['Debt to Income Ratio'])
        dtir_col['Debt to Income Ratio'] = pending_applications['Monthly Debts']/pending_applications['Monthly Income']
        pending_applications = pd.concat([pending_applications, dtir_col], axis=1)
        rejected_by_dtir = pending_applications['Debt to Income Ratio'] > self.get_thresholds_df()['DtIRT'].values[0]
        pending_applications.loc[rejected_by_dtir, 'Approval Status'] = 'Rejected'
        pending_applications.loc[rejected_by_dtir, 'Approved by ID'] = self.get_user_id()
        pending_applications = pending_applications.drop(columns=['Debt to Income Ratio'])

        # Sorting applications by timestamp.
        applications = pd.concat([processed_applications, pending_applications], ignore_index=True)
        applications['Timestamp'] = pd.to_datetime(applications['Timestamp'])
        applications = applications.sort_values(by='Timestamp', ascending=False)
        applications = applications.reset_index(drop=True)

        # Setting new application DataFrame object.
        self.set_applications_df(applications)

    #  Main menu GUI and navigation logic. Overloaded from BusinessAnalyst class.
    def main_menu(self):
        option = 0
        try:
            condition = True
            while condition is True:
                interface.sleep_and_clear_screen(1)
                print("Main Menu (Session ID " + self.get_user_id() + ")")
                print("-------------------------------------------------------------------------------------------")
                print("1. View Pending Applications")
                print("2. View Line of Credit Approvals")
                print("3. Logout")
                print("-------------------------------------------------------------------------------------------")
                option = interface.get_input_with_prompt("Select your option: ")
                condition = int(option) < 1 or int(option) > 3
        except ValueError:
            print("Input is not valid. Please try again.")
            interface.sleep_and_clear_screen(1)
            self.main_menu()

        match option:
            case "1":
                self.view_applications()
            case "2":
                self.view_approvals()
            case "3":
                self.logout()

    #  'View applications' menu GUI and navigation logic.
    def view_applications(self):
        option = 0
        sorted_applications_df = self.sort_applications_df()
        sorted_applications = self.sort_applications_df()
        pending_applications = sorted_applications[sorted_applications_df['Approval Status'] == 'Pending']
        df_len = len(pending_applications)
        try:
            condition = True
            while condition:
                interface.sleep_and_clear_screen(1)
                print("Pending Applications (Session ID " + self.get_user_id() + ")")
                print("-------------------------------------------------------------------------------------------")
                if pending_applications.empty is True:
                    print("No pending applications found.")
                    print("-------------------------------------------------------------------------------------------")
                    input("Press any key to return to the users menu.")
                    self.main_menu()
                else:
                    print(pending_applications.to_string())
                    print("-------------------------------------------------------------------------------------------")
                    option = interface.get_input_with_prompt("Select the index for the desired application: ")
                    option = int(option)  # MUST ALWAYS DO, OTHERWISE DATAFRAME.DROP() DOES NOT KNOW IT IS AN INT
                    condition = option < 0 or option > (df_len - 1)
        except ValueError:
            print("Input is not valid. Please try again.")
            interface.sleep_and_clear_screen(1)
            self.view_applications()

        selected_application = pending_applications.copy(pending_applications.index[option])
        self.evaluate_application(selected_application)

    #  'Evaluate application' menu GUI and navigation logic, including logic for approving rejecting new lines of
    #  credit.
    def evaluate_application(self, selected_application):
        choice = ""
        try:
            condition = False
            while condition is False:
                interface.sleep_and_clear_screen(1)
                print("Pending Applications (Session ID " + self.get_user_id() + ")")
                print("-------------------------------------------------------------------------------------------")
                print(selected_application.to_string())
                print("-------------------------------------------------------------------------------------------")
                choice = interface.get_input_with_prompt("Approve or decline line of credit (Y or N)?: ")
                choice = str(choice)
                condition = choice == "Y" or choice == "N"
        except ValueError:
            print("Input is not valid. Please try again.")
            interface.sleep_and_clear_screen(1)
            self.evaluate_application(selected_application)

        #  Approval/rejection logic.
        match choice:
            case "Y":
                selected_application['Approval Status'] = "Approved"
                selected_application['Approved by ID'] = self.get_user_id()
            case "N":
                selected_application['Approval Status'] = "Rejected"
                selected_application['Approved by ID'] = self.get_user_id()
        if choice == 'Y':
            approval_limit = self.approval_limit(selected_application)
            old_df = self.get_applications_df()
            old_df = old_df[old_df['SSN'] != selected_application['SSN'].values[0]]
            old_df = pd.concat([old_df, selected_application], ignore_index=True)
            old_df['Timestamp'] = pd.to_datetime(old_df['Timestamp'])
            applications = old_df.sort_values(by='Timestamp', ascending=False)
            applications = applications.reset_index(drop=True)
            self.set_applications_df(applications)

            #  Create new approval and add it to new approvals DataFrame object.
            new_row = pd.DataFrame({"Timestamp": [interface.get_pandas_timestamp()],
                                    "User ID": [selected_application['User ID'].values[0]],
                                    "Credit Line Limit": approval_limit})
            modified_df = self.get_approvals_df()
            modified_df['Timestamp'] = pd.to_datetime(modified_df['Timestamp'])
            if modified_df.empty:
                modified_df = new_row
            else:
                modified_df = pd.concat([modified_df, new_row], ignore_index=True)

            #  Sorting by timestamp.
            modified_df['Timestamp'] = pd.to_datetime(modified_df['Timestamp'])
            modified_df = modified_df.sort_values(by='Timestamp', ascending=False)
            modified_df = modified_df.reset_index(drop=True)
            self.set_approvals_df(modified_df)

        self.main_menu()

    #  Calculates line of credit limit for newly approved applications.
    def approval_limit(self, selected_application):
        approval_limit = 0
        thresholds = self.get_thresholds_df()
        dtir_limit = thresholds['PFRLfC'].values[0]
        income = selected_application['Monthly Income'].values[0]
        debts = selected_application['Monthly Debts'].values[0]
        credit_score = selected_application['Credit Score'].values[0]
        dtir = income - debts
        if credit_score > 350:
            percentage = dtir_limit * 0.25
            approval_limit = dtir * percentage
        elif credit_score > 475:
            percentage = dtir_limit * 0.50
            approval_limit = dtir * percentage
        elif credit_score > 600:
            percentage = dtir_limit * 0.75
            approval_limit = dtir * percentage
        elif credit_score > 750:
            approval_limit = dtir * dtir_limit

        mcl = thresholds['MCL'].values[0]
        if mcl > approval_limit:
            approval_limit = mcl

        return approval_limit

    #  Sorting existing applications DataFrame object.
    def sort_applications_df(self):
        sorted_applications_df = self.get_applications_df().sort_values(by=['Timestamp'], ascending=False)
        sorted_applications_df = sorted_applications_df.reset_index(drop=True)

        return sorted_applications_df

    #  'View approvals ' GUI and navigation logic.
    def view_approvals(self):
        interface.sleep_and_clear_screen(1)
        print("Approvals (Session ID " + self.get_user_id() + ")")
        print("-------------------------------------------------------------------------------------------")
        approvals_list_df = self.sort_approvals_df()
        if approvals_list_df.empty is True:
            print("No approvals found.")
        else:
            print(approvals_list_df.to_string())
        print("-------------------------------------------------------------------------------------------")
        input("Press any key to return to the users menu.")
        self.main_menu()

    #  Sorting approvals by timestamp.
    def sort_approvals_df(self):
        sorted_approvals_df = self.get_approvals_df().sort_values(by=['User ID'])
        sorted_approvals_df = sorted_approvals_df.reset_index(drop=True)

        return sorted_approvals_df

    #  Saves the current application and approvals DataFrame objects to originating .csv files.
    def logout(self):
        interface.sleep_and_clear_screen(1)
        self.get_applications_df().to_csv(interface.APPLICATIONS_FILEPATH, index=False)
        self.get_approvals_df().to_csv(interface.APPROVALS_FILEPATH, index=False)
        print("Session finished for ID " + self.get_user_id() + ".")
