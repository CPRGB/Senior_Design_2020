import tkinter as tk
from tkinter import ttk

import Connection as conn
import HelperMethods as hm


class LogPatient(tk.Frame):
    # values for all entries
    bmi = 0.0
    age_value = 0
    weight_value = 0
    height_value_ft = 0
    height_value_in = 0
    skin_color_type = ""
    ethnicity_option_selected = ""
    gender_option_selected = ""
    patient_id = 1
    id_list = conn.multi_select('subject_id', conn.subject)     # Initialize list with all subjects' ids

    # Check for empty subject table and if not empty get the patient's id to display
    if id_list != []:
        patient_id = id_list[-1][0] + 1

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Patient's Info", font=hm.LARGE_FONT)
        label.grid(row=0, column=1, padx=0, pady=10)

        id_label = ttk.Label(self, text="Patient ID:", font=hm.SMALL_FONT)
        id_label.grid(row=2, column=0, padx=0, pady=10)
        id_val = ttk.Label(self, text=self.patient_id, font=hm.SMALL_FONT)
        id_val.grid(row=2, column=1)

        age_label = ttk.Label(self, text="Age:", font=hm.SMALL_FONT)
        age_label.grid(row=4, column=0, padx=10, pady=10)
        age_entry = ttk.Entry(self, )
        age_entry.grid(row=4, column=1)

        gender_label = ttk.Label(self, text="Sex:", font=hm.SMALL_FONT)
        gender_label.grid(row=6, column=0, padx=10, pady=10)
        self.gender_option_selected = tk.StringVar()
        self.gender_option_selected.set(hm.Gender[0])
        gender_options = ttk.OptionMenu(self, self.gender_option_selected, *hm.Gender)
        gender_options.grid(row=6, column=1)

        weight_label = ttk.Label(self, text="Weight:", font=hm.SMALL_FONT)
        weight_label.grid(row=8, column=0, padx=10, pady=10)
        weight_entry = ttk.Entry(self)
        weight_entry.grid(row=8, column=1)
        weight_label_unit = ttk.Label(self, text="Lb", font=hm.SMALL_FONT)
        weight_label_unit.grid(row=8, column=2, padx=10, pady=10)

        height_label = ttk.Label(self, text="Height:", font=hm.SMALL_FONT)
        height_label.grid(row=10, column=0, padx=10, pady=10)
        height_entry_ft = ttk.Entry(self)
        height_entry_ft.grid(row=10, column=1, padx=2)
        weight_label_unit = ttk.Label(self, text="Ft", font=hm.SMALL_FONT)
        weight_label_unit.grid(row=10, column=2, padx=10, pady=10)

        height_entry_in = ttk.Entry(self)
        height_entry_in.grid(row=10, column=3)
        weight_label_unit = ttk.Label(self, text="In", font=hm.SMALL_FONT)
        weight_label_unit.grid(row=10, column=4, padx=10, pady=10)

        ethnicity_label = ttk.Label(self, text="Ethnicity:", font=hm.SMALL_FONT)
        ethnicity_label.grid(row=12, column=0, padx=10, pady=10)
        self.ethnicity_option_selected = tk.StringVar()
        self.ethnicity_option_selected.set(hm.Ethnicity[0])
        ethnicity_options = ttk.OptionMenu(self, self.ethnicity_option_selected, *hm.Ethnicity)
        ethnicity_options.grid(row=12, column=1)

        skin_color_label = ttk.Label(self, text="Fitzpatrick Scale:", font=hm.SMALL_FONT)
        skin_color_label.grid(row=14, column=0, padx=10, pady=10)
        self.skin_color_type = tk.StringVar()
        self.skin_color_type.set(hm.SkinColor[0])
        skin_color_entry = ttk.OptionMenu(self, self.skin_color_type, *hm.SkinColor)
        skin_color_entry.grid(row=14, column=1)

        save_button = ttk.Button(self, text="Save and Continue", command=lambda: save_and_go_to_recording_page())
        save_button.grid(row=26, column=1, padx=10, pady=30)

        def update_bmi(height_ft, height_in, weight, CONSTANT = 703.0):
            """ Method to calculate BMI """
            height = float((height_ft * 12.0) + height_in)
            if weight > 0.0 and height > 0.0:
                bmi = (weight / (height ** 2)) * CONSTANT
                return round(bmi, 1)
            else:
                return 0.0

        def compose_height(ft, inch):
            """ Composed the exact height by getting feet and inches. Merges them into a float number. Fixes errors
             such as 5.1 and 5.10 """
            decimal = float(inch)
            num = float(ft)
            if inch > 9:
                decimal = (decimal / 100)
                height = format(num + decimal, '.2f')
                return height
            else:
                decimal = float(self.height_value_in) / 10
                height = num + decimal
                return height

        def save_and_go_to_recording_page():
            """ Gets data input in the fields and saves it to subject table in database. This happens only
            if all fields pass validation in get_value() method """
            if get_values():
                # Call method to get bmi given height and weight
                self.bmi = update_bmi(self.height_value_ft, self.height_value_in, float(self.weight_value))
                # Call method to get accurate height value
                height_value = compose_height(self.height_value_ft, self.height_value_in)
                # Save patient to database in azure
                conn.insert(conn.subject, hm.current_researcher, self.age_value, self.weight_value,
                            height_value, self.bmi, self.ethnicity_option_selected.get(),
                            self.skin_color_type.get(), self.gender_option_selected.get())
                # move to recording page
                controller.show_dataRecording_frame()

            return

        # get_values stores all values from fields into variables and returns any errors found when trying to
        # convert each field into its respective type
        def get_values():
            """ Validates all fields in LogPatient frame for correct input """
            if hm.check_fields_inputs(
                    ageEntry=age_entry,
                    heightEntryFt=height_entry_ft,
                    heightEntryIn=height_entry_in,
                    weightEntry=weight_entry,
                    ethnicityOption=self.ethnicity_option_selected.get(),
                    genderOption=self.gender_option_selected.get(),
                    skinColorOption=self.skin_color_type.get()):

                self.age_value = int(age_entry.get())
                self.height_value_ft = int(height_entry_ft.get())
                self.height_value_in = int(height_entry_in.get())
                self.weight_value = int(weight_entry.get())
                return True
            else:
                return False
