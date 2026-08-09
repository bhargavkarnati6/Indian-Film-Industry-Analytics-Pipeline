import pandas as pd
from sqlalchemy import func, cast, Numeric, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Float, String, Boolean
from config import get_engine

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id               = Column(Integer, primary_key=True)
    title            = Column(String)
    genre            = Column(String)
    budget           = Column(Float)
    director_success = Column(Float)
    actor_success    = Column(Float)
    imdb             = Column(Float)
    trailer_views    = Column(Float)
    revenue          = Column(Float)
    roi              = Column(Float)
    profit           = Column(Float)
    profitable       = Column(Boolean)

from sqlalchemy import Integer as IntType

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def genre_performance():
    session = get_session()

    results = (
        session.query(
            Movie.genre,
            func.count(Movie.id).label('total_movies'),
            func.round(cast(func.avg(Movie.roi), Numeric), 1).label('avg_roi'),
            func.round(cast(func.avg(Movie.revenue), Numeric), 1).label('avg_revenue'),
            func.round(cast(func.avg(Movie.imdb), Numeric), 1).label('avg_imdb'),
        )
        .group_by(Movie.genre)
        .order_by(func.avg(Movie.roi).desc())
        .all()
    )

    df = pd.DataFrame(results)
    print("\n── Genre Performance ──────────────────────")
    print(df.to_string(index=False))
    session.close()
    return df


def hit_rate_by_genre():
    session = get_session()

    results = (
        session.query(
            Movie.genre,
            func.count(Movie.id).label('total_movies'),
            func.sum(cast(Movie.profitable, IntType)).label('profitable_count'),
        )
        .group_by(Movie.genre)
        .all()
    )

    df = pd.DataFrame(results)
    df['hit_rate_pct'] = round(df['profitable_count'] / df['total_movies'] * 100, 1)
    df = df.sort_values('hit_rate_pct', ascending=False)

    print("\n── Hit Rate by Genre ──────────────────────")
    print(df.to_string(index=False))
    session.close()
    return df


def top_10_by_profit(limit=10):
    session = get_session()

    results = (
        session.query(Movie.title, Movie.genre, Movie.budget, Movie.revenue, Movie.profit)
        .order_by(Movie.profit.desc())
        .limit(limit)
        .all()
    )

    df = pd.DataFrame(results)
    print(f"\n── Top {limit} Movies by Profit ────────────────")
    print(df.to_string(index=False))
    session.close()
    return df


def biggest_losses(limit=10):
    session = get_session()

    results = (
        session.query(Movie.title, Movie.genre, Movie.budget, Movie.revenue, Movie.profit)
        .filter(Movie.profitable == False)
        .order_by(Movie.profit.asc())
        .limit(limit)
        .all()
    )

    df = pd.DataFrame(results)
    print(f"\n── Biggest {limit} Losses ─────────────────────────")
    print(df.to_string(index=False))
    session.close()
    return df


if __name__ == '__main__':
    genre_performance()
    hit_rate_by_genre()
    top_10_by_profit()
    biggest_losses()
