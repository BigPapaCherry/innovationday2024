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
    # client.api_key = my_openai_key
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": "Do you think any of these logs have failures? if a status code exists, use http statuses to guide if it is a failure. Only tell me the ones that might be a failure. Return your answer as a json, including the message, the transaction id and with the reasoning in a 'reason' key in the response"+ str(logs)},
        ]
    )
    return response.choices[0].message.content



logs = ['{message:"successful response", transId:2222}', 'great success', 'everything worked', 'incomplete transId=1236', '200 http success','successful response', 'great success', 'everything worked', 'failed to complete transId=1235', '200 http success', 'successful response', 'great success', 'everything worked', 'incomplete transId=1234', '200 http success','successful response', 'great success', 'everything worked', 'failed to complete transId=1237', '200 http success']
logs2 = ['{message:"successful response", transId:2222}', '{message:"great success", transId:2223}', '{message:"transaction started", transId:2229}', '{message:"everything worked", transId:2224}', '{message:"incomplete", transId:1236}', '{message:"500 failed to complete", transId:1237}' ]
result = analyze_logs(logs2)
# print(result)
print(*json.loads(result))
failureKey = str(*json.loads(result))
print('first failure:   ' + str(json.loads(result)[failureKey][0]['message']))


