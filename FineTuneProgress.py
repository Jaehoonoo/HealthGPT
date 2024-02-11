import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI( #gets api key from epi file
    api_key=os.environ.get('OPENAI_API_KEY'),
)
fine_tuning_job_id = ' '#never got this do to service issues

# Retrieve the status of the fine-tuning job
job_status = client.fine_tuning.jobs.retrieve(fine_tuning_job_id)

# Print the job status
print(job_status)
