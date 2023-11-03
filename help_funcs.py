import json
instructions = json.loads(open('instructions.json').read())
from credentials import *

def make_prompt(key=None, model=None, test=False) -> str:
    '''
    Take a model name and a key which are used to extract instructions and models answers.
    returns: str prompt to another model.
    '''
    if key == None:
        raise TypeError('Key is None')
    if model == None:
        raise Exception('Provide a model name')
    answer = instructions[key][model]['Response']
    question = instructions[key]['instruction']
    prompt = "Evaluate answers provided by language model to instructions. " + \
            "If the answer is false explain why. Possible reasons: factual mistake, grammar mistake, logic mistake, no common sense, not according to the instruction, unethical, should not answer as a language model." +  \
            "Use this template to say if answer is false: <listed reasons from the list of possible reasons and brief explanation>; template if answer is true: 'TRUE'." + \
            "Example of your answer if True: TRUE. Example of your answer if False: logic mistake, no common sense. " + \
            f"Question: '{question}'. Answer: '{answer}'. "
    if test == True:
        return prompt[prompt.index('Question:'):]
    return prompt


from requests import post
def make_open_ai_request(prompt=None, token=OPENAI_API_KEY):
    if prompt == None:
        raise Exception('Provide prompt')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
        'model' : 'gpt-3.5-turbo',
        'messages' : [{'role' : 'user', 'content' : prompt}],
        'temperature' : 0.7
    }
    return post(url, headers=headers, json=body)


import nltk
def get_eval(response:json) -> (str, str):
    response_str = response['choices'][0]['message']['content']
    tokens = nltk.word_tokenize(response_str)
    evl = tokens[0].lower()
    if evl == 'true':
        res = 'TRUE'
        comment = ''
    else:
        res = 'FALSE'
        comment = response_str[7:]
    return res, comment

def make_request_yandex(instruction = None, model='general', tok = IAMTOKEN):
    if type(instruction) != str:
        raise TypeError('instruction should be a string')
    url = "https://llm.api.cloud.yandex.net/llm/v1alpha/instruct"
    headers = {
        "Authorization": f"Bearer {tok}",
        "x-folder-id": "b1gmdp3kcenod48c8ts0",
        "Content-Type": "application/json"
    }
    body = {"model": model,
            "generationOptions": {
                "partialResults": False,
                "temperature": 0.5,
                "maxTokens": 4096,
                },
            "instructionText": instruction,
            }
    return post(url=url, headers=headers, json=body)


def make_request_gigachat(instruction=None, token=GIGATOK, model='GigaChat:latest'):
    if type(instruction) != str:
        raise TypeError('Instruction should be in str format.')
    url = "https://beta.saluteai.sberdevices.ru/v1/chat/completions"
    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    body = {"model": model,
            'messages' : [
                {
                    'role' : 'user',
                    'content' : instruction
                }
            ],
            'temperature' : 0.87 #default value (previously used 0.7)
            }
    return post(url=url, headers=headers, json=body)