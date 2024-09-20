import os
from openai import OpenAI

client = OpenAI(
    api = os.getenv("OPENAI_API_KEY")
)

def ai_guess_delay(message) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "The following message is a tweet from a official subway account. Please, if the message is that a subway line or lines are delayed (now or in the future, ignore if it was in the past), return an array of lines and the estimated delay in minutes if no time is given try to guess a number on the range from 1 to 60 minutes, otherwise return an empty array and 0 minutes. The response should be in raw json format. There lines are 1-9, A,B and 12 The attributes are 'lines' and 'delay'."},
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return completion.choices[0].message.content