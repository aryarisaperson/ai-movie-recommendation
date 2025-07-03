import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from colorama import init, Fore
import time
import sys


# Initialize colorama
init(autoreset=True)

# Load and preprocess the dataset
def load_data(file_path='imdb_top_1000.csv'):
    try:
        df = pd.read_csv(file_path)
        df['combined_features'] = df['Genre'].fillna('') + ' ' + df['Overview'].fillna('')
        return df
    except FileNotFoundError:
        print(Fore.RED + f"Error: The file '{file_path}' was not found.")
        exit()

movies_df = load_data()

# Vectorize the combined features and compute cosine similarity
tfidf=TfidfVectorizer(stop_words="english")
tfidf_matrix=tfidf.fit_form(movies_df["combine_feature"])
cosine_sim=cosine_similarity(tfidf_matrix, tfidf_matrix)

# List all unique genres
def list_genres(df):
    return sorted(set(genre.strip() for sublist in df["Genre"].dropna().str.split(",") for genre in sublist))
genres=list_genres(movies_df)

# Recommend movies based on filters (genre, mood, rating)
def recommend_movies(genre, mood, rating, top_n):
    filtered_df=movies_df
    if genre:
        filtered_df=filtered_df[filtered_df["Genre"].str.contains(genre, case=False, na=False)]
    if rating:
        filtered_df=filtered_df[filtered_df["IMDB_Rating"]<=rating]
    filtered_df=filtered_df.sample(frac=1).reset_index(drop=True)

    recommendations=[]
    for indx,row in filtered_df,iterrows():
        overview=row["Overview"]
        if pd.isna(overview):
            continue
        polarity=Textblob(overview).sentiment.polarity
        if (mood and ((Textblob(mood).sentiment.polarity<0) or polarity>=0)) or not mood:
            recommendations.append(row["Series_Title"], polarity)
        if len(recommendations)==top_n:
            break
    return recommendations if recommendations else "not suitable movie"


# Display recommendations🍿 😊  😞  🎥

def display_recommendations(recs, name):
    print(f"AI analyzed your movie recommendations for {name}.")
    for idx, (title, polarity) in enumerate(recs, 1):
        sentiment="positive" if polarity>0 else "negative" if polarity <0 else "neutral"
        print(f"{idx}.{title} (polarity:{polarity}, {sentiment})")
# Small processing animation

def processing_animation():
    for _ in range(3):
        print(".", end="")
        time.sleep(0.5)

# Handle AI recommendation flow 🔍
def handle_ai(name):
    print(f"Let's find the perfect movie for you, {name}!")
    print("Available Genres for you:")
    for indx,genre in enumerate(genres, 1):
        print(f"{indx}.{genre}")
    print()
    while True:
        genre_input=input("Enter the genre number or name here:").strip()
        if genre_input.isdigit() and 1<=int(genre_input)<=len(genres):
            genre=genres[int(genre_input)-1]
            break
        elif genre_input.title() in genres:
            genre=genre_input.title()
            break
        print("Invalid input; please try again")
    mood=input(f"How are you feeling, {name}? (I will use this to recommend you something.")
    print("Analyzing mood...")
    processing_animation()
    polarity=TextBlob(mood).sentiment.polarity 
    mood_desc="positive" if polarity>0 else "negative" if polarity<0 else "neutral"
    print(f"{name}, I think your mood is {mood_desc}")

    while True:
        rating_input=input("enter the minimum IMDB rating (7.6-9.3) or skip").strip()
        if rating_input.lower()=="skip":
            rating=None
            break
        try:
            rating=float(rating_input)
            if 7.6<=rating<=9.3:
                break
            print("Rating scale is out-of-range, sorry")
        except ValueError:
            print("Sorry, I didn't get that. Can you please try that again?")

   # Processing animation while analyzing mood 😊  😞  😐
    

    # Processing animation while finding movies
    print(f"finding movies for {name}...")

      # Small processing animation while finding movies 🎬🍿
    processing_animation()
    recs=recommend_movies(genre=genre, mood=mood, rating=rating,top_n=5)
    if isinstance(recs,str):
        print(recs)
    else:
        display_recommendations(recs, name)
    while True:
        action=input("Would you like more recommendations? Say yes or no.").strip()
        if action.lower()=="no":
            print(f"Enjoy your movie, {name}!")
            break
        elif action.lower()=="yes":
            recs=recommend_movies(genre=genre, mood=mood, rating=rating, top_n=5)
            if isinstance (recs, str):
                print(recs)
            else:
                display_recommendations(recs, name)
        else:
            print("Sorry, didn't catch that!")

   
# Main program 🎥
def main():
    print("Welcome to your personal movie recommendation system!🎥🎥🎥🎥🎥🎥🎬🍿🎬🍿🎥🎥🎥🎬🍿🎬🍿🎬🍿")
    name=input("Whats your name?").strip()
    print(f"Hello, {name}!")
    handle_ai(name)
if __name__=="__main__":
    main()