from openai import ai

# INPUT: "Natural language message of a subway delay"
# OUTPUT: "JSON object with the subway lines and the estimated delay in minutes"
def ai_guess_delay(message) -> str:
    client = ai()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "The following message is a tweet from a official subway account. Please, if the message is that a subway line or lines are delayed (now or in the future, ignore if it was in the past), return an array of lines and the estimated delay in minutes if no time is given try to guess a number on the range from 1 to 60 minutes, otherwise return an empty array and 0 minutes. People who fall to the rails cause a delay of no less than 30 minutes. The response should be in raw json format, no markdown, only json. There lines are 1-9, A,B and 12 The attributes are 'lines' and 'delay'."},
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return completion.choices[0].message.content
