import pandas as pd
import numpy as np
from datetime import datetime
import time

def process_file(file):

    print("Processing file: {file.name}")

    start_time = time.time()
    df = read_large_file(file)
    print("Time to read file: {time.time() - start_time:.2f} seconds")


    print("Inferred Data Types:")
    print(df.dtypes)

    return df

def infer_and_convert_types(df):

    for col in df.columns:

        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')
        if not df_converted.isna().all():  # If at least one value is numeric
            df[col] = df_converted
            continue

        # Attempt to convert to datetime
        try:
            df[col] = pd.to_datetime(df[col])
            continue
        except (ValueError, TypeError):
            pass

        # Check if the column could be complex numbers 
        try: 
            df[col] = df[col].apply(complex) 
            continue 
        except (ValueError, TypeError): 
            pass

        # Check if the column should be categorical
        if len(df[col].unique()) / len(df[col]) < 0.5:  # Example threshold for categorization
            df[col] = pd.Categorical(df[col])

        # Check if column could be boolean
        unique_vals = set(df[col].dropna().str.lower().unique()) 
        boolean_values = {'true', 'false', 'yes', 'no'} 
        if unique_vals.issubset(boolean_values): 
            df[col] = df[col].map({'true': True, 'false': False, 'yes': True, 'no': False, 'Yes': True, 'No': False}) 
            df[col] = df[col].astype('bool')

    return df

def read_large_file(file, chunk_size=100000):
   
    if file.name.endswith('.csv'):
        reader = pd.read_csv(file, chunksize=chunk_size)
    elif file.name.endswith('.xlsx'):
        reader = pd.read_excel(file, chunksize=chunk_size)
    else:
        raise ValueError("Unsupported file type. Please provide a CSV or Excel file.")

    # Initialize an empty DataFrame to hold the result
    full_df = pd.DataFrame()

    for chunk in reader:
        # Process and convert data types for each chunk
        chunk = infer_and_convert_types(chunk)
        full_df = pd.concat([full_df, chunk], ignore_index=True)

    return full_df


