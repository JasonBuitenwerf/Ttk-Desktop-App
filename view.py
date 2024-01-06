# Program Written by Jason Buitenwerf

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from model import TravelRecord
from record_view import RecordView


class Window(ttk.Frame):
    """
    The main window of the application, the buttons save, load, select, and create new buttons are defined here,
    Record Views and forms appear beneath them
    """

    def __init__(self, parent):
        """
        Initializes Window class
        :param parent: This frames parent
        """
        super().__init__(parent)

        self.menu = ttk.Frame(self)
        self.content = ttk.Frame(self, width=1000, height=10000)

        # reload button
        reload_button = ttk.Button(self.menu, text='Load data from file', command=self.reload_button_clicked, width=30)
        reload_button.grid(row=0, column=0, padx=20, pady=20)

        # save button
        save_button = ttk.Button(self.menu, text='Save to file', command=self.save_button_clicked, width=30)
        save_button.grid(row=0, column=2, padx=20, pady=20)

        # display button
        display_button = ttk.Button(self.menu, text='Display records/Refresh', command=self.display_button_clicked,
                                    width=30)
        display_button.grid(row=0, column=3, padx=20)

        # new record button
        create_button = ttk.Button(self.menu, text='Create new record', command=self.create_button_clicked, width=30)
        create_button.grid(row=0, column=5, padx=20)

        # create pie chart button
        chart_button = ttk.Button(self.menu, text='Generate Pie Chart', command=self.chart_button_clicked, width=30)
        chart_button.grid(row=0, column=6, padx=20)

        label = ttk.Label(self.menu, text="Programmed by Jason Buitenwerf")
        label.grid(row=0, column=7, padx=20)

        self.menu.pack(side="top")
        self.content.pack(side="top", fill="both")
        self.content.pack_propagate(False)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller to be used by the window
        :param controller: controller to be set
        """
        self.controller = controller

    def reload_button_clicked(self):
        """
        The User is prompted to select a file from the file system to be loaded into the app, the filepath is then
        passed to the controller which will handle reading the file
        """
        filepath = filedialog.askopenfilename()
        if self.controller:
            self.controller.reload(filepath)

    def save_button_clicked(self):
        """
        The User is prompted to select a file from the file system to be saved to, the filepath is then
        passed to the controller which will handle writing to the file
        """
        filepath = filedialog.askopenfilename()
        if self.controller:
            self.controller.save(filepath)

    def display_button_clicked(self):
        """
        The first step of the display is delegated to the controller
        :return:
        """
        self.controller.display()

    def create_button_clicked(self):
        """
        Destroys any existing form before calling display_form to create a new one, this should only be called when
        the create button is clicked
        """
        self.controller.display_form()

    def chart_button_clicked(self):
        """
        Destroys any existing form before calling display_form to create a new one, this should only be called when
        the create button is clicked
        """
        self.controller.display_graph_options()

    def display(self, records):
        """
        Displays records from the database in a scrollable window
        :param records: A list of RecordViews displaying the data and buttons for updating and deleting records
        """
        # create canvas
        canvas = tk.Canvas(self.content)
        canvas.pack(side="left", fill="both", expand=True)

        # create scrollbar
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", ipadx=10)

        # configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # frame 2
        frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=frame, anchor="nw")

        column_headers = RecordView(
            frame,
            TravelRecord(
                'ref_number',
                'title_en',
                'purpose_en',
                'start_date',
                'end_date',
                'airfare',
                'other_transport',
                'lodging',
                'meals',
                'other_expenses',
                'total'
            ),
            self.controller
        )
        record_views = [column_headers]
        for travel_record in records:
            record_views.append(RecordView(frame, travel_record, self.controller))

        # place the column headers and RecordViews on the grid
        i = 0
        for record_view in record_views:
            record_view.grid(row=i, column=0, columnspan=14)
            i += 1

    def display_fnf_error(self):
        """
        Displays an error message
        """
        # Cleanup
        if len(self.displayed_records) > 0:
            for record_view in self.displayed_records:
                record_view.destroy()
        if self.content:
            self.content.destroy()

        # show error message
        self.content = tk.Label(self.master, text="The file could not be found.", foreground='red')
        self.content.grid(row=1, column=0)
