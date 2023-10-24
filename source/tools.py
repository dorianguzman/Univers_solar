# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24

@author: DorianGuzman
"""
import pandas as pd
import os

def read_data(filename):
    """
    Read data from a CSV file and preprocess it for analysis.

    Parameters
    ----------
    filename : str
        The path to the CSV file to read.

    Returns
    -------
    pd.DataFrame
        A DataFrame with preprocessed data for analysis.
    """

    # Check if the file exists
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    # Define column data types to improve performance
    dtype_mapping = {
        'wind_speed': float,
        'tmp_amb': float,
        'poa': float,
        'tmp_cell': float,
        'ac_power': float,
        'rain_mm': float,
    }

    # Read the CSV file into a DataFrame with predefined data types
    df = pd.read_csv(filename, dtype=dtype_mapping, parse_dates=['data_date'], errors='coerce')

    # Convert 'ac_power' to watts
    df['ac_power'] *= 1000

    # Set the 'data_date' column as the index
    df.set_index('data_date', drop=True, inplace=True)

    # Rename columns if needed
    # df = df.rename(columns={'old_column_name': 'new_column_name'})

    return df


