import streamlit as st
import pandas as pd
import requests
import pickle
import time

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = movies[['title', 'movie_id']].iloc[movie_indices]
    return recommended_movies

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '7e49c6ba5ed897b00b86bae41cabd73c'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
    return "https://via.placeholder.com/500x750?text=Poster+Not+Available"

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stHeader {
        color: #000000 !important;
        font-size: 36px;
        font-weight: bold !important;
        text-align: center;
    }
    .stSelectbox {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1);
    }
    .stCaption {
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        margin-top: 5px;
        color: black;
    }
    .stSpacing {
        margin-bottom: 10px;
    }
    .time-display {
        font-size: 14px;
        text-align: center;
        color: #1f77b4;
        margin-top: 10px;
        font-weight: bold;
    }
    .recommendation-header {
        color: black !important;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI
st.markdown("<h1 class='stHeader'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

# Movie selection dropdown
selected_movie = st.selectbox(
    "Select a movie:", 
    movies['title'].values, 
    key="movie_select", 
    help="Choose a movie to get recommendations."
)

# Recommendation button
if st.button('Get Recommendations', key="recommend_button"):
    start_time = time.time()  # Start timing
    
    with st.spinner("Fetching recommendations..."):
        recommendations = get_recommendations(selected_movie)
        time.sleep(1)  # Simulate loading delay for better UX

    # Recommendation header with black text
    st.markdown("<div class='recommendation-header'>Here are your top 10 recommendations:</div>", unsafe_allow_html=True)
    st.write("")

    # Create a 2x5 grid layout for movie posters
    for i in range(0, 10, 5):  # Loop over rows (2 rows, 5 movies each)
        cols = st.columns(5)  # Create 5 columns for each row
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130, use_container_width=True)
                    st.markdown(f"<p style='color:black; font-weight:bold; text-align:center;'>{movie_title}</p>", unsafe_allow_html=True)
                    st.markdown("<div class='stSpacing'></div>", unsafe_allow_html=True)
    
    # Display the time taken
    elapsed_time = time.time() - start_time
    st.markdown(f"<div class='time-display'>✨ Recommendations ready in {elapsed_time:.1f} seconds</div>", unsafe_allow_html=True)