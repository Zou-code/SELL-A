import requests

def get_genre_ids():
    url = "https://ott-details.p.rapidapi.com/getParams"
    querystring = {"param": "genre"}
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    genres = response.json()
    genre_ids = {genre: idx for idx, genre in enumerate(genres)}
    return genre_ids.get("Adventure"), genre_ids.get("Animation")

def search_movies(genre_id):
    url = "https://ott-details.p.rapidapi.com/advancedsearch"
    querystring = {
        "genre": genre_id,
        "type": "movie",
        "sort": "latest",
        "page": "1"
    }
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()
    return response_data.get("results", [])[:3]  # Get top 3 movies

def get_movie_details(imdbid):
    url = "https://ott-details.p.rapidapi.com/gettitleDetails"
    querystring = {"imdbid": imdbid}
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def get_additional_details(imdbid):
    url = "https://ott-details.p.rapidapi.com/getadditionalDetails"
    querystring = {"imdbid": imdbid}
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def main():
    adventure_id, animation_id = get_genre_ids()
    movies = search_movies(adventure_id) + search_movies(animation_id)
    
    for movie in movies:
        imdbid = movie["imdbid"]
        details = get_movie_details(imdbid)
        additional_details = get_additional_details(imdbid)
        
        print(f"Title: {details['title']}")
        print(f"Plot Summary: {additional_details['plotSummary']}")
        print("Cast Details:")
        for person in additional_details['people']:
            if person['category'] in ['actor', 'actress']:
                print(f"  - {person['peopleid']}: {person.get('characters', 'N/A')}")
        print("User Reviews:")
        for review in additional_details['reviews']:
            print(f"  - {review}")
        print("\n")

if __name__ == "__main__":
    main()