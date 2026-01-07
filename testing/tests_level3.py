import unittest
from calculator import Calculator
import pandas as pd
from datetime import datetime
from checkout_days import checkout_days

class TestBookBorrowedDays(unittest.TestCase):

    def setUp(self):
        self.csv_file = 'output_data/books_output.csv'

    def test_days_borrowed_calculation(self):
        df = pd.read_csv(self.csv_file)

        df['book_checkout'] = pd.to_datetime(df['book_checkout'])
        df['book_returned'] = pd.to_datetime(df['book_returned'])

        df = df.dropna(subset=['book_checkout'])
        df = df.dropna(subset=['book_returned'])

        for index, row in df.iterrows():
            checkout_date = row['book_checkout']
            return_date = row['book_returned']
            actual_days = row['days_borrowed']

            checkout_days = (checkout_date - pd.Timestamp("1970-01-01")).days
            return_days = (return_date - pd.Timestamp("1970-01-01")).days

            calc = Calculator(return_days, checkout_days)

            expected_days = calc.get_difference()

            self.assertEqual(
                expected_days,
                actual_days
            )

if __name__ == '__main__':
    unittest.main()
