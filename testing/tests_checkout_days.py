import unittest
import pandas as pd
from checkout_days_function import checkout_days

class TestBookBorrowedDays(unittest.TestCase):

    def setUp(self):
        self.checkout_date = pd.Timestamp('2025-01-01')
        self.returned_date = pd.Timestamp('2025-01-06')

    def test_diff(self):
        answer = checkout_days(self.checkout_date, self.returned_date)
        self.assertEqual(answer, 5, 'The answer is wrong.')

if __name__ == '__main__':
    unittest.main()
