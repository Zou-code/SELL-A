import os
import requests

def Additional_Title_Details(imdbid):
    url = "https://ott-details.p.rapidapi.com/getadditionalDetails"
    rapid_api_key = os.getenv('RAPID_API_KEY')
    querystring = {"imdbid": imdbid}

    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    print(Additional_Title_Details("tt15333594"))