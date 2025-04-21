import subprocess
from ast import literal_eval

import pandas as pd
from approach.retrieval import Retrieval
from util.llm_util import LLM_util
from util.code_util import CodeUtil
from prompt_codeact import prompt_code_act
from prompt_code_fix import prompt_code_fix
import numpy as np
import logging
import time


class CodeAct:

    def __init__(self):
        self.llm = LLM_util()
        self.top_k = 5
        self.act_loop = 10

        # 获取当前时间并格式化
        current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())

        # 定义日志文件名
        log_filename = f"../logs/log_CodeAct/log_{current_time}.log"

        # 配置日志记录器
        logging.basicConfig(
            level=logging.INFO,  # 设置日志级别
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),  # 文件处理器
                logging.StreamHandler()  # 控制台处理器
            ]
        )

    def consine_similarity(self, vec1, vec2):
        """
        计算两个向量的余弦相似度
        :param vec1: 向量1
        :param vec2: 向量2
        :return: 返回余弦相似度
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def retrieval(self, user_requirement):
        df_apis = pd.read_csv('./apis.csv', encoding='utf-8')
        # 将API描述的嵌入列转换为numpy数组
        df_apis['API_vector'] = df_apis['API_vector'].apply(literal_eval).apply(np.array)
        # 将用户需求转换为词嵌入表示
        user_requirement_vector = self.llm.model_embedding(user_requirement)
        # 计算用户需求的词嵌入和API描述的词嵌入之间的余弦相似度，并将结果存储在新similarity列中
        df_apis['similarity'] = df_apis['API_vector'].apply(lambda x: self.consine_similarity(user_requirement_vector, x))
        # 根据similarity进行排序，并返回前k个最相似的API
        df_apis_retrieved = df_apis.sort_values(by='similarity', ascending=False).head(self.top_k)

        return df_apis_retrieved

    def get_API_list(self, user_requirement):
        # 获取和用户需求最相似的top k个API的dataframe
        df_apis_retrieved = self.retrieval(user_requirement)
        API_list = ''
        for _, row in df_apis_retrieved.iterrows():
            API_name = row['api_name'].strip().replace(' ', '_')
            tool_name = row['tool_name'].strip().replace(' ', '_')
            API_code_path = f'../Tools/{tool_name}/{API_name}.py'
            API_calling_code = ''
            try:
                API_calling_code = open(API_code_path, 'r', encoding='utf-8').read()
            except:
                pass

            API_list = API_list + f'''\
API_name:{row['api_name']}
API_calling_dependency:{row['calling_dependency']}
scenario:{row['scenario']}
API_request_code:{API_calling_code}
'''
        return API_list

    def code_fix(self, error_code, error_message, API_documentation):
        prompt = prompt_code_fix(error_code, error_message, API_documentation)
        # 调用LLM生成修复后的代码
        fixed_code = self.llm.model_gpt4o(prompt)
        fixed_code = CodeUtil.get_code_from_string(fixed_code)
        return fixed_code

    def run_code(self, code):
        """
        将模型生成的可运行代码保存到文件中，并执行
        :param runnable_code:
        :return:
        """
        # 将可运行的代码保存到文件中 ./temp_output/executable_code.py
        with open('./runnable_code.py', 'w', encoding='utf-8') as f:
            f.write(code)
            f.flush()
            f.close()

        result = subprocess.run(
            ["python", "./runnable_code.py"],
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.PIPE,  # 捕获标准错误
            text=True,  # 以文本模式读取输出
            encoding='utf-8'  # 指定编码方式为 UTF-8
        )
        return result

    def main(self, user_requirement):
        search = Retrieval()
        df_possible_tools = search.tool_retrieval(user_requirement)
        tool_API_doc = CodeUtil.get_api_doc_for_codeact(df_possible_tools)

        # API_list = self.get_API_list(user_requirement)
        # 调用LLM生成代码
        prompt = prompt_code_act(user_requirement, tool_API_doc)
        logging.info(f"生成代码的prompt：{prompt}")
        code = self.llm.model_gpt4o(prompt)
        print(code)
        runnable_code = CodeUtil.get_code_from_string(code)
        logging.info(f"生成的代码：{runnable_code}")

        # 执行代码并返回结果
        result = self.run_code(runnable_code)
        if result.stdout:
            logging.info(f"代码执行成功：{result.stdout}")
            return result.stdout
        elif result.stderr or (not result.stdout and not result.stderr):
            for i in range(self.act_loop):
                logging.info(f"代码执行失败：{result.stderr}")
                if result.stderr:
                    message = result.stderr
                else:
                    logging.info(f"输出为空，失败：{result.stderr}")
                    message = "There may be some errors with the code, because the output is empty."
                runnable_code = self.code_fix(runnable_code, result.stderr, tool_API_doc)
                logging.info(f"第{i}次修复后的代码：{runnable_code}")
                # 执行代码并返回结果
                result = self.run_code(runnable_code)
                if result.stdout:
                    logging.info(f"代码执行成功：{result.stdout}")
                    return result.stdout
                elif result.stderr:
                    logging.info(f"代码执行失败：{result.stderr}")
                    continue
        logging.info(f"{self.act_loop}次尝试失败，返回False")
        return "False"


if __name__ == '__main__':
    user_requirement = '''A group of friends is organizing a themed movie night and needs a selection\
of movies that fit params like "Adventure" or "Animation." They are looking\
for three films and they would like to know the cast details, user reviews, and plot summaries for the chosen movies.'''
    codeAct = CodeAct()
    result = codeAct.main(user_requirement)