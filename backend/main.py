from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
from openai import OpenAI, AuthenticationError
from pinecone import Pinecone
from pymongo import MongoClient
import os
from utlis.prompt_templates import general_qa_prompt_template
from config import (EMBEDDING_MODEL, TEMPERATURE, TOP_K_VECTORS, OPEN_AI_LLM,
                    PINECONE_API_KEY,PINECONE_INDEX_NAME, PINECONE_HOST, MONGODB_URI, MONGODB_NAME, 
                    COLLECTION_NAME)

app = Flask(__name__)
CORS(app)

pc = Pinecone(api_key=PINECONE_API_KEY)


client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]
user_collection = db[COLLECTION_NAME]


def check_openai_api_key(client):
    try:
        client.models.list()
    except AuthenticationError as e:
        return False
    else:
        return True


def get_embedding(text, model, api_key):
    client = OpenAI(api_key=api_key)
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def generate_stream(prompt, api_key,):
    query_vector = get_embedding(prompt, model=EMBEDDING_MODEL, api_key=api_key)

    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
    query_results = index.query(vector=query_vector, top_k=TOP_K_VECTORS, include_metadata=True)

    results = []
    tags = []
    for result in query_results['matches']:
        most_similar_id = result['id']
        metadata = result["metadata"]
        concatenated_string = (
            "Question Title: " + metadata["Question_Title"].strip() +
            "; Question: " + metadata["Question_Body"].strip() +
            "; Tags: " + metadata["Tags"].strip() +
            "; Answer: " + metadata["Answer_Body"].strip()
        )
        tags.append(metadata["Tags"].strip())
        results.append(concatenated_string)
    result_context = ''.join(results)

    general_prompt = general_qa_prompt_template.format(tag=tags, user_query=prompt, contexts=result_context)

    client = OpenAI(api_key=api_key)

    stream = client.chat.completions.create(
        model=OPEN_AI_LLM,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": general_prompt
            }
        ],
        # temperature=TEMPERATURE,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield f"data: {json.dumps(chunk.choices[0].delta.content)}\n\n"


@app.route('/health')
def health_check():
    return "I am alive! But is CI/CD alive? Check CI/CD v2", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data['prompt']
    api_key = request.headers.get('OpenAI-API-Key')
    if not api_key:
        return jsonify({"error": "OpenAI API Key is missing in headers"}), 400

    client = OpenAI(api_key=api_key)
    if not check_openai_api_key(client):
        return jsonify({"error": "Invalid OpenAI API Key"}), 401

    return Response(generate_stream(prompt, api_key), mimetype='text/event-stream')

@app.route('/api/users', methods=['GET'])
def get_users():
    users = user_collection.find().sort("reputation",)
    user_list = list(users)
    for user in user_list:
        user["_id"] = str(user["_id"])  
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
