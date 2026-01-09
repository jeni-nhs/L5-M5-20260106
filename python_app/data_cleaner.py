import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
#import pyodbc

# Function to output dataframe that can be manipulated via a filepath
def fileLoader(filepath):
    data = pd.read_csv(filepath)
    return data 

# Duplicate Dropping Function
def duplicateCleaner(df):
    # Identify the duplicate rows first
    duplicate_flag = df.duplicated(keep='first')

    # Store the duplicates in separate dataframe
    duplicate_errors = df[duplicate_flag].copy()

    # Remove the duplicates from the main df
    df = df.drop_duplicates().reset_index(drop=True)
    
    return df, duplicate_errors

# NA handler - future scope can handle errors more elegantly. 
def naCleaner(df):
    # Identify the na rows
    na_flag = df.isna().any(axis=1)

    # Store the NAs in a separate dateframe
    na_errors = df[na_flag].copy()

    # Remove the nas from the main df
    df = df.dropna().reset_index(drop=True)

    return df, na_errors

# Turning date columns into datetime
def dateCleaner(col, df):
    date_errors = pd.DataFrame(columns=df.columns)  # Store rows with date errors

    # Strip any quotes from dates
    df[col] = df[col].str.replace('"', "", regex=True)

    try:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

    except Exception as e:
        print(f"Error while converting column {col} to datetime: {e}")

    # Identify rows with invalid dates
    error_flag = pd.to_datetime(df[col], dayfirst=True, errors='coerce').isna()
        
    # Move invalid rows to date_errors - Future feature
    date_errors = df[error_flag]
        
    # Keep only valid rows in df
    df = df[~error_flag].copy()

    # Reset index for the cleaned DataFrame
    df.reset_index(drop=True, inplace=True)

    return df, date_errors

def enrich_dateDuration(colA, colB, df):
    """
    Takes the two datetime input column names and the dataframe to create a new column date_delta which is the difference, in days, between colA and colB.
    
    Note:
    colB>colA
    """
    df['date_delta'] = (df[colB]-df[colA]).dt.days

    #Conditional Filtering to be able to gauge eroneous loans.
    df.loc[df['date_delta'] < 0, 'valid_loan_flag'] = False
    df.loc[df['date_delta'] >= 0, 'valid_loan_flag'] = True

    return df

def writeToSQL(df, table_name, server, database):

    # Create the connection string with Windows Authentication
    connection_string = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    try:
        # Write the DataFrame to SQL Server
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)

        print(f"Table{table_name} written to SQL")
    except Exception as e:
        print(f"Error writing to the SQL Server: {e}")

if __name__ == '__main__':
    print('**************** Starting Clean ****************')

    # Instantiation
    filepath_input = '../sample_data/03_Library Systembook.csv'
    date_columns = ['Book checkout', 'Book Returned']
    all_errors = []
    processed_rows = []
    start_dttm = datetime.now()

    data = fileLoader(filepath=filepath_input)

    # Drop the NAs and record them
    data, na_errors = naCleaner(data)

    if not na_errors.empty:
        na_errors['error_type'] = 'na'
        all_errors.append(na_errors)
    else:
        print("No NAs found")

    # Drop the duplicates and record them
    data, duplicate_errors = duplicateCleaner(data)

    if not duplicate_errors.empty:
        duplicate_errors['error_type'] = 'duplicate'
        all_errors.append(duplicate_errors)

    else:
        print("No duplicates found")

    # Converting date columns into datetime
    date_error_count = 0
    for col in date_columns:
        data, date_errors = dateCleaner(col, data)
        if not date_errors.empty:
            date_errors['error_type'] = 'date'
            all_errors.append(date_errors)
            date_error_count += len(date_errors)
        else:
            print("No date errors found")

    # Combine the error data
    if all_errors:
        final_errors = pd.concat(all_errors, ignore_index=True)
        final_errors['run_dttm'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        final_errors.to_csv('errors_books.csv',index=False)
        print(f"Total errors found: {len(final_errors)}")
    else:
        print("No errors found")

    # Enriching the dataset
    data = enrich_dateDuration(df=data, colA='Book Returned', colB='Book checkout')

    data.to_csv(f'cleaned_books_file_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv')

    #print(data)

    #Cleaning the customer file
    filepath_input_2 = '../sample_data/03_Library SystemCustomers.csv'

    data2 = fileLoader(filepath=filepath_input_2)

    all_errors2 = []
    processed_rows2 = []

    # Drop the NAs and record them
    data2, na_errors2 = naCleaner(data2)

    if not na_errors2.empty:
        na_errors2['error_type'] = 'na'
        all_errors2.append(na_errors2)
    else:
        print("No NAs found")

    # Drop the duplicates and record them
    data2, duplicate_errors2 = duplicateCleaner(data2)

    if not duplicate_errors2.empty:
        duplicate_errors2['error_type'] = 'duplicate'
        all_errors2.append(duplicate_errors2)

    else:
        print("No duplicates found")

    # Combine the error data
    if all_errors2:
        final_errors2 = pd.concat(all_errors2, ignore_index=True)
        final_errors2['run_dttm'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        final_errors2.to_csv('errors_customers.csv',index=False)
        print(f"Total errors found: {len(final_errors2)}")
    else:
        print("No errors found")

    data2.to_csv(f'cleaned_customers_file_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv')

    ## Add processing information

    ## Duration processing
    end_dttm = datetime.now()
    duration = end_dttm - start_dttm

    run_dttm = pd.DataFrame({
        'start_dttm': [start_dttm],
        'end_dttm': [end_dttm],
        'duration_seconds':[duration.total_seconds()]
    })

    run_dttm.to_csv('run_dttm.csv', mode='a', header=not pd.io.common.file_exists('run_dttm.csv'), index=False)

    ## Processed rows information
    processed_rows = pd.DataFrame({
        'process_type': ['processed','date_errors','duplicate_errors','na_errors'],
        'row_count': [
            len(data),
            date_error_count,
            len(duplicate_errors),
            len(na_errors)
        ]
    })

    processed_rows2 = pd.DataFrame({
        'process_type': ['processed','duplicate_errors','na_errors'],
        'row_count': [
            len(data2),
            len(duplicate_errors2),
            len(na_errors2)
        ]
    })

    processed_rows['file_name'] = 'books'
    processed_rows2['file_name'] = 'customers'

    all_processed = pd.concat([processed_rows, processed_rows2], ignore_index=True, sort=False)

    all_processed['run_dttm'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    all_processed.to_csv('process.csv',mode='a', header=not pd.io.common.file_exists('process.csv'),index=False)
    print(all_processed)


    print('**************** DATA CLEANED ****************')

#    print('Writing to SQL Server...')
#
#    writeToSQL(
#        data, 
#        table_name='loans_bronze', 
#        server = 'localhost', 
#        database = 'm5library' 
#    )
#
#    writeToSQL(
#        data2, 
#        table_name='customer_bronze', 
#        server = 'localhost', 
#        database = 'm5library'
#    )
    print('**************** End ****************')