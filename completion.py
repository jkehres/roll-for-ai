import os
import openai
from dotenv import load_dotenv

def get_completion(prompt):
  load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return response["choices"][0]["text"].strip()