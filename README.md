
# Movie Select - Discover Your Movie Mojo

Welcome to "Movie Select - Discover Your Movie Mojo"! This Streamlit application helps you discover new movies based on your favorite selections. Customize your recommendations by various filters and enjoy a tailored movie-watching experience.

- **Check out the Application: ** [Movie Select](https://huggingface.co/spaces/Shubham235/MovieSelect)

## Features

- **Personalized Recommendations:** Select your favorite movie and get personalized recommendations.
- **Filter Options:** Refine your recommendations by the number of recommendations, IMDB rating, release category, and revenue.
- **User-Friendly Interface:** A visually appealing and intuitive interface to make your movie discovery journey seamless.

## Dataset

This application uses a fresh dataset created by [Shubham Chandra](https://www.kaggle.com/datasets/shubhamchandra235/imdb-and-tmdb-movie-metadata-big-dataset-1m).

**Title:** IMDB & TMDB Movie Metadata Big Dataset (>1M)

**Subtitle:** A Comprehensive Dataset Featuring Detailed Metadata of Movies (IMDB, TMDB). Over 1M Rows & 42 Features: Metadata, Ratings, Genres, Cast, Crew, Sentiment Analysis and many more…

### Detailed Description:

**Overview:** This comprehensive dataset was created by me by merging the extensive film data available from both IMDB and TMDB API's and numerous datasets, offering a rich resource for movie enthusiasts, data scientists, and researchers. With over 1 million rows and 42 detailed features, this dataset provides in-depth information about a wide variety of movies, spanning different genres, periods, and production backgrounds.

**File Information:**

- **File Size:** ≈ 1GB
- **Format:** CSV (Comma-Separated Values)

Some recommendations are also made based on tags from the sentiment analysis results.

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/movie-select.git
   cd movie-select
   ```

2. **Install the Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```sh
   streamlit run app.py
   ```

## Usage

1. **Start the App:** Open your terminal and navigate to the project directory. Run `streamlit run app.py` to start the application.
2. **Select a Movie:** Use the dropdown to select your favorite movie.
3. **Filter Recommendations:** Use the sidebar to apply various filters such as the number of recommendations, IMDB rating, release category, and revenue.
4. **View Recommendations:** Click the "Show Recommendation" button to see your personalized movie recommendations.

## Project Structure

- `app.py`: The main Streamlit application file.
- `notebook/`
  - `movies_dict.pkl`: A pickle file containing the movies dictionary.
  - `similarity_tags.pkl`: A pickle file containing similarity tags.
  - `poster_dict.pkl`: A pickle file containing movie posters.
  - `similarity_main_tags.pkl`: A pickle file containing main similarity tags.
  - `data/image.jpg`: The background image for the app.

## Background Image

The background image is set using a URL in the CSS. If you prefer to use a local image, you can modify the CSS accordingly.

## Dependencies

- Streamlit
- Pandas
- Pickle
- PIL (Pillow)
- Base64
- sklearns

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the awesome framework.
- [PostImg](https://postimg.cc/) for hosting the background image.

---

Enjoy discovering your movie mojo with "Movie Select"! If you have any questions or feedback, feel free to reach out.

**Happy Movie Watching!**
