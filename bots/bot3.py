import os
from dotenv import load_dotenv
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

def run():
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    agent = create_csv_agent(OpenAI(temperature=0, openai_api_key=openai_api_key), "./data/doug_score.csv", verbose=True)

    car_question = "what are the 10 highest rated cars as a daily?"

    bot_response = agent.run(car_question)

    print(bot_response)
