from config import EMBEDDING_ENCODING, MAX_EMBEDDING_TOKENS, EMBEDDING_MODEL, PINECONE_API_KEY, PINECONE_HOST, PINECONE_INDEX_NAME
import tiktoken
from openai import OpenAI, APIConnectionError
import pandas as pd
import threading
import queue
import streamlit as st
from pinecone import Pinecone

def check_openai_api_key(client):
    try:
        client.models.list()
    except APIConnectionError:
        return False
    else:
        return True

def get_embedding(text, client, model=EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def worker(row_queue, result_list, client):
    while not row_queue.empty():
        row = row_queue.get()
        combined_text = (
            "Question Title: " + row["Question_Title"].strip() + 
            "; Question: " + row["Question_Body"].strip() +
            "; Tags: " + row["Tags"].strip() +
            "; Answer: " + row["Answer_Body"].strip()
        )
        encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
        n_tokens = len(encoding.encode(combined_text))
        if n_tokens <= MAX_EMBEDDING_TOKENS:
            embedding = get_embedding(combined_text, client)
            result_list.append((row["Question_ID"], combined_text, embedding))
        row_queue.task_done()

def vectorize(df, api_key):
    vectorization_columns = ["Question_ID", "Question_Title", "Question_Body", "Tags", "Answer_Body"]
    df = df[vectorization_columns].dropna()

    client = OpenAI(api_key=api_key)
    if not check_openai_api_key(client):
        return df

    row_queue = queue.Queue()
    [row_queue.put(row) for _, row in df.iterrows()]
    results = []

    num_threads = 32 
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(row_queue, results, client))
        thread.start()
        threads.append(thread)

    progress_bar = st.empty()
    while not row_queue.empty():
        progress = (1 - row_queue.qsize() / len(df))
        print(progress)
        progress_bar.progress(progress)


    for thread in threads:
        thread.join()

    progress_bar.progress(100)


    results_df = pd.DataFrame(results, columns=['Question_ID', 'Combined', 'Embeddings'])
    df['Question_ID'] = df['Question_ID'].astype(results_df['Question_ID'].dtype)
    df = pd.merge(df, results_df, on='Question_ID', how='left')

    return df
   


def flush_pinecone_db():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)


    index.delete(delete_all=True)

def upsert_df_to_pinecone(df):
    temp_df = df.dropna()
    pc = Pinecone(api_key=PINECONE_API_KEY)

    temp_df['Embeddings'] = temp_df['Embeddings'].apply(eval)
    
    data_to_insert = [
        (str(idx), vector, {
            "Question_Title": row["Question_Title"],
            "Question_Body": row["Question_Body"],
            "Tags": row["Tags"],
            "Answer_Body": row["Answer_Body"]
        }) 
        for idx, vector, row in zip(temp_df["Question_ID"], temp_df['Embeddings'], temp_df.to_dict(orient="records"))
    ]
    
    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
    
    batch_size = 100
    for i in range(0, len(data_to_insert), batch_size):
        batch = data_to_insert[i:i+batch_size]
        try:
            index.upsert(vectors=batch)
            print(f"Upserted batch {i//batch_size + 1}")
        except Exception as e:
            print(f"Error during upsert of batch {i//batch_size + 1}:", e)
    
    print("All batches upserted")
    return True



