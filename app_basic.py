import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title('Movie Recommendation System')

# Safely open and load the pickled data
try:
    with open('notebook/movies.pkl', 'rb') as file:
        movies_data = pickle.load(file)
        
    # Print the loaded data to debug
    st.write("Data loaded from pickle file:", movies_data)

    # Check if the expected 'title' column exists
    if 'title' in movies_data.columns:
        movies_list = movies_data['title'].values
    else:
        st.error("The 'title' column is not found in the pickle file.")
        movies_list = []

except FileNotFoundError:
    st.error("The pickle file was not found.")
    movies_list = []

except KeyError as e:
    st.error(f"Key error: {e}")
    movies_list = []

except Exception as e:
    st.error(f"An error occurred: {e}")
    movies_list = []

# Create a selectbox for movie titles if the list is not empty
if len(movies_list) > 0:
    option = st.selectbox('Select your Favorite Movie', movies_list)
    # Display the selected option
    st.write('You selected:', option)
else:
    st.write("No movies available to select.")
