import re
from config import Config
import pandas as pd


class APICaller:

    def API_function_gen(self, API_function_list):
        """
        生成Rapid API的调用代码
        :param API_function_list: 调用API的函数签名,是一个list类型数据
        :return:
        """
        API_caller_code = 'import requests\n'
        for API_function in API_function_list:
            API_function_lines = API_function.split('\n')
            function_signature = API_function_lines[0].strip()

            # 获取函数的参数列表，用于拼凑querystring
            pattern = r'\((.*?)\)'
            match = re.search(pattern, function_signature)
            param_list = ''
            if match:
                param_list = match.group(1)
            key_values = []
            for param in param_list.split(','):
                key = f'"{param.strip()}"'
                value = param.strip()
                query = key + ':' + value
                key_values.append(query)
            key_value_str = ', '.join(key_values)
            query_string = '{' + key_value_str + '}'

            # 从获得的函数中获取不同的关键信息
            tool_name = ''
            API_name = ''
            step_description = ''
            expected_output = ''
            for line in API_function_lines:
                if line.strip().startswith('tool name'):
                    tool_name = line.split(':')[-1].strip()
                elif line.strip().startswith('API name'):
                    API_name = line.split(':')[-1].strip()
                elif line.strip().startswith('The description of This Step'):
                    step_description = line.split(':')[-1].strip()
                elif line.strip().startswith('The expected output'):
                    expected_output = line.split(':')[-1].strip()
            df_tools = pd.read_csv(Config.tool_path)
            df_apis = pd.read_csv(Config.api_path)

            # 获取对应的API的信息
            # df_selected_api = df_apis.loc[df_apis['tool_name'] == tool_name and df_apis['api_name'] == API_name]
            df_selected_api = df_apis.loc[(df_apis['tool_name'] == tool_name) & (df_apis['api_name'] == API_name)]
            response_schema = ''
            endpoint_name = ''
            head = ''  # http 开头的url地址
            for index, row in df_selected_api.iterrows():
                response_schema = row['json_schema']
                endpoint_name = row['endpoint_name']
            df_selected_tool = df_tools.loc[df_tools['tool_name'] == tool_name]

            for index, row in df_selected_tool.iterrows():
                head = row['head']
            head_host = head.strip('https://').strip('http://')
            url = f'{head}/{endpoint_name}'

            call_code = f'''\
{function_signature}
    \'\'\'
    tool name: {tool_name}
    API name: {API_name}
    The description of this Step: {step_description}
    The expected output: {expected_output}
    response schema: 
    {response_schema.strip()}
    \'\'\'
    url = "{url}"
    querystring = {query_string}
    headers = {{
        "x-rapidapi-key": "{Config.Rapid_API_key}",
        "x-rapidapi-host": "{head_host}"
    }}
    response = requests.get(url, headers=headers, params=querystring).json()
    return response '''

            API_caller_code += call_code + '\n\n'
        return API_caller_code






if __name__ == '__main__':
    pseudocode = '''\
def OTT_Details_Advanced_Search(start_year, end_year, min_imdb, max_imdb, genre, language, type, sort, page):
    """
    tool name: OTT Details
    API name: Advanced Search 
    The description of This Step: This function will call the Advanced Search API from the OTT Details tool to find movies that fit the specified genre and other filters.
    The expected output: A list of movies that fit the specified genre and other filters.
    """
#######################################    
def OTT_Details_Title_Details(imdbid):
    """
    tool name: OTT Details
    API name: Title Details
    The description of This Step: This function will call the Title Details API from the OTT Details tool to get detailed information about a specific movie.
    The expected output: Detailed information about a specific movie.
    """
#######################################
def OTT_Details_Additional_Title_Details(imdbid):
    """
    tool name: OTT Details
    API name: Additional Title Details
    The description of This Step: This function will call the Additional Title Details API from the OTT Details tool to get additional details about a specific movie, including reviews, quotes, plot summaries, cast details, and trailer URLs.
    The expected output: Additional details about a specific movie, including reviews, quotes, plot summaries, cast details, and trailer URLs.
    """
#######################################
if __name__ == '__main__':
    """
    Plan description:
    Step1: Use the Advanced Search API from the OTT Details tool to find movies that fit the specified genre and other filters.
    Step2: For each movie found, use the Title Details API from the OTT Details tool to get detailed information about the movie.
    Step3: For each movie found, use the Additional Title Details API from the OTT Details tool to get additional details about the movie, including reviews, quotes, plot summaries, cast details, and trailer URLs.
    """

    # Step1: Use the Advanced Search API from the OTT Details tool to find movies that fit the specified genre and other filters.
    movies = OTT_Details_Advanced_Search(1970,2020,6,7.8,"action","english","movie","latest","1")
    # The movies variable now contains a list of movies that fit the specified genre and other filters.

    for movie in movies:
        # Step2: For each movie found, use the Title Details API from the OTT Details tool to get detailed information about the movie.
        movie_details = OTT_Details_Title_Details(movie['imdbid'])
        # The movie_details variable now contains detailed information about the movie.

        # Step3: For each movie found, use the Additional Title Details API from the OTT Details tool to get additional details about the movie, including reviews, quotes, plot summaries, cast details, and trailer URLs.
        additional_movie_details = OTT_Details_Additional_Title_Details(movie['imdbid'])
        # The additional_movie_details variable now contains additional details about the movie, including reviews, quotes, plot summaries, cast details, and trailer URLs.
'''

    pseudocode = re.sub(r'^```json\n|\n```$', '', pseudocode)
    pseudocode = re.sub(r'^```\n|\n```$', '', pseudocode)
    pseudocode = re.sub(r'^```python\n|\n```$', '', pseudocode)

    api_functions = pseudocode.split('#######################################')[:-1]

    mian_function = pseudocode.split('#######################################')[-1]

    caller = APICaller()
    code = caller.API_function_gen(api_functions)
    print(code)
