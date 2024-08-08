import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the movies dictionary and similarity tags
movies_dict = pickle.load(open('notebook/movies_dict.pkl', 'rb'))
movies_dict = pd.DataFrame(movies_dict)
similarity_tags = pickle.load(open('notebook/similarity_tags.pkl', 'rb'))
poster = pickle.load(open('notebook/poster_dict.pkl', 'rb'))
similarity_main_tags = pickle.load(open('notebook/similarity_main_tags.pkl', 'rb'))

# CSS for background image and styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-photo/clapperboard-remote-control-space_23-2147681385.jpg");
        background-size: cover;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 2px 2px #000000;
    }
    .subheader {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 1px 1px #000000;
    }
    .movie-title {
        font-size: 16px;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 1px 1px #000000;
        padding: 5px;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .shaded-box {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .movie-poster {
        width: 100%;
        height: auto; /* Maintain aspect ratio */
        object-fit: cover; /* Ensures the image covers the whole area */
        border-radius: 10px;
    }
    .movie-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title shaded-box">Movie Select - Discover Your Movie Mojo</div>', unsafe_allow_html=True)

# Function to recommend movies
def recommend(movie, similarity, exclude_movies=set()):
    movie_index = movies_dict[movies_dict['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:101]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_title = movies_dict.iloc[i[0]].title
        if movie_title not in exclude_movies:
            recommended_movies.append(movie_title)
            recommended_movies_poster.append(poster[movie_title])
        if len(recommended_movies) == 10:  # Limit to 10 recommendations
            break
    
    # Combine the movies and their posters into a list of tuples
    combined_list = list(zip(recommended_movies, recommended_movies_poster))
    
    # Sort the combined list by IMDB rating and then by revenue
    combined_list = sorted(
        combined_list,
        key=lambda x: (
            movies_dict[movies_dict['title'] == x[0]]['IMDB_Rating'].values[0],
            movies_dict[movies_dict['title'] == x[0]]['revenue'].values[0]
        ),
        reverse=True
    )
    
    # Separate the sorted movies and posters back into two lists
    recommended_movies, recommended_movies_poster = zip(*combined_list)
    
    return list(recommended_movies), list(recommended_movies_poster)

selected_movie_name = st.selectbox('Select your Favorite Movie', movies_dict['title'].values)

if st.button('Show Recommendation'):
    # Get the first set of recommendations
    recommended_movie_names_1, recommended_movie_posters_1 = recommend(selected_movie_name, similarity_main_tags)

    st.markdown('<div class="subheader shaded-box">Recommendations</div>', unsafe_allow_html=True)
    
    # Display first 5 recommendations
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            movie_name = recommended_movie_names_1[i]
            movie_poster = recommended_movie_posters_1[i]
            google_search_url = f"https://www.google.com/search?q={movie_name}+watch+now"
            col.markdown(f'<div class="movie-container"><div class="movie-title">{movie_name}</div><a href="{google_search_url}" target="_blank"><img src="{movie_poster}" class="movie-poster"></a></div>', unsafe_allow_html=True)

    # Display next 5 recommendations
    col6, col7, col8, col9, col10 = st.columns(5)
    for i, col in enumerate([col6, col7, col8, col9, col10], start=5):
        with col:
            movie_name = recommended_movie_names_1[i]
            movie_poster = recommended_movie_posters_1[i]
            google_search_url = f"https://www.google.com/search?q={movie_name}+watch+now"
            col.markdown(f'<div class="movie-container"><div class="movie-title">{movie_name}</div><a href="{google_search_url}" target="_blank"><img src="{movie_poster}" class="movie-poster"></a></div>', unsafe_allow_html=True)

    # Get the second set of recommendations, excluding the first set
    recommended_movie_names_2, recommended_movie_posters_2 = recommend(selected_movie_name, similarity_tags, set(recommended_movie_names_1))

    st.markdown('<div class="subheader shaded-box">Some other Suggestions </div>', unsafe_allow_html=True)

    # Display first 5 suggestions
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            movie_name = recommended_movie_names_2[i]
            movie_poster = recommended_movie_posters_2[i]
            google_search_url = f"https://www.google.com/search?q={movie_name}+watch+now"
            col.markdown(f'<div class="movie-container"><div class="movie-title">{movie_name}</div><a href="{google_search_url}" target="_blank"><img src="{movie_poster}" class="movie-poster"></a></div>', unsafe_allow_html=True)

    # Display next 5 suggestions
    col6, col7, col8, col9, col10 = st.columns(5)
    for i, col in enumerate([col6, col7, col8, col9, col10], start=5):
        with col:
            movie_name = recommended_movie_names_2[i]
            movie_poster = recommended_movie_posters_2[i]
            google_search_url = f"https://www.google.com/search?q={movie_name}+watch+now"
            col.markdown(f'<div class="movie-container"><div class="movie-title">{movie_name}</div><a href="{google_search_url}" target="_blank"><img src="{movie_poster}" class="movie-poster"></a></div>', unsafe_allow_html=True)
