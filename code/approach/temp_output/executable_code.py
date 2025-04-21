import os
import requests

def Genre_List():
    url = "https://advanced-movie-search.p.rapidapi.com/genre/movie/list"
    rapid_api_key = os.getenv('RAPID_API_KEY')

    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")


def Search_By_Genre(with_genres, page):
    url = "https://advanced-movie-search.p.rapidapi.com/discover/movie"
    rapid_api_key = os.getenv('RAPID_API_KEY')
    querystring = {"with_genres": with_genres, "page": page}

    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")


def Get_Detailed_Response(movie_id):
    url = "https://advanced-movie-search.p.rapidapi.com/movies/getdetails"
    rapid_api_key = os.getenv('RAPID_API_KEY')
    querystring = {"movie_id": movie_id}

    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")


def extract_genre_id(genre_list, genre_name):
    for genre in genre_list['genres']:
        if genre['name'] == genre_name:
            return genre['id']
    return None


def select_top_movies(movies, count):
    return movies['results'][:count]


def display_movie_details(movie_details):
    print(f"Title: {movie_details['title']}")
    print(f"Overview: {movie_details['overview']}")
    print(f"Popularity: {movie_details['popularity']}")
    print(f"Vote Average: {movie_details['vote_average']}")
    print(f"Vote Count: {movie_details['vote_count']}")
    print("\n")


if __name__ == '__main__':
    genre_list = Genre_List()
    theme_id = extract_genre_id(genre_list, "Adventure")

    if theme_id is not None:
        movies = Search_By_Genre(theme_id, 1)
        selected_movies = select_top_movies(movies, 3)

        for movie in selected_movies:
            movie_details = Get_Detailed_Response(movie['id'])
            display_movie_details(movie_details)
    else:
        print("Genre not found.")