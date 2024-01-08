import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import DateEntry
from datetime import date


class PieChartForm(ttk.Frame):
    """
    Class for the form used to generate pie charts
    """

    def __init__(self, parent, controller):
        """
        Initializes a form, fields are blank by default
        :param parent: the frames parent
        :param travel_record: Optional, include to create an update form
        """
        super().__init__(parent)

        self.controller = controller

        # Select Date range
        select_expenses_label = ttk.Label(self, text='Select the date range to include', anchor='s',
                                          font=('Ariel', 13, 'bold'))
        select_expenses_label.pack(side='top', ipady=10)

        date_entry_frame = ttk.Frame(self)
        date_entry_frame.pack(side='top')

        include_label = ttk.Label(
            date_entry_frame,
            text='Include dates between:',
            anchor='s',
            font=('Ariel', 11)
        )
        include_label.pack(side='left', padx=5)
        self.start_date = DateEntry(master=date_entry_frame, dateformat='%Y-%m-%d', startdate=date(2017,1,1))
        self.start_date.pack(side='left', padx=5)
        conjoining_label = ttk.Label(master=date_entry_frame, text='and', anchor='s', font=('Ariel', 11))
        conjoining_label.pack(side='left', padx=5)
        self.end_date = DateEntry(master=date_entry_frame, dateformat='%Y-%m-%d', startdate=date(2023,12,31))
        self.end_date.pack(side='left', padx=5)

        # Select Expenses
        select_expenses_label = ttk.Label(self, text='Select attributes to include', anchor='s',
                                          font=('Ariel', 13, 'bold'))
        select_expenses_label.pack(side='top', ipady=10)

        expenses_frame = ttk.Frame(self)
        expenses_frame.pack(side='top')

        airfare_boolean = tk.BooleanVar(value=True)
        airfare_check = ttk.Checkbutton(
            expenses_frame,
            text='Airfare',
            variable=airfare_boolean,
            onvalue=True,
            offvalue=False
        )
        airfare_check.pack(side='left', padx=5)

        transport_boolean = tk.BooleanVar(value=True)
        transport_check = ttk.Checkbutton(
            expenses_frame,
            text='Other Transportation Costs',
            variable=transport_boolean,
            onvalue=True,
            offvalue=False
        )
        transport_check.pack(side='left', padx=5)

        lodging_boolean = tk.BooleanVar(value=True)
        meals_check = ttk.Checkbutton(
            expenses_frame,
            text='Lodging',
            variable=lodging_boolean,
            onvalue=True,
            offvalue=False
        )
        meals_check.pack(side='left', padx=5)

        meals_boolean = tk.BooleanVar(value=True)
        meals_check = ttk.Checkbutton(
            expenses_frame,
            text='Meals',
            variable=meals_boolean,
            onvalue=True,
            offvalue=False
        )
        meals_check.pack(side='left', padx=5)

        other_boolean = tk.BooleanVar(value=True)
        other_check = ttk.Checkbutton(
            expenses_frame,
            text='Other Expenses',
            variable=other_boolean,
            onvalue=True,
            offvalue=False
        )
        other_check.pack(side='left', padx=5)

        # Select Titles you wish to include
        select_titles_label = ttk.Label(self, text='Select those titles you wish to include for this graph', anchor='s',
                                        font=('Ariel', 13, 'bold'))
        select_titles_label.pack(side='top', ipady=10)

        expenses_frame = ttk.Frame(self)
        expenses_frame.pack(side='top', padx=5)

        board_member_boolean = tk.BooleanVar(value=True)
        board_member_check = ttk.Checkbutton(
            expenses_frame,
            text='Board Members',
            variable=board_member_boolean,
            onvalue=True,
            offvalue=False
        )
        board_member_check.pack(side='left', padx=5)

        board_boolean = tk.BooleanVar(value=True)
        board_check = ttk.Checkbutton(
            expenses_frame,
            text='Board of Directors',
            variable=board_boolean,
            onvalue=True,
            offvalue=False
        )
        board_check.pack(side='left', padx=5)

        chair_boolean = tk.BooleanVar(value=True)
        chair_check = ttk.Checkbutton(
            expenses_frame,
            text='Chair',
            variable=chair_boolean,
            onvalue=True,
            offvalue=False
        )
        chair_check.pack(side='left', padx=5)

        chairperson_boolean = tk.BooleanVar(value=True)
        chairperson_check = ttk.Checkbutton(
            expenses_frame,
            text='Chairpersons',
            variable=chairperson_boolean,
            onvalue=True,
            offvalue=False
        )
        chairperson_check.pack(side='left', padx=5)

        chief_exec_boolean = tk.BooleanVar(value=True)
        chief_exec_check = ttk.Checkbutton(
            expenses_frame,
            text='Chief Executive Officer',
            variable=chief_exec_boolean,
            onvalue=True,
            offvalue=False
        )
        chief_exec_check.pack(side='left', padx=5)

        director_boolean = tk.BooleanVar(value=True)
        director_check = ttk.Checkbutton(
            expenses_frame,
            text='Executive Directors',
            variable=director_boolean,
            onvalue=True,
            offvalue=False
        )
        director_check.pack(side='left', padx=5)

        vice_chair_boolean = tk.BooleanVar(value=True)
        vice_chair_check = ttk.Checkbutton(
            expenses_frame,
            text='Vice Chair',
            variable=vice_chair_boolean,
            onvalue=True,
            offvalue=False
        )
        vice_chair_check.pack(side='left', padx=5)

        # Buttons
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(side='top', pady=5)

        generate_from_expenses = ttk.Button(
            master=buttons_frame,
            command=self.chart_by_category,
            text='Chart Expenditures by Expense Category',
            style='big.TButton',
            padding=5
        )
        generate_from_expenses.pack(side='left', ipadx=3, padx=3)
        generate_from_titles = ttk.Button(
            master=buttons_frame,
            command=self.chart_by_title,
            text='Chart Expenditures by Title',
            style='big.TButton',
            padding=5
        )
        generate_from_titles.pack(side='left', ipadx=3, padx=3)

        self.expenses_to_include = {
            'airfare': airfare_boolean,
            'other_transport': other_boolean,
            'lodging': lodging_boolean,
            'meals': meals_boolean,
            'other_expenses': other_boolean
        }

        self.titles_to_include = {
            'Board Member': board_member_boolean,
            'Board of Directors': board_boolean,
            'Chair': chair_boolean,
            '%Chairperson%': chairperson_boolean,
            'Chief Executive Officer': chief_exec_boolean,
            '%Executive Director%': director_boolean,
            'Vice Chair': vice_chair_boolean
        }

    def chart_by_category(self):
        self.controller.chart_by_category(self)

    def chart_by_title(self):
        self.controller.chart_by_title(self)
        