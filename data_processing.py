import re
import pandas as pd

def rename_columns(df):
    df = df.copy()
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_", regex=True)
        .str.normalize('NFKD')
        .str.encode('ascii', errors='ignore')
        .str.decode('utf-8')
    )
    column_mapping = {
        "original_titlÊ": "original_title",
        "genrë¨": "genre",
        "unnamed:_8": "unnamed_8"
    }
    df.rename(columns=column_mapping, inplace=True)
    return df

def clean_and_fill_content_rating(df):
    df = df.copy()
    df["content_rating"] = df["content_rating"].fillna("Unrated") 
    df["content_rating"] = df["content_rating"].replace("Not Rated", "Unrated") 
    return df

def remove_fully_null_columns_rows(df):
    df = df.dropna(axis=0, how='all') 
    df = df.dropna(axis=1, how='all')  
    return df

def clean_release_year(df):
    df = df.copy()
    df["release_year_coerce"] = pd.to_datetime(df["release_year"], errors="coerce")
    df["release_year_mixed"] = pd.to_datetime(df["release_year"], errors="coerce", format="mixed")
    return df

def clean_income(df):
    df = df.copy()
    df["income"] = df["income"].replace({'\$': '', ',': ''}, regex=True)  # Remove '$' and commas
    df["income"] = pd.to_numeric(df["income"], errors="coerce")  # Convert to numeric (int)
    df["income"] = df["income"].fillna(0).astype(int)  # Replace NaN with 0 and convert to int
    return df
