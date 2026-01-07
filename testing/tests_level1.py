import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calc = Calculator(8,2)
        answer = calc.get_sum()
        print(f'Calculator parameters: {calc.num1}, {calc.num2}')
        self.assertEqual(calc.get_sum(), 10, 'The answer was not ten.')

    # test_diff, test_product, test_quotient

    def test_diff(self):
        diff_calc = Calculator(8,2)
        answer = diff_calc.get_difference()
        self.assertEqual(diff_calc.get_difference(),6, 'The answer was not 6.')

    def test_product(self):
        prod_calc = Calculator(8,2)
        answer = prod_calc.get_product()
        self.assertEqual(prod_calc.get_product(),16,'The answer was not 16.')

    def test_quotient(self):
        prod_quot = Calculator(8,2)
        answer = prod_quot.get_quotient()
        self.assertEqual(prod_quot.get_quotient(),4,'The answer was not 4.')        

if __name__ == '__main__':
    unittest.main()