import os
import openai

def make_openai_request(status):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
      engine="davinci",
      prompt=status.text,
      temperature=0.9,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.6,
      stop=["\n"]
    )

    # content safety check
    return response
