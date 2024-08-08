import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import base64

# Streamlit App
st.set_page_config(page_title="Movie Select", page_icon=":briefcase:", layout="wide")
st.markdown('<div class="title">Movie Select - Discover Your Movie Mojo</div>', unsafe_allow_html=True)

# Load the movies dictionary and similarity tags
movies_dict = pickle.load(open('notebook/movies_dict.pkl', 'rb'))
movies_dict = pd.DataFrame(movies_dict)
similarity_tags = pickle.load(open('notebook/similarity_tags.pkl', 'rb'))
poster = pickle.load(open('notebook/poster_dict.pkl', 'rb'))
similarity_main_tags = pickle.load(open('notebook/similarity_main_tags.pkl', 'rb'))

# CSS for styling
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://i.postimg.cc/d114JH9w/image-blurr.jpg");
        background-size: cover;
    }}
    .title {{
        font-size: 36px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 2px 2px #000000;
    }}
    .subheader {{
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 1px 1px #000000;
    }}
    .movie-title {{
        font-size: 16px;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 1px 1px #000000;
        padding: 5px;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 5px;
        margin-bottom: 10px;
    }}
    .shaded-box {{
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }}
    .movie-poster {{
        width: 150px; /* Set width in pixels */
        height: 225px; /* Set height in pixels */
        object-fit: cover; /* Ensures the image covers the whole area */
        border-radius: 10px;
    }}
    .movie-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .stButton button {{
        width: 100%;
        background-color: #FF4B4B; /* Set button color */
        color: white;
        font-size: 18px;
        padding: 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }}
    .stButton button:hover {{
        background-color: #FF0000; /* Hover color */
    }}
    .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(0, 0, 0, 0.5);
    }}
    .stSelectbox div[data-baseweb="select"] div[role="combobox"] {{
        background-color: rgba(0, 0, 0, 0.5);
        color: #FFFFFF;
    }}
    .stSelectbox div[data-baseweb="select"] div[role="listbox"] {{
        background-color: rgba(0, 0, 0, 0.5);
        color: #FFFFFF;
    }}
    .stSelectbox div[data-baseweb="select"] div[role="listbox"] ul {{
        background-color: rgba(0, 0, 0, 0.5);
        color: #FFFFFF;
    }}
    .stSelectbox div[data-baseweb="select"] div[role="listbox"] ul li {{
        background-color: rgba(0, 0, 0, 0.5);
        color: #FFFFFF;
    }}
    .vertical-divider {{
        border-left: 2px solid white;
        height: 100%;
        position: absolute;
        left: 50%;
        margin-left: -3px;
        top: 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Function to recommend movies
def recommend(movie, similarity, exclude_movies=set(), num_recommendations=12, sort_by_rating=False, sort_by_revenue=False):
    movie_index = movies_dict[movies_dict['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:112]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_title = movies_dict.iloc[i[0]].title
        if movie_title not in exclude_movies:
            recommended_movies.append(movie_title)
            recommended_movies_poster.append(poster[movie_title])
        if len(recommended_movies) == num_recommendations:
            break
    
    # Combine the movies and their posters into a list of tuples
    combined_list = list(zip(recommended_movies, recommended_movies_poster))
    
    # Sort the combined list by IMDB rating and then by revenue if specified
    if sort_by_rating:
        combined_list = sorted(
            combined_list,
            key=lambda x: movies_dict[movies_dict['title'] == x[0]]['IMDB_Rating'].values[0],
            reverse=(sort_by_rating == "Descending")
        )
    if sort_by_revenue:
        combined_list = sorted(
            combined_list,
            key=lambda x: movies_dict[movies_dict['title'] == x[0]]['revenue'].values[0],
            reverse=(sort_by_revenue == "Descending")
        )
    
    # Separate the sorted movies and posters back into two lists
    if combined_list:
        recommended_movies, recommended_movies_poster = zip(*combined_list)
        return list(recommended_movies), list(recommended_movies_poster)
    else:
        return [], []

# Sidebar for filters
st.sidebar.header("Filter Recommendations")
st.sidebar.markdown(
    """
    <style>
    .sidebar-content {
        position: fixed;
        top: 20%;
        width: 20%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
num_recommendations = st.sidebar.number_input("Number of Recommendations", min_value=12, max_value=51, value=12)
sort_by_rating = st.sidebar.radio("Sort by IMDB Rating", ("None", "Ascending", "Descending"))
release_category = st.sidebar.selectbox("Movie Generation", ["All", "New", "Old", "Classic"])
sort_by_revenue = st.sidebar.radio("Sort by Revenue", ("None", "Ascending", "Descending"))

# Check if the 'Certificate' column exists in the dataframe
if 'Certificate' in movies_dict.columns:
    certificate = st.sidebar.selectbox("Certificate", ["All"] + list(movies_dict['Certificate'].dropna().unique()))
else:
    certificate = "All"

# Filter movies_dict based on sidebar selections
filtered_movies_dict = movies_dict.copy()
if release_category == "New":
    filtered_movies_dict = filtered_movies_dict[filtered_movies_dict['release_year'] >= 2010]
elif release_category == "Old":
    filtered_movies_dict = filtered_movies_dict[(filtered_movies_dict['release_year'] >= 1980) & (filtered_movies_dict['release_year'] < 2010)]
elif release_category == "Classic":
    filtered_movies_dict = filtered_movies_dict[filtered_movies_dict['release_year'] < 1980]

if certificate != "All":
    filtered_movies_dict = filtered_movies_dict[filtered_movies_dict['Certificate'] == certificate]

# Movie selection box and button on the same line
col1, col2 = st.columns([3, 1])
with col1:
    selected_movie_name = st.selectbox('', filtered_movies_dict['title'].values)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add a break to align the button properly
    show_recommendation = st.button('Show Recommendation', use_container_width=True)

if show_recommendation:
    # Get the first set of recommendations
    recommended_movie_names_1, recommended_movie_posters_1 = recommend(
        selected_movie_name, similarity_main_tags, num_recommendations=num_recommendations, sort_by_rating=sort_by_rating, sort_by_revenue=sort_by_revenue
    )

    # Get the second set of recommendations, excluding the first set
    recommended_movie_names_2, recommended_movie_posters_2 = recommend(
        selected_movie_name, similarity_tags, set(recommended_movie_names_1), num_recommendations=num_recommendations, sort_by_rating=sort_by_rating, sort_by_revenue=sort_by_revenue
    )

    col1, col2, col3 = st.columns([1, 0.1, 1])

    with col1:
        st.markdown('<div class="subheader shaded-box">Top Picks for You</div>', unsafe_allow_html=True)
        for i in range(0, len(recommended_movie_names_1), 3):
            row = st.columns(3)
            for j in range(3):
                if i + j < len(recommended_movie_names_1):
                    with row[j]:
                        movie_name = recommended_movie_names_1[i + j]
                        movie_poster = recommended_movie_posters_1[i + j]
                        google_search_url = f"https://www.google.com/search?q={movie_name}+watch+now"
                        st.markdown(f'<div class="movie-container"><a href="{google_search_url}" target="_blank"><img src="{movie_poster}" class="movie-poster"></a><div class="movie-title">{movie_name}</div></div>', unsafe_allow_html=True)
            st.markdown("""---""")

    with col2:
        st.markdown('<div class="vertical-divider"></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="subheader shaded-box">Some Other Suggestions</div>', unsafe_allow_html=True)
        for i in range(0, len(recommended_movie_names_2), 3):
            row = st.columns(3)
            for j in range(3):
                if i + j < len(recommended_movie_names_2):
                    with row[j]:
                        movie_name = recommended_movie_names_2[i + j]
                        movie_poster = recommended_movie_posters_2[i + j]
                        google_search_url = f"https://www.google.com/search?q={movie_name}+watch+now"
                        st.markdown(f'<div class="movie-container"><a href="{google_search_url}" target="_blank"><img src="{movie_poster}" class="movie-poster"></a><div class="movie-title">{movie_name}</div></div>', unsafe_allow_html=True)
            st.markdown("""---""")
