import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, String, Boolean, Integer
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


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


TELUGU_TITLES = [
    'Aadavallu Meeku Johaarlu', 'Ashoka Vanamlo Arjuna Kalyanam', 'DJ Tillu',
    'Hi Nanna', 'Most Eligible Bachelor', 'Radhe Shyam', 'RRR',
    'Baahubali: The Beginning', 'Baahubali: The Conclusion',
    'Pushpa: The Rise - Part 1', 'Kalki 2898 AD', 'Pushpa: The Rule - Part 2',
    'Devara part 1', 'Tuck Jagadish', 'Bheemla nayak', 'krack', 'Saaho',
    'Geetha govindam', 'Tillu Sqaure', 'Aadavallu miku joharalu',
    'Sundaram master', 'Kalki-2989AD', 'Pushpa the rise-part 1', 'Devara -1',
    'Pushpaka Vimanam', 'Nene Raju nene Mantri', 'Vakeel Saab',
    'Arjun Suravaram', 'Kalki', 'Bluff Master', 'Baahubali 2: The Conclusion',
    'Ala Modalaindi', 'Ammammagarillu', 'Anni Manchi Sakunamule', 'Arya 2',
    'Baby', 'Chitralahari', 'Color Photo', 'Dear Comrade', 'Desamuduru',
    'Majili', 'Nenu Sailaja', 'Ninu Kori', 'Hello Guru Prema Kosame',
    'Rangasthalam', 'Maharshi', 'Jersey', 'Shyam Singha Roy',
    'Ante Sundaraniki', 'Uppena', 'Akhanda', 'Kushi', 'Guntur Kaaram',
    'Hanu-Man', 'Eagle', 'Wailtar veerayaa', 'Arjuna Phalguna',
    'Gandharva dhaari arjuna', 'Sailja reddy alludu', 'Alludu Seenu',
    'Gandeevadhari Arjuna', 'Pelli choopulu', 'Middle class melodies',
    'Raju gari gadhi', 'Krishnarjuna Yudham', 'krishnarjuna yuddham',
]

COLORS = ['#E63946', '#457B9D', '#2A9D8F', '#E9C46A', '#F4A261']


def get_data():
    session = get_session()
    results = session.query(
        Movie.title,
        Movie.genre,
        Movie.revenue,
        Movie.profitable,
    ).all()

    session.close()

    all_movies = pd.DataFrame(results)

    telugu = all_movies[all_movies['title'].isin(TELUGU_TITLES)].copy()

    return all_movies, telugu


def build_dashboard(all_movies, telugu):
    fig, axes = plt.subplots(3, 2, figsize=(16, 18))
    fig.suptitle('Indian Film Industry — Analytics Dashboard',
                 fontsize=18, fontweight='bold')
    fig.patch.set_facecolor('#F8F9FA')

    ax1 = axes[0, 0]
    top_india = all_movies.nlargest(10, 'revenue')
    ax1.barh(top_india['title'].str[:25], top_india['revenue'],
             color=COLORS[0], alpha=0.85)
    ax1.set_title('Top 10 Highest Grossing — All India', fontweight='bold')
    ax1.set_xlabel('Box Office Revenue (Cr)')
    ax1.invert_yaxis()
    ax1.set_facecolor('#F8F9FA')
    for i, val in enumerate(top_india['revenue']):
        ax1.text(val + 10, i, f'₹{val:.0f}Cr', va='center', fontsize=8)

    ax2 = axes[0, 1]
    top_telugu = telugu.nlargest(10, 'revenue')
    ax2.barh(top_telugu['title'].str[:25], top_telugu['revenue'],
             color=COLORS[1], alpha=0.85)
    ax2.set_title('Top 10 Highest Grossing — Telugu', fontweight='bold')
    ax2.set_xlabel('Box Office Revenue (Cr)')
    ax2.invert_yaxis()
    ax2.set_facecolor('#F8F9FA')
    for i, val in enumerate(top_telugu['revenue']):
        ax2.text(val + 10, i, f'₹{val:.0f}Cr', va='center', fontsize=8)

    ax3 = axes[1, 0]
    genre_india = all_movies.groupby('genre')['revenue'].mean().sort_values(ascending=False).round(1)
    bars3 = ax3.bar(genre_india.index, genre_india.values, color=COLORS[:len(genre_india)])
    ax3.set_title('Avg Revenue by Genre — All India (Cr)', fontweight='bold')
    ax3.set_ylabel('Avg Revenue (Cr)')
    ax3.set_xlabel('Genre')
    ax3.set_facecolor('#F8F9FA')
    ax3.tick_params(axis='x', rotation=15)
    for bar, val in zip(bars3, genre_india.values):
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 1, f'₹{val:.0f}Cr', ha='center', fontsize=8)

    ax4 = axes[1, 1]
    genre_telugu = telugu.groupby('genre')['revenue'].mean().sort_values(ascending=False).round(1)
    bars4 = ax4.bar(genre_telugu.index, genre_telugu.values, color=COLORS[:len(genre_telugu)])
    ax4.set_title('Avg Revenue by Genre — Telugu (Cr)', fontweight='bold')
    ax4.set_ylabel('Avg Revenue (Cr)')
    ax4.set_xlabel('Genre')
    ax4.set_facecolor('#F8F9FA')
    ax4.tick_params(axis='x', rotation=15)
    for bar, val in zip(bars4, genre_telugu.values):
        ax4.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 1, f'₹{val:.0f}Cr', ha='center', fontsize=8)

    ax5 = axes[2, 0]
    hit_india = all_movies.groupby('genre')['profitable'].mean().mul(100).round(1).sort_values(ascending=False)
    bars5 = ax5.bar(hit_india.index, hit_india.values, color=COLORS[:len(hit_india)])
    ax5.set_title('Genre Hit Rate — All India (%)', fontweight='bold')
    ax5.set_ylabel('% of Movies Profitable')
    ax5.set_xlabel('Genre')
    ax5.axhline(50, color='black', linewidth=1, linestyle='--', label='50% mark')
    ax5.legend(fontsize=9)
    ax5.set_facecolor('#F8F9FA')
    ax5.tick_params(axis='x', rotation=15)
    for bar, val in zip(bars5, hit_india.values):
        ax5.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.5, f'{val}%', ha='center', fontsize=8)

    ax6 = axes[2, 1]
    hit_telugu = telugu.groupby('genre')['profitable'].mean().mul(100).round(1).sort_values(ascending=False)
    bars6 = ax6.bar(hit_telugu.index, hit_telugu.values, color=COLORS[:len(hit_telugu)])
    ax6.set_title('Genre Hit Rate — Telugu (%)', fontweight='bold')
    ax6.set_ylabel('% of Movies Profitable')
    ax6.set_xlabel('Genre')
    ax6.axhline(50, color='black', linewidth=1, linestyle='--', label='50% mark')
    ax6.legend(fontsize=9)
    ax6.set_facecolor('#F8F9FA')
    ax6.tick_params(axis='x', rotation=15)
    for bar, val in zip(bars6, hit_telugu.values):
        ax6.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.5, f'{val}%', ha='center', fontsize=8)

    plt.tight_layout()
    plt.savefig('outputs/dashboard.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Dashboard saved to outputs/dashboard.png")


if __name__ == '__main__':
    all_movies, telugu = get_data()
    build_dashboard(all_movies, telugu)
