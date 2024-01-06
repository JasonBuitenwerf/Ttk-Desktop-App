from tkinter import ttk


class RecordView(ttk.Frame):
    """
    The view object for the TravelRecords
    """

    def __init__(self, parent, travel_record, controller):
        """
        Initializes the RecordView
        :param parent: this views parent
        :param travel_record: the TravelRecord this view represents
        :param controller: the controller for the main window
        """
        super().__init__(parent)

        self.parent = parent
        self.travel_record = travel_record
        self.controller = controller

        ref_num_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.ref_number,
            width=16
        )
        ref_num_label.pack(side="left", fill="both")

        title_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.title_en,
            width=34,
            wraplength=200
        )
        title_label.pack(side="left", fill="both")

        purpose_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.purpose_en,
            width=34,
            wraplength=200
        )
        purpose_label.pack(side="left", fill="both")

        start_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.start_date,
            width=14)
        start_label.pack(side="left", fill="both")

        end_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.end_date,
            width=14
        )
        end_label.pack(side="left", fill="both")  # .grid(row=0, column=5)

        airfare_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.airfare,
            width=14
        )
        airfare_label.pack(side="left", fill="both")  # .grid(row=0, column=6)

        transport_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.other_transport,
            width=14
        )
        transport_label.pack(side="left", fill="both")  # .grid(row=0, column=7)

        lodging_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.lodging,
            width=14
        )
        lodging_label.pack(side="left", fill="both")  # .grid(row=0, column=8)

        meals_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.meals,
            width=14
        )
        meals_label.pack(side="left", fill="both")

        expenses_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.other_expenses,
            width=14
        )
        expenses_label.pack(side="left", fill="both")

        total_label = ttk.Label(
            master=self,
            anchor="nw",
            borderwidth=1,
            relief="solid",
            text=travel_record.total,
            width=14
        )
        total_label.pack(side="left", fill="both")

        delete_button = ttk.Button(
            master=self,
            command=self.delete_button_clicked,
            text='Delete',
            width=8
        )
        delete_button.pack(side="left", fill="both")

        edit_button = ttk.Button(
            master=self,
            command=self.edit_button_clicked,
            text='Edit',
            width=8
        )
        edit_button.pack(side="left", fill="both")

    def delete_button_clicked(self):
        """
        removes the associated record from the database and destroys this RecordView
        """
        self.controller.delete_record(self.travel_record)
        self.destroy()

    def edit_button_clicked(self):
        """
        Creates a form and asks the window to display it
        """
        self.controller.display_form(self.travel_record)