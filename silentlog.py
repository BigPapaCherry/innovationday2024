import json
import os
from openai import OpenAI

# client= OpenAI
openai_keys = json.load(open('C:/shared/content/config/api-keys/openai.json'))
my_openai_key = openai_keys['team-7']
os.environ['OPENAI_API_KEY'] = my_openai_key
# print(my_openai_key)

# OpenAI.api_key = my_openai_key


def analyze_logs(logs):
    # print('logs inside function: ' + str(logs))

    client = OpenAI()
    client.api_key = my_openai_key
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": "Analyze these Splunk logs to find silent failures: "+ str(logs)},
        ]
    )
    return response.choices[0].message.content



logs = ['successful response', 'great success', 'everything worked', 'huge failure', '200 http success']
print(analyze_logs(logs))


