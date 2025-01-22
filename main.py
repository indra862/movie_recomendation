# import streamlit as st
# import pickle
# import pandas as pd

# def recomended_movie_list(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = simi[movie_index]
#     movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

#     recom = []
#     for i in movie_list:
#         recom.append(movies.iloc[i[0]].title)
#     return recom



# simi = pickle.load(open('simi.pkl','rb'))

# movies_list = pickle.load(open('movies.pkl','rb'))
# movies = movies_list['title'].values

# st.title('Movie Recomendation Web App')
# movie_selected = st.selectbox(
#     'Select The Movies you like',movies
# )

# if st.button ('Recommend'):
#     recomendations = recomended_movie_list(movie_selected)
#     for i in recomendations:
#         st.write(i)







# import streamlit as st
# import pickle
# import pandas as pd

# # Load data
# movies_list = pickle.load(open('movies.pkl', 'rb'))
# similarity_matrix = pickle.load(open('simi.pkl', 'rb'))

# # Ensure movies is a DataFrame
# movies = pd.DataFrame(movies_list)

# def recommend_movie_list(movie):
#     try:
#         movie_index = movies[movies['title'] == movie].index[0]
#         distances = similarity_matrix[movie_index]
#         movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#         recommendations = []
#         for i in movie_list:
#             recommendations.append(movies.iloc[i[0]].title)
#         return recommendations
#     except IndexError:
#         return ["Movie not found. Please try another."]

# st.title('Movie Recommendation Web App')

# # Dropdown for movie selection
# movie_selected = st.selectbox(
#     'Select a movie you like:',
#     movies['title'].values
# )

# # Recommend button
# if st.button('Recommend'):
#     recommendations = recommend_movie_list(movie_selected)
#     st.subheader('Recommended Movies:')
#     for rec in recommendations:
#         st.write(rec)




import streamlit as st
import pickle
import pandas as pd
import requests
import json
import os

# Load the API key
with open(r"C:\Users\Dell\Desktop\projects\movie_recomendation\.kaggle\kaggle.json", 'r') as f:
    kaggle_api = json.load(f)

api_key = kaggle_api['key']
username = kaggle_api['username']

os.environ['KAGGLE_USERNAME'] = username
os.environ['KAGGLE_KEY'] = api_key

# print(f"Kaggle API key: {api_key}")
# print(f"Kaggle username: {username}")

# TMDb API key
API_KEY = api_key  # Replace with your actual API key
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500/"  # Adjust size as needed

# Load data
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity_matrix = pickle.load(open('simi.pkl', 'rb'))
# Ensure movies is a DataFrame
movies = pd.DataFrame(movies_list)
def get_movie_poster(movie_title):
    """Fetch movie poster URL from TMDb API."""
    try:
        response = requests.get(f"{BASE_URL}/search/movie", params={
            "api_key": api_key,
            "query": movie_title
        })
        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"{IMAGE_BASE_URL}{poster_path}"
        return None
    except Exception as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return None

def recommend_movie_list(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity_matrix[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommendations = []
        posters = []
        for i in movie_list:
            recommended_movie = movies.iloc[i[0]].title
            recommendations.append(recommended_movie)
            posters.append(get_movie_poster(recommended_movie))
        return recommendations, posters
    except IndexError:
        return ["Movie not found. Please try another."], []

st.title('Movie Recommendation Web App')

# Dropdown for movie selection
movie_selected = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    recommendations, posters = recommend_movie_list(movie_selected)
    st.subheader('Recommended Movies:')
    for rec, poster in zip(recommendations, posters):
        st.write(rec)
        if poster:
            st.image(poster, width=150)  # Display the poster
        else:
            st.write("Poster not available.")


