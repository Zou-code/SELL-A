# school:JXNU
# author:zouzhou
# createTime: 2024/5/29 17:14
import os

import openai
import pandas as pd
from tqdm import tqdm


"""将数据集中的api描述变成向量并保存到csv文件中"""

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = 'text-embedding-3-small'

def get_embedding(input):
    """使用OpenAI 将文本向量化"""
    embedding = client.embeddings.create(
        model=model,
        input=input,
        encoding_format='float'
    )
    print(type(embedding))
    return embedding.data[0].embedding

if __name__ == '__main__':
    df = pd.read_csv('./api_data.csv')
    df_new = pd.DataFrame(columns=['api_name', 'api_description', 'required_parameters','method', 'tool_name', 'head', 'embedding'])
    for _,row in tqdm(df.iterrows()):
        # print(row['api_description'])
        row['embedding'] = get_embedding(row['api_description'])
        # df_new = pd.concat(df_new,row,ignore_index=True)
        df_new = df_new._append(row,ignore_index=True)
    df_new.to_csv('./new_api_data.csv')

