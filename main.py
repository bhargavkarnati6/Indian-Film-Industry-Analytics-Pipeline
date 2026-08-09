from load_data import load_and_clean, push_to_database
from analyse   import genre_performance, hit_rate_by_genre, top_10_by_profit, biggest_losses
from visualise import get_data, build_dashboard


def main():
    print("=" * 50)
    print("  Indian Film Industry Analytics Pipeline")
    print("=" * 50)

    print("\n[Step 1] Loading data...") 
    df = load_and_clean()
    push_to_database(df)

    print("\n[Step 2] Running analysis...") 
    genre_performance()
    hit_rate_by_genre()
    top_10_by_profit()
    biggest_losses()

    print("\n[Step 3] Building dashboard...") 
    all_movies, telugu = get_data()
    build_dashboard(all_movies, telugu)

    print("\n" + "=" * 50)
    print("  Done!")
    print("=" * 50)


if __name__ == '__main__':
    main()
