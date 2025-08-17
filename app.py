import pickle
import streamlit as st
import requests

st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 0.5em 1.5em;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #ff2e2e;
    }
    .stSelectbox>div>div>div {
        font-size: 16px;
    }
    .movie-title {
        font-weight: bold;
        font-size: 16px;
        margin-top: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.markdown("<h1 style='text-align: center; color: #333;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Get similar movie suggestions based on your favorites!</p>", unsafe_allow_html=True)

movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_column_width='always')
            st.markdown(f"<div class='movie-title'>{recommended_movie_names[i]}</div>", unsafe_allow_html=True)
