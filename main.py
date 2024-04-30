# Name: Valary Musibega
# Project: Credit Application Program
# Course: CS 3321
# Description: This class is the program's main driver.

import administrator    # Imports the administrator class for session administrator creation.
import businessanalyst  # Imports the administrator class for session administrator creation.
import client           # Imports the administrator class for session administrator creation.
import interface        # Imports the administrator class for session administrator creation.

if __name__ == '__main__':

    #  Initialize all existing files as DataFrame objects. Otherwise, create new DataFrame objects with existing column
    #  list parameters and create new .csv files based on these objects.
    users_df = interface.open_or_create_csv(interface.AUTHORIZED_USERS_FILEPATH, interface.AUTHORIZED_USERS_COLUMNS)
    credit_scores_df = interface.open_or_create_csv(interface.CREDIT_SCORES_FILEPATH, interface.CREDIT_SCORES_COLUMNS)
    thresholds_df = interface.open_or_create_csv(interface.THRESHOLDS_FILEPATH, interface.THRESHOLDS_COLUMNS)
    applications_df = interface.open_or_create_csv(interface.APPLICATIONS_FILEPATH, interface.APPLICATIONS_COLUMNS)
    approvals_df = interface.open_or_create_csv(interface.APPROVALS_FILEPATH, interface.APPROVALS_COLUMNS)
    name, user_id = interface.login_prompt(users_df)
    session_char = user_id[0]

    #  Depending on session client data, respective user class is created with respective DataFrame objects.
    match session_char:
        case 'A':
            interface.sleep_and_clear_screen(1)
            session_admin = administrator.Administrator(name,
                                                        user_id,
                                                        applications_df,
                                                        approvals_df,
                                                        credit_scores_df,
                                                        thresholds_df,
                                                        users_df)
            session_admin.application_preprocessing()
            session_admin.main_menu()
        case 'B':
            interface.sleep_and_clear_screen(1)
            session_employee = businessanalyst.BusinessAnalyst(name,
                                                               user_id,
                                                               applications_df,
                                                               approvals_df,
                                                               credit_scores_df,
                                                               thresholds_df)
            session_employee.application_preprocessing()
            session_employee.main_menu()
        case 'C':
            interface.sleep_and_clear_screen(1)
            session_client = client.Client(name,
                                           user_id,
                                           applications_df,
                                           approvals_df)
            session_client.main_menu()
