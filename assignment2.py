from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

app = QApplication([])

window = uic.loadUi("a2.ui")

window.pageContainer.setCurrentIndex(0)


# Function to update the proceed button based on the checkbox state
def update_proceed_button():
    window.proceedButton1.setEnabled(window.checkBox.isChecked())


window.checkBox.stateChanged.connect(update_proceed_button)


# Function to change to the demographic page of the stacked widget

def proceed_to_demoPage():
    if window.checkBox.isChecked():
        window.pageContainer.setCurrentIndex(1)


window.proceedButton1.clicked.connect(proceed_to_demoPage)

window.proceedButton1.setEnabled(False)

# setting up codes for the demographic page
window.ageError.hide()
window.genderError.hide()
window.eduError.hide()


# set a function when any radio button is checked
def is_radio_button_checked(button_group):
    for button in button_group:
        if button.isChecked():
            return True
    return False


def valid_demo():
    # Valid age
    age_valid = window.ageInput.text().isdigit() and 0 < int(window.ageInput.text()) < 100
    if not age_valid:
        window.ageError.show()
    else:
        window.ageError.hide()
    # Valid Gender
    gender_buttons = [window.rdbM, window.rdbF, window.rdbO, window.rdbP]
    gender_valid = is_radio_button_checked(gender_buttons)
    if not gender_valid:
        window.genderError.show()
    else:
        window.genderError.hide()
    # Valid Education
    education_buttons = [window.rdbBA, window.rdbMA, window.rdbPhD, window.rdbHS]
    edu_valid = is_radio_button_checked(education_buttons)
    if not edu_valid:
        window.eduError.show()
    else:
        window.eduError.hide()

    return age_valid and gender_valid and edu_valid


# Change to the experiment instruction page if demographics are valid
def proceed_to_ins_page():
    if valid_demo():
        window.pageContainer.setCurrentIndex(window.pageContainer.currentIndex() + 1)


window.proceedButton1_2.clicked.connect(proceed_to_ins_page)


# Change to the experiment selection page after reading the instruction
def proceed_to_trial1():
    index = window.pageContainer.indexOf(window.trial1Page)
    window.pageContainer.setCurrentIndex(index)


# Connect the proceed button on the instruction page to the function
window.proceedButton1_3.clicked.connect(proceed_to_trial1)

from random import randint




import os

# Create a file to keep track of the number of participants in each condition.
def get_least_populated_condition():
    filename = "condition_counts.csv"
    counts = [0, 0, 0]

    # Check if the file exists before attempting to read it
    if os.path.exists(filename):
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()

        if len(lines) == 3:
            for i in range(3):
                counts[i] = int(lines[i].split(',')[0])

    # Determine condition with the least participants
    min_count = min(counts)
    condition_index = counts.index(min_count)

    # Update the count for this condition
    counts[condition_index] += 1

    # Write updated counts back to file
    file = open(filename, 'w')
    for count in counts:
        file.write(str(count) + '\n')
    file.close()

    return condition_index


# Add the radio button check function
def check_selection_and_update_confirm_button():
    # Enable the confirm button only if one of the radio buttons is selected
    if window.rdb_a.isChecked() or window.rdb_b.isChecked():
        window.confirmBtn1.setEnabled(True)
    else:
        window.confirmBtn1.setEnabled(False)

# Connect the radio buttons' stateChanged signal to the new function
window.rdb_a.toggled.connect(check_selection_and_update_confirm_button)
window.rdb_b.toggled.connect(check_selection_and_update_confirm_button)

# Initially disable the confirm button until a choice is made
window.confirmBtn1.setEnabled(False)



# Function to generate a setup and confirmation function with enclosed urn content state
def create_trial_setup():

    # hand code the conditions and use the function to get the least populated condition
    condition_index = get_least_populated_condition()
    conditions = [(2, (1, 1), (2, 0)), (10, (5, 5), (7, 3)), (100, (50, 50), (43, 57))]

    condition_index = randint(0, len(conditions) - 1)
    condition = conditions[condition_index]

    # Randomly decide which urn gets the known distribution
    if randint(0, 1) == 0:
        urn_a_content = condition[1]
        urn_b_content = condition[2]
    else:
        urn_a_content = condition[2]
        urn_b_content = condition[1]

    def setup_trial():
        # Determine the total number of marbles for the condition
        total_marbles = sum(condition[1])

        # Check the radio buttons state to set the confirm button state
        check_selection_and_update_confirm_button()

        # Set label texts based on the condition
        if urn_a_content == condition[1]:
            window.knownLabel.setText(f"Total: {total_marbles} marbles (50% red & 50% blue)")
            window.unknownLabel.setText(f"Total: {total_marbles} marbles (Unknown proportion)")
        else:
            window.knownLabel.setText(f"Total: {total_marbles} marbles (Unknown proportion)")
            window.unknownLabel.setText(f"Total: {total_marbles} marbles (50% red & 50% blue)")

        # Create a QFont object for setting the font size
        label_font = QFont()
        label_font.setPointSize(8)

        # Apply the font to the labels
        window.knownLabel.setFont(label_font)
        window.unknownLabel.setFont(label_font)

        window.blueLabel1.hide()
        window.redLabel1.hide()
        window.proceedButton1_4.hide()



    # only show the results after pressing the confirm buttton
    def confirm_selection():
        global result

        total_marbles_a = sum(urn_a_content)
        total_marbles_b = sum(urn_b_content)

        if window.rdb_a.isChecked():
            random_number = randint(1, total_marbles_a)
            if random_number <= urn_a_content[0]:
                result = 'red'
            else:
                result = 'blue'
        elif window.rdb_b.isChecked():
            random_number = randint(1, total_marbles_b)
            if random_number <= urn_b_content[0]:
                result = 'red'
            else:
                result = 'blue'

        if result == 'red':
            window.redLabel1.show()
            window.blueLabel1.hide()
        else:
            window.blueLabel1.show()
            window.redLabel1.hide()

        window.proceedButton1_4.show()



        # Save the participant's data to a csv file
        def save_participant_data():

            filename = "experiment_results.csv"
            # Gather data
            age = window.ageInput.text()
            gender = get_selected_button_text([window.rdbM, window.rdbF, window.rdbO, window.rdbP])
            education_level = get_selected_button_text([window.rdbBA, window.rdbMA, window.rdbPhD, window.rdbHS])
            condition_number = condition_index + 1

            if urn_a_content == condition[2]:
                urn_position = 1
            else:
                urn_position = 0

            if window.rdb_b.isChecked():
                selected_urn = 1
            else:
                selected_urn = 0

            data_line = f"{age},{gender},{education_level},{condition_number},{urn_position},{selected_urn},{result}\n"

            # Open the file and append the data
            csvfile = open(filename, 'a')
            csvfile.write(data_line)
            csvfile.close()


        # Helper function to get the selected button's text in a button group
        def get_selected_button_text(button_group):
            for button in button_group:
                if button.isChecked():
                    return button.text()
            return ""

        # Function to move to the debrief page
        def proceed_to_debrief():
            index = window.pageContainer.indexOf(window.debriefPage)
            window.pageContainer.setCurrentIndex(index)

        window.proceedButton1_4.clicked.connect(proceed_to_debrief)

        # Function to end the study and exit the application
        def exit_application():
            save_participant_data()
            app.quit()

        # Connect the exit function to the exit button
        window.exitBtn.clicked.connect(exit_application)

    return setup_trial, confirm_selection


setup_trial, confirm_selection = create_trial_setup()

window.confirmBtn1.clicked.connect(confirm_selection)

setup_trial()

window.show()
app.exec()
