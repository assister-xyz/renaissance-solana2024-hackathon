import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CSV_OUTPUT_DIRECTORY = os.getenv('CSV_OUTPUT_DIRECTORY', 'data_output')

API_BASE_URL = "https://api.stackexchange.com/2.3"
STACK_EXCHANGE_API_KEY = os.getenv("STACK_EXCHANGE_API_KEY")

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_HOST = os.getenv('PINECONE_HOST')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'default-model')
EMBEDDING_ENCODING = os.getenv('EMBEDDING_ENCODING', 'default-encoding')
MAX_EMBEDDING_TOKENS = int(os.getenv('MAX_EMBEDDING_TOKENS', 512))

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_NAME = os.getenv("MONGODB_NAME")
