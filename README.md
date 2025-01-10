# 🎥 Movie Recommendation App

Welcome to the **Movie Recommendation App**! This project is a Streamlit-based web application that allows users to search for movies and receive personalized recommendations. The app leverages a vector database powered by **Weaviate** for efficient search and recommendation functionality.

## Features

- **Search Movies**: Look up movies by title, description, or other attributes.
- **Personalized Recommendations**: Get movie recommendations based on similar attributes.
- **Interactive Interface**: An easy-to-use web interface built with Streamlit.
- **Retrieval-Augmented Generation (RAG)**: Provides context-aware recommendations by combining vector database search with generative AI models.

## Live Demo

The application is live and available at:
[Movie Recommendation App](https://movie-recommendation-app-hqdkeryw5pq6k7tb4fgcpt.streamlit.app/)

## Technologies Used

- **Python**: Backend programming language.
- **Streamlit**: Framework for building the web interface.
- **Weaviate**: Vector database for storing and querying movie data.
- **OpenAI GPT**: Generative AI model for enhanced text-based recommendations.

## Data Management with Weaviate

The application utilizes Weaviate to store and manage movie-related data, including:

1. **Collections**:
   - **Movies**: Stores movie metadata (e.g., title, description, director, year, rating).
   - **Reviews**: Stores user reviews of movies.
   - **Synopsis**: Contains detailed synopses for each movie.

2. **Data Population**:
   - Data was imported from a CSV file and vectorized into embeddings for efficient querying.
   - Relationships between collections were established, such as linking movies to their reviews and synopses.

3. **Search and Recommendations**:
   - **Hybrid Search**: Combines semantic (meaning-based) search with exact matching to enhance retrieval accuracy.
   - **RAG Integration**: Combines vector search results with OpenAI GPT to generate personalized recommendations based on user inputs.

---

Enjoy the app, and happy movie searching and recommending!

