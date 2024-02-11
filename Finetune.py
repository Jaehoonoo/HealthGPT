import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI( #gets api key from epi file
    api_key=os.environ.get('OPENAI_API_KEY'),
)

file = client.files.create(#gets data set from repository
    file=open("meal_plan_chat_dataset.jsonl", "rb"),
    purpose="fine-tune"
)

client.fine_tuning.jobs.create(#starts fine tuning process
    training_file=file.id,
    model="gpt-3.5-turbo"
)
#unable to fine tune model due to issues with openai payment services
