import pandas as pd

def checkout_days(checkout_date,returned_date):
    if pd.isna(checkout_date) or pd.isna(returned_date):
        return None
    return int((returned_date - checkout_date).days)

if __name__ == '__main__':
    checkout_days()