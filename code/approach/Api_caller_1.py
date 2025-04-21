from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from self_discovery import SelfDiscovery
import os
import re
import pandas as pd

"""
利用LLM生成调用rapid api的代码
"""

class APICaller:
    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.mode_gpt35 = ChatOpenAI(
            model='gpt-3.5-turbo',
            openai_api_key=openai_api_key,
            temperature=0
        )
        self.model_gpt4 = ChatOpenAI(
            model='gpt-4',
            openai_api_key=openai_api_key,
            temperature=0.1
        )
        self.model_deepseek = ChatOpenAI(
            model='deepseek-chat',
            openai_api_key='sk-08164a083199467595e5d797f3a88b7f',
            base_url='https://api.deepseek.com'
        )

    def get_plan(self,framework:SelfDiscovery,task_description):
        """
        调用SelfDiscovery类的方法，获得给定用户需求的API调用链描述信息
        :param framework: SelfDiscovery类
        :param task_description: 用户需求任务的描述
        :return:一个list，其中每个元素都是一个二元组，（api_name, step_description
        """
        return framework.self_discovery_framework(task_description)

    def get_steps(reasoning_steps) -> list:
        """
        对推理步骤的字符串进行拆分，得到每一个步骤调用的api名字及其步骤描述
        :param reasoning_steps: 字符串类型的推理步骤
        :return: 一个列表，列表里面每个元素是一个二元组(api_name,step_description)
        """
        steps = reasoning_steps.split('########################')
        apis = []
        for step in steps:
            step = step.strip()
            step_lines = step.split('\n')
            pattern = r'^\d+\.\s*'
            step_desc = re.sub(pattern, '', step_lines[0]).strip()
            api_name = step_lines[1].strip().split(':')[-1].strip()
            print(step_desc)
            print(api_name + '\n')
            apis.append((api_name, step_desc))
        return apis

    def get_api_caller_code(self, api_name, step_description, task_description,context:list=None):
        """
        调用LLM获得调用API的代码
        :param task_description: 任务描述
        :param api_name: 被调用的api
        :param step_description: 这一步骤的描述
        :param context: 上下文，因为这一步输入的参数可能会用到前面步骤的输出
        :return: api请求调用的Python代码
        """

        # 根据api_name 从api库中查找对应的行
        # TODO 这里的查找是有点问题的，因为api_name 可能不是唯一的，后续需要考虑加入新的
        df = pd.read_csv('../new_api_data.csv')
        df_new = df.loc[df['api_name'] == api_name]
        api_description = ''
        api_required_parameters = ''
        api_method_type = ''
        api_url = ''
        for _,row in df_new.iterrows():
            api_description = row['api_description']
            api_required_parameters = row['required_parameters']
            api_method_type = row['method']
            api_url = row['head']

        code_example = '''import requests

url = "https://ott-details.p.rapidapi.com/advancedsearch"

querystring = {"start_year":"1970","end_year":"2020","min_imdb":"6","max_imdb":"7.8","genre":"action","language":"english","type":"movie","sort":"latest","page":"1"}

headers = {
	"x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
	"x-rapidapi-host": "ott-details.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring).json'''

        prompt_template = open("../prompt/APICaller.txt","r").read()

        # prompt_template = (prompt_template.replace('{api_endpoint}',api_name).replace('{method_type}',api_method_type).
        #           replace('{api_description}',api_description).replace('{api_url}',api_url).replace('{parameters}',api_required_parameters).
        #           replace('{task_description}',task_description).replace('{step_description}',step_description).replace('{previous_reasoning_steps}','').
        #           replace('rapidapi_key','887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4'))
        prompt = ChatPromptTemplate.from_template(prompt_template)
        message = prompt.format_messages(
            api_endpoint=api_name,
            method_type=api_method_type,
            api_description=api_description,
            api_url=api_url,
            parameters=api_required_parameters,
            task_description=task_description,
            rapidapi_key='887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4',
            step_description=step_description,
            previous_reasoning_steps=None,
            example=code_example
        )
        api_call_code = self.mode_gpt35.invoke(message).content
        return api_call_code

    def API_code_supp(self):
        function = '''def OTT_Details_Advanced_Search(start_year, end_year, min_imdb, max_imdb, genre, language, type, sort) -> list:
    """
    This step uses the Advanced Search API from OTT Details to search for movies or TV shows based on various parameters such as release year, IMDB rating, genre, language, type, and sorting options.
    The expected output: A list of movies or TV shows that match the specified criteria.
    """
    url = "https://ott-details.p.rapidapi.com/advancedsearch"

    querystring = {"start_year":start_year,"end_year":end_year,"min_imdb":min_imdb,"max_imdb":max_imdb,"genre":genre,"language":language,"type":type,"sort":sort,"page":page}

    headers = {
        "x-rapidapi-key": "887d71b920mshd04c314a5ea867bp15a429jsn1949371722b4",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }

    data = requests.get(url, headers=headers, params=querystring).json()'''
        main_function = '''if __name__ == '__main__':
    """
    Plan description:
    Step1: Identify the streaming services available (Netflix, Prime Video, Disney+).
    Step2: Determine the criteria for family-friendly movies (appropriate content, age ratings).
    Step3: Search for movies that meet the criteria on each streaming service.
    Step4: Compile a list of recommended movies with their streaming links.
    """

    # Step1: Get the list of supported OTT platforms in the desired region
    platforms = OTT_Details_getPlatforms("US")

    # Step2: Define criteria for family-friendly movies
    family_friendly_criteria = {
        "genre": ["Family", "Animation", "Comedy"],
        "language": ["English"],
        "type": "movie",
        "min_imdb": 6.0,
        "max_imdb": 8.0
    }

    # Step3: Search for family-friendly movies on each platform
    recommended_movies = []
    for platform in platforms:
        movies = OTT_Details_Advanced_Search(None, None, family_friendly_criteria["min_imdb"], family_friendly_criteria["max_imdb"], ",".join(family_friendly_criteria["genre"]), family_friendly_criteria["language"], family_friendly_criteria["type"], "highestrated")
        for movie in movies:
            if platform in movie.get("OTT_Platforms", []):
                recommended_movies.append(movie)

    # Step4: Get additional details and streaming links for recommended movies
    for movie in recommended_movies:
        details = OTT_Details_getadditionalDetails(movie["imdb_id"])
        movie.update(details)

    # Output the list of recommended movies with streaming links
    print(recommended_movies)'''

        prompt = open('../prompt/result_parse_2.txt','r',encoding='utf-8').read()
        prompt_template = ChatPromptTemplate.from_template(prompt)
        json_schema = open('../json_schema.txt','r',encoding='utf-8').read()
        message = prompt_template.format_messages(function=function,main_function=main_function,json_schema=json_schema)
        response = self.model_gpt4.invoke(message).content
        print(response)


if __name__ == '__main__':
    caller = APICaller()
    # api_name = 'discover/movie'
    # step_desc = 'First, we need to discover family-friendly movies. We can use the `discover/movie` API to find movies by genre. We can specify genres like "Family", "Animation", "Adventure", etc. to get a list of suitable movies.'
    # task_description = 'My family is planning a movie night and we need some family-friendly movies to watch. Can you recommend some movies suitable for children that are available on streaming services like Netflix, Prime Video, and Disney+? It would be great if you could provide the streaming links for these movies.'
    #
    # code = caller.get_api_caller_code(api_name, step_desc, task_description)
    # print(code)

    caller.API_code_supp()




# chat = ChatOpenAI(model='deepseek-chat',base_url= 'https://api.deepseek.com',openai_api_key='sk-08164a083199467595e5d797f3a88b7f')
# prompt = ChatPromptTemplate.from_template('Hello?')
# chain = prompt | chat
# response = chain.invoke({})
# print(response.content)

