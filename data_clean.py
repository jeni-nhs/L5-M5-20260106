import pandas as pd

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(' ','_')
    return df

def clean_column_values(df):
    df['book_checkout'] = df['book_checkout'].str.replace('"','',regex=False)

def read_csv(filepath):
    df = pd.read_csv('sample_data/03_Library Systembook.csv')
    print('Dataframe here')
    return(df)

def dropna():
    df = df.dropna()
    return(df)

def column_names():
    df.columns = df.columns.str.lower().str.replace(' ','_')
    return(df)

if __name__ == '__main__':
    print('Dataframe')