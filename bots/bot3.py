import os
from dotenv import load_dotenv
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

def run():
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
