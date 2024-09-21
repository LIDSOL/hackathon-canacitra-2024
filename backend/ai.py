from openai import OpenAI as ai

# INPUT: "Natural language message of a subway delay"
# OUTPUT: "list with the subway lines and the estimated delay in minutes"
def ai_guess_delay(message) -> list:
    client = ai()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "The following message is a tweet from a official subway account. Please, if the message is that a subway line or lines are delayed (now or in the future, ignore if it was in the past), return an array of lines and the estimated delay in minutes if no time is given try to guess a number on the range from 1 to 60 minutes, otherwise return 'NO'. People who fall to the rails cause a delay of no less than 30 minutes. The response should be in python list format. There lines are 1-9, A,B and 12. The line format should be 'ML1', 'ML2', 'ML3', 'ML4', 'ML5', 'ML6', 'ML7', 'ML8', 'ML9', 'MLA', 'MLB' and 'ML12'. and the delay should be an integer, example [('ML1', 10), ('ML2', 20)]."},
            {
                "role": "user",
                "content": message
            }
        ]
    )

    #message = "El servicio se encuentra momentáneamente detenido en la Línea 7 y 6. Realizamos maniobras para rescatar a una persona que presuntamente se arrojó al paso del tren."
    #guess = ai_guess_delay(message)
    #print(guess)
    # [('ML6', 30), ('ML7', 30)]
    #for line_delay in guess:
        #print("Line:", line_delay[0])
        #print("Delay:", line_delay[1])

    if completion.choices[0].message.content == "NO":
        return []

    return eval(completion.choices[0].message.content)

# INPUT: "Natural language user report"
# OUTPUT: ("ML1", "ML2")
def ai_guess_report(message) -> list:
    client = ai()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "The following message is a user report of a subway delay. Please, return the line or lines that are affected. The response should be in python list format, ['line1', 'line2', ...] .There lines are 1-9, A,B and 12. The line format should be 'ML1', 'ML2', 'ML3', 'ML4', 'ML5', 'ML6', 'ML7', 'ML8', 'ML9', 'MLA', 'MLB' and 'ML12'. and the delay should be an integer, example ['ML1', 'ML2']."},
            {
                "role": "user",
                "content": message
            }
        ]
    )

    # Example usage
    #message = "La linea 3 y 6 va lentisima, llevamos 20 minutos parados en Zapata"
    #report = ai_guess_report(message)
    #print(report)
    #['ML3', 'ML6']

    # Convert the string to a tuple
    return eval(completion.choices[0].message.content)
