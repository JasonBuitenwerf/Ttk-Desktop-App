from tkinter import ttk
import tkinter as tk

from model import TravelRecord


class NewRecordForm(ttk.Frame):
    """
    Class for create and update forms
    """

    def __init__(self, parent, controller, travel_record=None):
        """
        Initializes a form, fields are blank by default
        :param parent: the frames parent
        :param travel_record: Optional, include to create an update form
        """
        super().__init__(parent)

        self.controller = controller
        self.feedback_message = None

        # Determine whether the entry fields will be empty or pre-filled
        if travel_record is None:
            self.ref_num_var = tk.StringVar()
            self.title_var = tk.StringVar()
            self.purpose_var = tk.StringVar()
            self.start_var = tk.StringVar()
            self.end_var = tk.StringVar()
            self.airfare_var = tk.StringVar()
            self.transport_var = tk.StringVar()
            self.lodging_var = tk.StringVar()
            self.meals_var = tk.StringVar()
            self.expenses_var = tk.StringVar()
        else:
            self.ref_num_var = tk.StringVar(value=travel_record.ref_number)
            self.title_var = tk.StringVar(value=travel_record.title_en)
            self.purpose_var = tk.StringVar(value=travel_record.purpose_en)
            self.start_var = tk.StringVar(value=travel_record.start_date)
            self.end_var = tk.StringVar(value=travel_record.end_date)
            self.airfare_var = tk.StringVar(value=travel_record.airfare)
            self.transport_var = tk.StringVar(value=travel_record.other_transport)
            self.lodging_var = tk.StringVar(value=travel_record.lodging)
            self.meals_var = tk.StringVar(value=travel_record.meals)
            self.expenses_var = tk.StringVar(value=travel_record.other_expenses)

        self.travel_record = travel_record

        # ref_number
        ref_num_label = ttk.Label(self, text='ref_number')
        ref_num_label.grid(row=0, column=0, sticky='W')
        ref_num_entry = ttk.Entry(self, textvariable=self.ref_num_var, width=100)
        ref_num_entry.grid(row=0, column=1, sticky='E')

        # title_en
        title_label = ttk.Label(self, text='title_en')
        title_label.grid(row=1, column=0, sticky='W')
        title_entry = ttk.Entry(self, textvariable=self.title_var, width=100)
        title_entry.grid(row=1, column=1, sticky='E')

        # purpose_en
        purpose_label = ttk.Label(self, text='purpose_en')
        purpose_label.grid(row=2, column=0, sticky='W')
        purpose_entry = ttk.Entry(self, textvariable=self.purpose_var, width=100)
        purpose_entry.grid(row=2, column=1, sticky='E')

        # start_date
        start_label = ttk.Label(self, text='start_date')
        start_label.grid(row=3, column=0, sticky='W')
        start_entry = ttk.Entry(self, textvariable=self.start_var, width=100)
        start_entry.grid(row=3, column=1, sticky='E')

        # end_date
        end_label = ttk.Label(self, text='end_date')
        end_label.grid(row=4, column=0, sticky='W')
        end_entry = ttk.Entry(self, textvariable=self.end_var, width=100)
        end_entry.grid(row=4, column=1, sticky='E')

        # airfare
        airfare_label = ttk.Label(self, text='airfare')
        airfare_label.grid(row=5, column=0, sticky='W')
        airfare_entry = ttk.Entry(self, textvariable=self.airfare_var, width=100)
        airfare_entry.grid(row=5, column=1, sticky='E')

        # other_transport
        transport_label = ttk.Label(self, text='other_transport')
        transport_label.grid(row=6, column=0, sticky='W')
        transport_entry = ttk.Entry(self, textvariable=self.transport_var, width=100)
        transport_entry.grid(row=6, column=1, sticky='E')

        # lodging
        lodging_label = ttk.Label(self, text='lodging')
        lodging_label.grid(row=7, column=0, sticky='W')
        lodging_entry = ttk.Entry(self, textvariable=self.lodging_var, width=100)
        lodging_entry.grid(row=7, column=1, sticky='E')

        # meals
        meals_label = ttk.Label(self, text='meals')
        meals_label.grid(row=8, column=0, sticky='W')
        meals_entry = ttk.Entry(self, textvariable=self.meals_var, width=100)
        meals_entry.grid(row=8, column=1, sticky='E')

        # other_expenses
        expenses_label = ttk.Label(self, text='other_expenses')
        expenses_label.grid(row=9, column=0, sticky='W')
        expenses_entry = ttk.Entry(self, textvariable=self.expenses_var, width=100)
        expenses_entry.grid(row=9, column=1, sticky='E')

        # submit button
        submit_button = ttk.Button(self, text='Submit', command=self.submit_button_clicked, width=100)
        submit_button.grid(row=10, column=1)

    def submit_button_clicked(self):
        """
        Creates a travel record and passes it to the controller, if this form was created with a travel_record, this new
        record will replace it in the data structure
        """
        try:
            self.controller.create_new(
                self,
                TravelRecord(
                    self.ref_num_var.get(), self.title_var.get(), self.purpose_var.get(), self.start_var.get(),
                    self.end_var.get(), self.airfare_var.get(), self.transport_var.get(), self.lodging_var.get(),
                    self.meals_var.get(), self.expenses_var.get(),
                    float(self.airfare_var.get()) + float(self.transport_var.get()) + float(self.lodging_var.get())
                    + float(self.meals_var.get()) + float(self.expenses_var.get())
                ),
                self.travel_record  # Will be None when creating a new record
            )
        except ValueError:
            self.show_failure_message("The last 5 fields must contain numbers")

    def show_success_message(self, message):
        """
        Shows a success message
        :param message: the message to be shown
        """
        self.feedback_message = ttk.Label(self, text=message, foreground='green')
        self.feedback_message.grid(row=11, columnspan=11)

    def show_failure_message(self, message):
        """
        Shows a failure message
        :param message: the message to be shown
        """
        self.feedback_message = ttk.Label(self, text=message, foreground='red')
        self.feedback_message.grid(row=11, columnspan=11)