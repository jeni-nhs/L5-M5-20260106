import pandas as pd
import sys

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(' ','_')
    return df

def clean_column_values(df):
    df['book_checkout'] = df['book_checkout'].str.replace('"','',regex=False)

    # replace 2 weeks with a number
    df['days_allowed_to_borrow'] = df['days_allowed_to_borrow'].str.replace('2 weeks','14',regex=False).astype(int)

    # capitalise book titles
    df['books'] = df['books'].str.title()

    # Fix LOTR books
    mask = df['books'].str.startswith('Lord Of The Rings', na=False)
    df.loc[mask, 'books'] = df.loc[mask,'books'].str.replace('Kind','King', regex=False)

    return df

def clean_dates(df, date_columns):
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def process_csv(input_file,output_file):
    df = pd.read_csv(input_file)

    df = clean_column_names(df)
    df = clean_column_values(df)
    df = clean_dates(df)

    df.to_csv(output_file, index=False)

    return df


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    df = process_csv(input_file, output_file)
    print(f"csv processing complete! output saved to {output_file}")