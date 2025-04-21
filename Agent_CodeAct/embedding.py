# school:JXNU
# author:zouzhou
# createTime: 2024/10/9 19:01

import pandas as pd
from util.llm_util import LLM_util
from tqdm import tqdm

def embedding():
    """
    对API的描述进行 embedding
    :return:
    """

    df_apis = pd.read_csv("./apis.csv", encoding="utf-8")
    tqdm.pandas()
    llm = LLM_util()
    df_apis["API_vector"] = df_apis["api_description"].progress_apply(lambda x: llm.model_embedding(x))

    df_apis.to_csv("./apis.csv", index=False, encoding="utf-8")


if __name__ == '__main__':
    embedding()