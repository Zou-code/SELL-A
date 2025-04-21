# school:JXNU
# author:zouzhou
# createTime: 2024/10/2 15:44
import json
import subprocess

from config import Config
import time
from openai import OpenAI
from approach.retrieval import Retrieval
from prompt.prompt_react.prompt_agent import prompt_React
from prompt.prompt_react.prompt_result_parse import prompt_result_parse
from prompt.prompt_react.prompt_calling_code import prompt_calling_code
from util.llm_util import LLM_util
from util.code_util import CodeUtil
from util.log import Logger
import os
import pandas as pd
import re
import sys
import time


# TODO ①加上log的配置
# TODO ②写一个函数，用于拼凑API的描述文档
# TODO ③改写prompt，明确每一步的输出是什么
# TODO ④思考清楚，怎么调用代码，是通过代码的控制呢，还是让模型生成API的调用代码？
# TODO ⑤需要再 写一个Prompt，让模型从输出的json数据中提取关键的信息
# TODO ⑥怎么结束下来？怎么才能让模型认为任务已经完成了，结束下来？

# TODO ⑦后面再考虑，是否可以在生成调用代码的同时，让其同时对json数据进行处理，返回和request相关的信息


class ReActAgent:

    def __init__(self):
        self.model_name = Config.react_model
        self.model = LLM_util()
        self.retrieval = Retrieval()
        # 获取当前时间并格式化
        current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        # CodeUtil.configure_logging('../logs/log_ReAct')
        sys.stdout = Logger(f'../logs/log_ReAct/log_{current_time}')
        print('你好')
        self.max_turns = Config.react_max_turn

    def get_alternative_tools(self, requirement):
        """
        根据用户输入的需求，进行相似度匹配，获得备用的工具，并返回
        :param requirement:
        :return: 一个列表，包含备用的工具  [ {"tool_name":"", "API_list":[{"API_name":"",...},{"API_name":"", ...} ] } ]
        """
        df_possible_tools = self.retrieval.tool_retrieval(requirement)
        df_apis = pd.read_csv(Config.api_path)
        tool_list = list()  # 最终返回的应该是一个list，其中包括多个工具的字典
        for _, row_tool in df_possible_tools.iterrows():
            tool_dict = dict()
            tool_name = row_tool['tool_name']
            tool_dict['tool_name'] = tool_name
            # 根据工具名，查询该工具的api
            df_api = df_apis[df_apis['tool_name'] == tool_name]
            API_list = list()  # 一个工具下应该有一个列表，其中包含多个api
            for _, row_api in df_api.iterrows():
                API_dict = dict()  # 一个api应该是一个字典,其中有多个属性 ，包括api_name,api_description,api_parameters
                API_dict['api_name'] = row_api['api_name']
                API_dict['api_description'] = row_api['api_description']
                API_dict['useage_scenario'] = row_api['scenario']
                API_dict['calling_dependency'] = row_api['calling_dependency']
                API_dict['required_parameters'] = row_api['required_parameters']
                API_list.append(API_dict)
            tool_dict['API_list'] = API_list
            tool_list.append(tool_dict)
        return tool_list

    def get_tool_desc(self, alternative_tools: list):
        tool_desc = ''
        for tool in alternative_tools:
            tool_name = tool.get('tool_name')
            API_list = tool.get('API_list')
            for API in API_list:
                API_name = API.get('api_name')
                API_description = API.get('api_description')
                usage_scenario = API.get('useage_scenario')
                calling_dependency = API.get('calling_dependency')
                required_parameters = API.get('required_parameters')
                tool_desc = tool_desc + f'''\
tool name:{tool_name}
API name:{API_name}
API description:{API_description}
usage scenario:{usage_scenario}
API calling dependency:{calling_dependency}
required_parameters:{required_parameters}

'''
        return tool_desc

    def result_extract_from_json(self, query, json_data):
        """
        根据query和response，调用LLM，从response中提取关键信息
        :param query: 即每次循环的thought
        :param json_data: API调用后的json数据
        :return:
        """
        # TODO：需要对json数据进行判断，如果超出token需要处理
        num_tokens = LLM_util.num_tokens_from_prompt(json_data)
        if num_tokens > 8000:
            json_tokens = LLM_util.get_top_k_tokens(json_data, 6000)
            response = LLM_util.tokens_to_text(json_tokens)
        prompt = prompt_result_parse(query, json_data)
        result = self.model.model_deepseek_coder(prompt)
        return result

    def call_llm(self, prompt):
        openai_api_key = Config.openai_api_key
        client = OpenAI(api_key=openai_api_key, base_url="https://openkey.cloud/v1")
        message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        while True:
            try:
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=message,
                    temperature=0,
                    stop=["Observation:"]
                )
                # return response.choices[0].message['content']
                return response.choices[0].message.content
            except Exception as e:
                print(e)
                time.sleep(1)

    def parse_action(self, text):
        # 使用正则表达式提取Final Answer
        final_answer_match = re.search(r'Final Answer:(.*?)(?=$)', text, re.DOTALL)
        if final_answer_match:
            final_answer = final_answer_match.group(1).strip()
            return final_answer

        # 使用正则表达式提取Thought
        thought_match = re.search(r'Thought:(.*?)(?=Action:|$)', text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None

        # 使用正则表达式提取Action
        action_match = re.search(r'Action:(.*?)(?=Action Input:|$)', text, re.DOTALL)
        action = action_match.group(1).strip() if action_match else None

        # 使用正则表达式提取Action Input
        action_input_match = re.search(r'Action Input:(.*?)(?=$)', text, re.DOTALL)
        action_input = action_input_match.group(1).strip() if action_input_match else None

        # 直接返回提取的内容
        return thought, action, action_input

    def calling_code_generator(self, tool_name, API_name, action_input):
        """
        根据选择的tool_name和API_name，调用代码生成器，生成代码
        :param action_input:
        :param tool_name:
        :param API_name:
        :return:
        """
        # 从库中查找API的信息
        df_apis = pd.read_csv(Config.api_path)
        API_doc = ''

        for _, row_api in df_apis.iterrows():
            if (row_api['tool_name'] == tool_name) and (row_api['api_name'] == API_name):
                API_doc = API_doc + f'''\
        API_name: {API_name}
        required_parameters: {row_api['required_parameters']}
        API_request_code:
        ```
        row{row_api['example_calling_code']}
        ```
        actural_parameters: {action_input}
'''
        prompt = prompt_calling_code(API_doc)
        code = self.model.model_deepseek_coder(prompt)
        code = re.sub(r'^```json\n|\n```$', '', code)
        code = re.sub(r'^```\n|\n```$', '', code)
        code = re.sub(r'^```python\n|\n```$', '', code)
        return code

    def agent(self, query):
        token_sum = 0
        turn_count = 1
        # 先进行相似度检索，获取可选的tools
        alternative_tools = self.get_alternative_tools(query)
        # 根据可选的tools，获取工具的描述
        tool_desc = self.get_tool_desc(alternative_tools)
        print(f'\nalternative_tools:{tool_desc}')

        history = prompt_React(tool_desc, query)


        while turn_count < self.max_turns:
            print(f'\nLoop:{turn_count}')
            print('\n' + '--' * 10)
            token_sum += self.model.num_tokens_from_prompt(history)
            response = self.call_llm(history)
            print('\n' + response)
            results = self.parse_action(response)

            # 已经获得了最终答案，可以结束程序，直接返回最终结果
            if len(results) == 1:
                return True, results[0]
            else:
                thought = results[0]
                action = json.loads(results[1])
                action_input = results[2]
                tool_name = action.get('tool_name')
                API_name = action.get('API_name')

                calling_code = self.calling_code_generator(tool_name, API_name, action_input)
                with open('./calling_code.py', 'w', encoding='utf-8') as f:
                    f.write(calling_code)
                    f.flush()
                    f.close()
                # 执行代码，获取结果
                run_result = result = subprocess.run(
                    ["python", "./calling_code.py"],
                    stdout=subprocess.PIPE,  # 捕获标准输出
                    stderr=subprocess.PIPE,  # 捕获标准错误
                    text=True,  # 以文本模式读取输出
                    encoding = 'utf-8'  # 指定编码方式为 UTF-8
                )
                if run_result.stdout:
                    observation = self.result_extract_from_json(thought, run_result.stdout)
                    print('\nObservation:'+observation)
                    print(f"\ntoken_sum: {token_sum}")
                else:
                    observation = run_result.stderr
                    print('\nObservation:' + observation)
                    print(f"\ntoken_sum: {token_sum}")
                # 将结果添加到历史记录中
                history = ''.join([history, response, 'Observation:'+observation])
                current_token = self.model.num_tokens_from_prompt(history)
                print(f'\nCurrent token:{current_token}')
                # 继续循环
                turn_count += 1
        return False, history, token_sum



if __name__ == '__main__':
    requirement = '''A group of friends is organizing a themed movie night and needs a selection\
of movies that fit params like "Adventure" or "Animation." They are looking\
for three films and they would like to know the cast details, user reviews, and plot summaries for the chosen movies.'''
    react = ReActAgent()
    answer = react.agent(requirement)
    if answer[0]:
        print(f'执行成功，最终答案为:\n{answer[1]}')
        print(answer[1])
    else:
        print(f"执行失败，没有在{Config.react_max_turn}轮内找到答案")
        print(f'历史问答记录为:\n{answer[1]}')
    print(answer[-1])
