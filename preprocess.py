import pandas as pd

def clean_data(df):
    # Data Cleaning Steps
    # 1. Remove rows with missing values
    df.dropna(inplace=True)

    # 2. Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # 3. Text Cleaning
    #    - Convert text to lowercase
    df['reviews.title'] = df['reviews.title'].str.lower()
    df['reviews.text'] = df['reviews.text'].str.lower()

    #    - Remove punctuation and special characters
    df['reviews.title'] = df['reviews.title'].str.replace(r'[^\w\s]', '')
    df['reviews.text'] = df['reviews.text'].str.replace(r'[^\w\s]', '')

    # 4. Feature Engineering
    #    - Extract year, month, and day from dateAdded
    df['dateAdded'] = pd.to_datetime(df['dateAdded'])
    df['year'] = df['dateAdded'].dt.year
    df['month'] = df['dateAdded'].dt.month
    df['day'] = df['dateAdded'].dt.day

    # 5. Data Type Conversion (if needed)
    #    - Convert year, month, and day to integers
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['day'] = df['day'].astype(int)

    # 6. Encoding Categorical Variables (if needed)
    #    - One-hot encoding for categories
    df = pd.get_dummies(df, columns=['categories'], prefix='categories')

    return df