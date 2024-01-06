# Program Written by Jason Buitenwerf

import tkinter
from model import TravelRecord
from view import Window
from controller import Controller
import mysql.connector

import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

class App(tkinter.Tk):
    """
    Entry point for the program, initializes the data structure, the view and the controller.
    """

    def __init__(self):
        """
        Entry point for the program, initializes the data structure, the view and the controller.
        """
        super().__init__()

        self.title('Ttk Python App')

        # create a model
        expense_list = []

        # create database connection
        mysql_connection = mysql.connector.connect(**config)

        cursor = mysql_connection.cursor()

        cursor.execute("SELECT * FROM travel_records")

        for record in cursor.fetchall():
            expense_list.append(
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

        # create a view and place it on the root window
        view = Window(self)
        view.pack()

        # create a controller
        controller = Controller(expense_list, view)

        # set the controller to view
        view.set_controller(controller)

        # display records on startup
        controller.display()

        # Configure style
        # self.style = ttk.Style(self)
        # self.style.configure('TCheckbutton', font=('Ariel', 11))
        # self.style.configure('TButton', font=('Ariel', 10))
        # self.style.configure('big.TButton', font=('Ariel', 12))


if __name__ == '__main__':
    app = App()
    app.state("zoomed")
    app.mainloop()
