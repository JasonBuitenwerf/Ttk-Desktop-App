# Program Written by Jason Buitenwerf

class TravelRecord:
    """Acts as a Model for the csv file: travelq.csv"""

    def __init__(self, ref_number, title_en, purpose_en, start_date, end_date, airfare, other_transport, lodging,
                 meals, other_expenses, total):
        """Initializes the TravelRecord"""
        self.ref_number = ref_number
        self.title_en = title_en
        self.purpose_en = purpose_en
        self.start_date = start_date
        self.end_date = end_date
        self.airfare = airfare
        self.other_transport = other_transport
        self.lodging = lodging
        self.meals = meals
        self.other_expenses = other_expenses
        self.total = total

    def __str__(self):
        """Return a string listing the values contained in the record"""
        return f"{self.ref_number}, {self.title_en}, {self.purpose_en}, {self.start_date}, {self.end_date}, " \
               f"{self.airfare}, {self.other_transport}, {self.lodging}, {self.meals}, {self.other_expenses}, " \
               f"{self.total}"

    def __eq__(self, other):
        """
        Defines how equality of TravelRecords is judged: all fields must contain the same data
        :param other: the TravelRecord to compare with this TravelRecord
        """
        if not isinstance(other, TravelRecord):
            return False

        return (
                self.ref_number == other.ref_number
                and self.title_en == other.title_en
                and self.purpose_en == other.purpose_en
                and self.start_date == other.start_date
                and self.end_date == other.end_date
                and self.airfare == other.airfare
                and self.other_transport == other.other_transport
                and self.lodging == other.lodging
                and self.meals == other.meals
                and self.other_expenses == other.other_expenses
                and self.total == other.total
        )

    def to_tuple(self):
        """
        Creates a tuple listing the values of this record's attributes
        :return: the tuple listing this records attributes
        """
        record_tuple = (
            self.ref_number,
            self.title_en,
            self.purpose_en,
            self.start_date,
            self.end_date,
            self.airfare,
            self.other_transport,
            self.lodging,
            self.meals,
            self.other_expenses,
            self.total
        )

        return record_tuple
