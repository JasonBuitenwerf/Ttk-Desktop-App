# Program written by Jason Buitenwerf

import csv
import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as pyplot

from new_record_form import NewRecordForm
from pie_chart_form import PieChartForm
from model import TravelRecord

class Controller:
    """
    The controller holds the view and the data structure, and is responsible for data manipulation
    """

    def __init__(self, model, view):
        """
        Initializes the controller
        :param model: the in-memory data structure, a list of records
        :param view: the window that this controller controls
        """
        self.model = model
        self.view = view
        load_dotenv()
        self.config = {
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'database': os.getenv("DB_DATABASE")
        }
        self.insert_statement = """
        INSERT INTO travel_records (
            ref_number, 
            title_en, 
            purpose_en, 
            start_date, 
            end_date, 
            airfare, 
            other_transport, 
            lodging, 
            meals, 
            other_expenses, 
            total
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.update_statement = """
        UPDATE travel_records
        SET
            ref_number = %s,
            title_en = %s,
            purpose_en = %s,
            start_date = %s,
            end_date = %s,
            airfare = %s,
            other_transport = %s,
            lodging = %s,
            meals = %s,
            other_expenses = %s, 
            total = %s
        WHERE
            ref_number = %s
        """
        self.delete_statement = "DELETE FROM travel_records WHERE ref_number = %s"

    def reload(self, filepath):
        """
        Loads a file to the database, replacing the tables data with that of the csv
        :param filepath: the filepath of the file to load
        """
        try:
            with open(filepath, encoding='utf-8-sig') as csv_file:
                reader = csv.DictReader(csv_file)
                self.model = []
                for row in reader:
                    self.model.append(
                        TravelRecord(
                            row["ref_number"],
                            row["title_en"],
                            row["purpose_en"],
                            datetime.strptime(row["start_date"], "%Y-%m-%d") if row["start_date"] != '' else None,
                            datetime.strptime(row["end_date"], "%Y-%m-%d") if row["end_date"] != '' else None,
                            float(row["airfare"]) if row["airfare"] != "" else 0.0,
                            float(row["other_transport"]) if row["other_transport"] != "" else 0.0,
                            float(row["lodging"]) if row["lodging"] != "" else 0.0,
                            float(row["meals"]) if row["meals"] != "" else 0.0,
                            float(row["other_expenses"]) if row["other_expenses"] != "" else 0.0,
                            float(row["total"]) if row["total"] != "" else 0.0
                        )
                    )
        except FileNotFoundError:
            self.view.display_fnf_error()

        # Create database connection
        mysql_connection = mysql.connector.connect(**self.config)

        cursor = mysql_connection.cursor()

        # replace table in db
        cursor.execute("DELETE FROM travel_records")

        values = []  # a list of tuples, each representing a travel_record read from the file
        for record in self.model:
            values.append(record.to_tuple())

        cursor.executemany(self.insert_statement, values)
        mysql_connection.commit()

        cursor.close()
        mysql_connection.close()

    def save(self, filepath):
        """
        Saves the data to a file
        :param filepath: the filepath of the file to be written to
        """
        try:
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['ref_number', 'title_en', 'purpose_en', 'start_date', 'end_date', 'airfare',
                                 'other_transport', 'lodging', 'meals', 'other_expenses', 'total'])
                for row in self.model:
                    writer.writerow([row.ref_number, row.title_en, row.purpose_en, row.start_date, row.end_date,
                                     row.airfare, row.other_transport, row.lodging, row.meals, row.other_expenses,
                                     row.total])
        except FileNotFoundError:
            self.view.display_fnf_error()

    def display(self):
        """
        Clears the content section of the view and asks the view to display the records
        """
        # Cleanup
        for child in self.view.content.winfo_children():
            child.destroy()

        self.model = []
        # create database connection
        mysql_connection = mysql.connector.connect(**self.config)

        cursor = mysql_connection.cursor()

        cursor.execute("SELECT * FROM travel_records")

        for record in cursor.fetchall():
            self.model.append(
                TravelRecord(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                    record[5],
                    record[6],
                    record[7],
                    record[8],
                    record[9],
                    record[10]
                )
            )

        cursor.close()
        mysql_connection.close()

        self.view.display(self.model[0:100])

    def display_form(self, travel_record=None):
        """
        Clears the content section of the view and creates a form to be displayed there instead, used for both new
        records and for updating existing records
        :param travel_record: the TravelRecord to be edited, exclude to create an empty form for creating a new record
        """
        # Cleanup
        for child in self.view.content.winfo_children():
            child.destroy()

        if travel_record is None:
            # Create new form and place it on the grid
            form = NewRecordForm(self.view.content, self)
        else:
            form = NewRecordForm(self.view.content, self, travel_record)

        form.pack(side="top", expand=True)

    def display_graph_options(self):
        # Cleanup
        for child in self.view.content.winfo_children():
            child.destroy()

        # Display graph creation form
        form = PieChartForm(parent=self.view.content, controller=self)
        form.pack(side="top", expand=True)

    def create_new(self, form, new_record, old_record=None):
        """
        Creates or updates a record in the database
        :param form: the form calling this method, used for displaying error/success messages
        :param new_record: the record to be added
        :param old_record: optional, include a record to replace it with new_record in the database
        """

        # create a new record if there is no old_record
        if old_record is None:
            record_is_unique = True
            for record in self.model:
                if new_record.ref_number == record.ref_number:
                    record_is_unique = False
            if record_is_unique:
                self.model.append(new_record)

                # create database connection
                mysql_connection = mysql.connector.connect(**self.config)

                cursor = mysql_connection.cursor()

                cursor.execute(self.insert_statement, new_record.to_tuple())
                mysql_connection.commit()

                cursor.close()
                mysql_connection.close()

                form.show_success_message("Travel record successfully added.")
            else:
                form.show_failure_message(
                    "Travel record already added, cannot add multiple records with the same ref_number."
                )

        # update the specified record
        else:
            try:
                record_is_unique = True
                for record in self.model:
                    if (record != old_record) and (new_record.ref_number == record.ref_number):
                        record_is_unique = False
                if record_is_unique and (new_record != old_record):
                    index = self.model.index(old_record)
                    self.model[index] = new_record

                    # create database connection
                    mysql_connection = mysql.connector.connect(**self.config)

                    cursor = mysql_connection.cursor()

                    values = new_record.to_tuple() + (old_record.ref_number,)
                    cursor.execute(self.update_statement, values)
                    mysql_connection.commit()

                    cursor.close()
                    mysql_connection.close()

                    form.show_success_message("Travel record successfully updated.")
                else:
                    form.show_failure_message("Travel record was not changed")
            except ValueError:
                form.show_failure_message(
                    "The record was already updated or you are trying to update column headers"
                )

    def delete_record(self, record):
        """
        Removes a record from the database
        :param record: record to be removed
        """
        # remove from in-memory list
        self.model.remove(record)

        # create database connection
        mysql_connection = mysql.connector.connect(**self.config)

        cursor = mysql_connection.cursor()

        cursor.execute("DELETE FROM travel_records WHERE ref_number = %s", (record.ref_number,))
        mysql_connection.commit()

        cursor.close()
        mysql_connection.close()

    def chart_by_category(self, form):
        """
        Generates a pie chart with slices representing expense categories
        :param form: the form used to generate the chart, provides access to the selected options
        """
        start_date = form.start_date.entry.get()
        end_date =form.end_date.entry.get()
        labels = []

        select_query = 'SELECT '
        for key in form.expenses_to_include:
            if form.expenses_to_include[key].get():
                select_query += f"sum({key}), "
                labels.append(key)
        select_query = select_query[:-2] + f"FROM travel_records " \
                                           f"WHERE start_date >= '{start_date}' " \
                                           f"AND end_date <= '{end_date}' AND ("
        for key in form.titles_to_include:
            if form.titles_to_include[key].get():
                select_query += f"title_en LIKE '{key}' OR "
        select_query = select_query[:-4] + ")"

        # create database connection and execute query
        mysql_connection = mysql.connector.connect(**self.config)
        cursor = mysql_connection.cursor()
        cursor.execute(select_query)
        record = list(cursor.fetchone())
        cursor.close()
        mysql_connection.close()

        for attribute in record:
            print(attribute)
        sum_total = sum(record)
        iterable_total = []
        while len(iterable_total) < len(record):
            iterable_total.append(sum_total)
        percentages = list(map(lambda x, total: x / total * 100, record, iterable_total))
        print(len(percentages))
        for percentage in percentages:
            print(percentage)
        pyplot.pie(percentages, labels=labels)
        pyplot.show()

    def chart_by_title(self, form):
        """
        Generates a pie chart with slices representing expense categories
        :param form: the form used to generate the chart, provides access to the selected options
        """
        start_date = form.start_date.entry.get()
        end_date =form.end_date.entry.get()
        select_query = 'SELECT title_en, sum('
        for key in form.expenses_to_include:
            if form.expenses_to_include[key].get():
                select_query += f"{key}+"
        select_query = select_query[:-1] + f") FROM travel_records " \
                                           f"WHERE start_date >= '{start_date}' " \
                                           f"AND end_date <= '{end_date}' AND ("
        for key in form.titles_to_include:
            if form.titles_to_include[key].get():
                select_query += f"title_en LIKE '{key}' OR "
        select_query = select_query[:-4] + ") GROUP BY title_en ORDER BY title_en"

        # create database connection and execute query
        mysql_connection = mysql.connector.connect(**self.config)
        cursor = mysql_connection.cursor()
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        mysql_connection.close()

        expenses_by_title = {
            'Board Members': 0,
            'Board of Directors': 0,
            'Chair': 0,
            'Chairpersons': 0,
            'Chief Executive Officer': 0,
            'Executive Directors': 0,
            'Vice Chair': 0
        }
        expenses_by_selected_titles = {}

        for record in records:
            if record[0].lower() == 'board member':
                expenses_by_title['Board Members'] += record[1]
            elif record[0].lower() == 'board of directors':
                expenses_by_title['Board of Directors'] += record[1]
            elif record[0].lower() == 'chair':
                expenses_by_title['Chair'] += record[1]
            elif 'chairperson' in record[0].lower():
                expenses_by_title['Chairpersons'] += record[1]
            elif record[0].lower() == 'chief executive officer':
                expenses_by_title['Chief Executive Officer'] += record[1]
            elif 'executive director' in record[0]:
                expenses_by_title['Executive Directors'] += record[1]
            elif record[0].lower() == 'vice chair':
                expenses_by_title['Vice Chair'] += record[1]

        for title in expenses_by_title:
            if expenses_by_title[title]:
                print(expenses_by_title[title].__int__)
                expenses_by_selected_titles.update({title: expenses_by_title[title]})
        sum_total = sum(expenses_by_selected_titles.values())
        iterable_total = []
        while len(iterable_total) < len(expenses_by_selected_titles):
            iterable_total.append(sum_total)
        percentages = list(
            map(lambda attribute, total: attribute / total * 100, expenses_by_selected_titles.values(), iterable_total))
        pyplot.pie(percentages, labels=list(expenses_by_selected_titles.keys()))
        pyplot.show()
        