# utils/preprocessing.py

import pandas as pd
import numpy as np

def load_data(order_filepath, calendar_filepath):
    """
    Loads the order and calendar data from CSV files and merges them.
    Args:
        order_filepath (str): Path to the order data CSV file.
        calendar_filepath (str): Path to the calendar data CSV file.
    Returns:
        pd.DataFrame: Merged data containing both order and calendar features.
    """
    # Load data
    orders = pd.read_csv(order_filepath)
    calendar = pd.read_csv(calendar_filepath)
    
    # Merge the dataframes on the 'date' column
    orders['date'] = pd.to_datetime(orders['date'])
    calendar['date'] = pd.to_datetime(calendar['date'])
    
    # Merge on date
    merged_data = pd.merge(orders, calendar, on='date')
    
    return merged_data

def create_lag_features(df, lags=[1, 3, 7]):
    """
    Create lag features for forecasting.
    Args:
        df (pd.DataFrame): Dataframe with 'sku', 'zip_code', 'volume' columns.
        lags (list): List of lag periods to create features for.
    Returns:
        pd.DataFrame: Dataframe with lag features added.
    """
    # Ensure data is sorted by SKU, zip code, and date
    df.sort_values(by=['sku', 'zip_code', 'date'], inplace=True)
    
    # Create lag features
    for lag in lags:
        df[f'lag_{lag}'] = df.groupby(['sku', 'zip_code'])['volume'].shift(lag)
    
    # Create rolling mean
    df['rolling_mean_7'] = df.groupby(['sku', 'zip_code'])['volume'].shift(1).rolling(7).mean()
    
    # Drop NA values caused by lag and rolling mean
    df.dropna(inplace=True)
    
    return df

def encode_categorical_features(df):
    """
    Encodes categorical features like SKU and zip code using integer codes.
    Args:
        df (pd.DataFrame): Dataframe with categorical columns.
    Returns:
        pd.DataFrame: Dataframe with encoded categorical features.
    """
    df['sku_code'] = df['sku'].astype('category').cat.codes
    df['zip_code_encoded'] = df['zip_code'].astype('category').cat.codes
    
    return df

def preprocess_forecasting_data(order_filepath, calendar_filepath, lags=[1, 3, 7]):
    """
    Preprocesses the forecasting data by loading, merging, creating features, and encoding categorical data.
    Args:
        order_filepath (str): Path to the order data CSV file.
        calendar_filepath (str): Path to the calendar data CSV file.
        lags (list): List of lag periods for creating lag features.
    Returns:
        pd.DataFrame: Preprocessed and feature-engineered data.
    """
    # Load and merge data
    df = load_data(order_filepath, calendar_filepath)
    
    # Create lag features and rolling mean
    df = create_lag_features(df, lags=lags)
    
    # Encode categorical features
    df = encode_categorical_features(df)
    
    return df
