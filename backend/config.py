import os
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_ENCODING = os.getenv("EMBEDDING_ENCODING")
TOP_K_VECTORS = int(os.getenv("TOP_K_VECTORS")) 
OPEN_AI_LLM = os.getenv("OPEN_AI_LLM")
TEMPERATURE = float(os.getenv("TEMPERATURE"))

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_HOST = os.getenv('PINECONE_HOST')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

REDIS_HOST=os.getenv('REDIS_HOST')
REDIS_PORT=os.getenv('REDIS_PORT')
REDIS_PASSWORD=os.getenv('REDIS_PASSWORD')

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_NAME = os.getenv("MONGODB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
