import requests

def Search_By_Genre(with_genres, page):
    """
    Retrieve a list of movies and TV shows filtered by genre, including details like title, release date, and ratings.
    :param with_genres: A string representing the genre IDs to filter by, example: 80.
    :param page: A number indicating the page number of results to fetch, example: 1.
    :response_schema:
    ```json
    {
      "type": "object",
      "properties": {
        "page": {
          "type": "integer",
          "description": "The current page number of the results."
        },
        "results": {
          "type": "array",
          "description": "List of movie or TV show results.",
          "items": {
            "type": "object",
            "properties": {
              "adult": {
                "type": "boolean",
                "description": "Indicates if the content is for adults only."
              },
              "backdrop_path": {
                "type": "string",
                "description": "URL path to the backdrop image."
              },
              "genre_ids": {
                "type": "array",
                "description": "List of genre IDs associated with the content.",
                "items": {
                  "type": "integer"
                }
              },
              "id": {
                "type": "integer",
                "description": "Unique identifier for the content."
              },
              "original_language": {
                "type": "string",
                "description": "Original language of the content."
              },
              "original_title": {
                "type": "string",
                "description": "Original title of the content."
              },
              "overview": {
                "type": "string",
                "description": "Brief summary of the content."
              },
              "popularity": {
                "type": "number",
                "description": "Popularity score of the content."
              },
              "poster_path": {
                "type": "string",
                "description": "URL path to the poster image."
              },
              "release_date": {
                "type": "string",
                "description": "Release date of the content."
              },
              "title": {
                "type": "string",
                "description": "Title of the content."
              },
              "video": {
                "type": "boolean",
                "description": "Indicates if there is a video available for the content."
              },
              "vote_average": {
                "type": "number",
                "description": "Average rating of the content."
              },
              "vote_count": {
                "type": "integer",
                "description": "Number of votes for the content."
              }
            },
            "required": ["adult", "backdrop_path", "genre_ids", "id", "original_language", "original_title", "overview", "popularity", "poster_path", "release_date", "title", "video", "vote_average", "vote_count"]
          }
        },
        "total_pages": {
          "type": "integer",
          "description": "Total number of pages available."
        },
        "total_results": {
          "type": "integer",
          "description": "Total number of results available."
        }
      },
      "required": ["page", "results", "total_pages", "total_results"]
    }
    ```
    """
    url = "https://advanced-movie-search.p.rapidapi.com/discover/movie"
    querystring = {"with_genres": with_genres, "page": page}
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def Get_Detailed_Response(movie_id):
    """
    Retrieve comprehensive details about a specific movie, including budget, revenue, genres, and more.
    :param movie_id: Number - The unique identifier for the movie.
    :response_schema:
    ```json
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "properties": {
        "adult": {
          "type": "boolean"
        },
        "backdrop_path": {
          "type": "string"
        },
        "belongs_to_collection": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "poster_path": {
              "type": "string"
            },
            "backdrop_path": {
              "type": "string"
            }
          },
          "required": ["id", "name", "poster_path", "backdrop_path"]
        },
        "budget": {
          "type": "integer"
        },
        "genres": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer"
              },
              "name": {
                "type": "string"
              }
            },
            "required": ["id", "name"]
          }
        },
        "homepage": {
          "type": "string"
        },
        "id": {
          "type": "integer"
        },
        "imdb_id": {
          "type": "string"
        },
        "original_language": {
          "type": "string"
        },
        "original_title": {
          "type": "string"
        },
        "overview": {
          "type": "string"
        },
        "popularity": {
          "type": "number"
        },
        "poster_path": {
          "type": "string"
        },
        "production_companies": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer"
              },
              "logo_path": {
                "type": "string"
              },
              "name": {
                "type": "string"
              },
              "origin_country": {
                "type": "string"
              }
            },
            "required": ["id", "logo_path", "name", "origin_country"]
          }
        },
        "production_countries": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "iso_3166_1": {
                "type": "string"
              },
              "name": {
                "type": "string"
              }
            },
            "required": ["iso_3166_1", "name"]
          }
        },
        "release_date": {
          "type": "string"
        },
        "revenue": {
          "type": "integer"
        },
        "runtime": {
          "type": "integer"
        },
        "spoken_languages": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "english_name": {
                "type": "string"
              },
              "iso_639_1": {
                "type": "string"
              },
              "name": {
                "type": "string"
              }
            },
            "required": ["english_name", "iso_639_1", "name"]
          }
        },
        "status": {
          "type": "string"
        },
        "tagline": {
          "type": "string"
        },
        "title": {
          "type": "string"
        },
        "video": {
          "type": "boolean"
        },
        "vote_average": {
          "type": "number"
        },
        "vote_count": {
          "type": "integer"
        }
      },
      "required": [
        "adult", "backdrop_path", "belongs_to_collection", "budget", "genres", "homepage", "id", "imdb_id", "original_language", "original_title", "overview", "popularity", "poster_path", "production_companies", "production_countries", "release_date", "revenue", "runtime", "spoken_languages", "status", "tagline", "title", "video", "vote_average", "vote_count"
      ]
    }
    ```
    """
    url = "https://advanced-movie-search.p.rapidapi.com/movies/getdetails"
    querystring = {"movie_id": movie_id}
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def Title_Details(imdbid):
    """
    Retrieve comprehensive data on movies, including genre, image URLs, IMDb ID, rating, languages, release year, runtime, and streaming availability.
    :param imdbid: String - The IMDb ID of the movie, required to fetch detailed information.
    :response_schema:
    ```json
    {
      "type": "object",
      "properties": {
        "genre": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of genres associated with the movie."
        },
        "imageurl": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "URLs of images associated with the movie."
        },
        "imdbid": {
          "type": "string",
          "description": "Unique IMDb ID of the movie."
        },
        "imdbrating": {
          "type": "number",
          "description": "IMDb rating of the movie."
        },
        "language": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of languages in which the movie is available."
        },
        "released": {
          "type": "integer",
          "description": "Year the movie was released."
        },
        "runtime": {
          "type": "string",
          "description": "Duration of the movie."
        },
        "streamingAvailability": {
          "type": "object",
          "properties": {
            "country": {
              "type": "object",
              "properties": {
                "US": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "platform": {
                        "type": "string",
                        "description": "Name of the streaming platform."
                      },
                      "url": {
                        "type": "string",
                        "description": "URL to watch the movie on the platform."
                      }
                    },
                    "required": ["platform", "url"]
                  },
                  "description": "List of streaming platforms and URLs where the movie is available in the US."
                }
              }
            }
          },
          "required": ["country"]
        },
        "synopsis": {
          "type": "string",
          "description": "Brief summary of the movie's plot."
        },
        "title": {
          "type": "string",
          "description": "Title of the movie."
        },
        "type": {
          "type": "string",
          "description": "Type of the media (e.g., 'movie')."
        }
      },
      "required": ["genre", "imageurl", "imdbid", "imdbrating", "language", "released", "runtime", "streamingAvailability", "synopsis", "title", "type"]
    }
    ```
    """
    url = "https://ott-details.p.rapidapi.com/gettitleDetails"
    querystring = {"imdbid": imdbid}
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def Additional_Title_Details(imdbid):
    """
    Retrieve comprehensive details about a movie or TV show, including reviews, quotes, plot summaries, cast details, and trailer URLs.
    :param imdbid: String - The IMDb ID of the movie or TV show, required to fetch the detailed information.
    :response_schema:
    ```json
    {
      "type": "object",
      "properties": {
        "imdbid": {
          "type": "string",
          "description": "Unique identifier for the movie on IMDb."
        },
        "numVotes": {
          "type": "integer",
          "description": "Number of votes the movie has received on IMDb."
        },
        "people": {
          "type": "array",
          "description": "List of people involved in the movie.",
          "items": {
            "type": "object",
            "properties": {
              "category": {
                "type": "string",
                "description": "Category of the person (e.g., actor, actress, director, writer, producer)."
              },
              "characters": {
                "type": ["array", "null"],
                "description": "List of characters played by the person, if applicable.",
                "items": {
                  "type": "string"
                }
              },
              "job": {
                "type": ["string", "null"],
                "description": "Job description of the person, if applicable."
              },
              "peopleid": {
                "type": "string",
                "description": "Unique identifier for the person on IMDb."
              }
            },
            "required": ["category", "peopleid"]
          }
        },
        "plotSummary": {
          "type": "string",
          "description": "Summary of the movie's plot."
        },
        "quotes": {
          "type": "array",
          "description": "List of notable quotes from the movie.",
          "items": {
            "type": "string"
          }
        },
        "reviews": {
          "type": "array",
          "description": "List of reviews for the movie.",
          "items": {
            "type": "string"
          }
        },
        "title": {
          "type": "string",
          "description": "Title of the movie."
        },
        "trailerUrl": {
          "type": "array",
          "description": "List of URLs for the movie's trailers on IMDb.",
          "items": {
            "type": "string"
          }
        }
      },
      "required": ["imdbid", "numVotes", "people", "plotSummary", "quotes", "reviews", "title", "trailerUrl"]
    }
    ```
    """
    url = "https://ott-details.p.rapidapi.com/getadditionalDetails"
    querystring = {"imdbid": imdbid}
    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()