import pandas
import pandas as pd
from embedding import Embedding
import re


# def implement_reasoning_structure(task_description):
#     embedding = Embedding()
#     top_similar_api_list = embedding.find_top_similar_texts(task_description, 10)
#     df = pd.read_csv('./new_api_data.csv')
#
#     api_list = ''''''
#     for api, similarity in top_similar_api_list:
#         result = df.loc[df['api_description'] == api]
#         for index, row in result.iterrows():
#             api_list = api_list + 'api_name: ' + row['api_name'] + '\ndescription: ' + row['api_description'] + '\nrequired_parameters:\n' + row['required_parameters'] + '\n\n'
#
#     print(api_list)
#
# query = 'My family is planning a movie night and we need some family-friendly movies to watch. Can you recommend some movies suitable for children that are available on streaming services like Netflix, Prime Video, and Disney+? It would be great if you could provide the streaming links for these movies.'
# implement_reasoning_structure(query)


def get_plan(reasoning_steps) -> list:
    """
    对推理步骤的字符串进行拆分，得到每一个步骤调用的api名字及其步骤描述
    :param reasoning_steps: 字符串类型的推理步骤
    :return: 一个列表，列表里面每个元素是一个二元组(api_name,step_description)
    """
    steps = reasoning_steps.split('########################')
    apis = []
    for step in steps:
        step= step.strip()
        step_lines = step.split('\n')
        pattern = r'^\d+\.\s*'
        step_desc = re.sub(pattern,'',step_lines[0]).strip()
        # step_desc = re.sub(r'^\d+\.', '', step_lines[0]).strip(' ')
        api_name = step_lines[1].strip().split(':')[-1].strip()
        print(step_desc)
        print(api_name+'\n')
        apis.append((api_name,step_desc))
    return apis



# 测试函数
input_string = ''' 1. First, we need to discover family-friendly movies. We can use the `discover/movie` API to find movies by genre. We can specify genres like "Family", "Animation", "Adventure", etc. to get a list of suitable movies.
    API name: discover/movie
    API call: 
    ```
    GET https://advanced-movie-search.p.rapidapi.com/discover/movie?with_genres=Family,Animation,Adventure
    ```
    ########################
2. Next, we can use the `advancedsearch` API to filter these movies based on their release year, IMDb rating, language, and type. We can specify the type as 'movie', language as 'English', and set a minimum IMDb rating to ensure the quality of the movies.
    API name: advancedsearch
    API call: 
    ```
    GET https://ott-details.p.rapidapi.com/advancedsearch?type=movie&language=english&min_imdb=7
    ```
    ########################
3. Once we have a list of movies, we can use the `movies/getdetails` API to get detailed information about each movie. This can help us understand the plot, cast, and other details of the movie.
    API name: movies/getdetails
    API call: 
    ```
    GET https://advanced-movie-search.p.rapidapi.com/movies/getdetails?movie_id={movie_id}
    ```
    ########################
4. To find out which streaming services these movies are available on, we can use the `getPlatforms` API. We can specify the region as 'US' to get a list of supported OTT platforms in the USA.
    API name: getPlatforms
    API call: 
    ```
    GET https://ott-details.p.rapidapi.com/getPlatforms?region=US
    ```
    ########################
5. Finally, we can use the `getadditionalDetails` API to get additional details of the movie such as reviews, plot summary, cast details, quotes, trailer url etc. This can help us make a final decision on which movies to watch.
    API name: getadditionalDetails
    API call: 
    ```
    GET https://ott-details.p.rapidapi.com/getadditionalDetails?imdbid={imdb_id}
    ```'''
get_plan(input_string)

