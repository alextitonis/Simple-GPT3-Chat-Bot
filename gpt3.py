import openai
import os
import string

class gpt3:
    def __init__(self, key):
        openai.api_key = key
        
    
    def getResponse(self, input):
        input += 'bot:'
        response = openai.Completion.create(
                    engine='davinci',
                    prompt=input,
                    max_tokens=100,
                    temperature=0.85,
                    top_p=1,
                    n=1,
                    stop = ['\n bot', '\nbot', '\nHuman: '],
                    frequency_penalty=0,
                    presence_penalty=0.7
                    )
        
        resp = response.choices[0].text + ''
        return resp