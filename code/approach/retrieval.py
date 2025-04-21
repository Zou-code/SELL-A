# school:JXNU
# author:zouzhou
# createTime: 2024/7/20 16:26
import pandas as pd
from config import Config
from ast import literal_eval
import numpy as np
from util.llm_util import LLM_util
from prompt.prompt_task_plan import prompt_implement


# from openai.embeddings_utils import cosine_similarity

class Retrieval:
    def __init__(self):
        self.llm_util = LLM_util()

    def consine_similarity(self, vec1, vec2):
        """
        计算两个向量的余弦相似度
        :param vec1: 向量1
        :param vec2: 向量2
        :return: 返回余弦相似度
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def tool_retrieval(self, user_requirement, top_k=3):
        """
        从tools.csv中找到和user_requirement 最相似的top k 个tool
        :param top_k: 检索前k个，默认为3
        :param user_requirement: 用户需求
        :return: 返回的是一个dataframe，是top k个最相似的tool
        """

        df_tools = pd.read_csv('../data/tools_react.csv')
        # 将嵌入向量列转换为Numpy数组
        df_tools["embedding"] = df_tools["embedding"].apply(literal_eval).apply(np.array)
        # 获取用户需求的词嵌入表示
        user_requirement_embedding = self.llm_util.model_embedding(user_requirement)
        # 计算user_requirement_embedding嵌入向量与tool base 中每个tool描述的嵌入向量的余弦相似度，并将结果保存子啊similarity列中
        df_tools["similarity"] = df_tools["embedding"].apply(
            lambda x: self.consine_similarity(user_requirement_embedding, x))
        # 根据相似度进行排序，并返回前k个最相似的tool
        df_tools_retrieved = df_tools.sort_values("similarity", ascending=False).head(top_k)

        return df_tools_retrieved


if __name__ == '__main__':
    # 测试是否真的能够找到最相似的tool 描述
    requirement = 'advanced queries like genre'
    tools = Retrieval().tool_retrieval(requirement, top_k=2)
    tools.to_csv('tools_retrieved.csv', index=False)
    # df_tools = pd.read_csv('tools_retrieved.csv')
    # from util.code_util import CodeUtil
    # api_doc = CodeUtil.get_api_doc(df_tools)
    # prompt = prompt_implement("", api_doc , requirement)
    # print(api_doc)
    # print("##########################################################")
    # print(prompt)
