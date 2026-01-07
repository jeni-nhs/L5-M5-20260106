class Calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def get_sum(self):
        return self.num1 + self.num2
    
    def get_difference(self):
        return self.num1 - self.num2
    
    def get_product(self):
        return self.num1 * self.num2
    
    def get_quotient(self):
        return self.num1 / self.num2
    
if __name__ == '__main__':
    myCalc = Calculator(num1 = 1093450, num2 = 234527)
    print(myCalc.get_product())
    