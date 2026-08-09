
import pandas as pd
from config import get_engine


def load_and_clean():
    df = pd.read_csv('data/Movie_Data.csv')

    df.columns = [
        'id', 'title', 'genre', 'budget', 'director_success',  
        'actor_success', 'imdb', 'trailer_views', 'revenue'
    ]

    number_columns = ['budget', 'revenue', 'imdb', 'director_success', 'actor_success']    
    for col in number_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['budget', 'revenue'])

    df['profit'] = df['revenue'] - df['budget']

    df['roi'] = ((df['revenue'] - df['budget']) / df['budget']) * 100

    df['profitable'] = df['profit'] > 0

    df = df.reset_index(drop=True)

    print(f"Loaded {len(df)} movies across {df['genre'].nunique()} genres")
    return df


def push_to_database(df):
    engine = get_engine()
    df.to_sql('movies', con=engine, if_exists='replace', index=False)

    print(f"Pushed {len(df)} rows into PostgreSQL")


if __name__ == '__main__':
    df = load_and_clean()
    push_to_database(df)
