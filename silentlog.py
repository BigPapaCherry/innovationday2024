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
            # {"role": "user", "content": "Do you think any of these logs have failures? I'm especially interested in users who may have started the process but not finished. The order of pages is Welcome, Menu, Order, Confirm. All transactions have a unique transactionId to identify the transaction. Transactions must reach the webpage Confirm to be successful. Only tell me the ones that might be a failure or potential failure. Make sure to list all transactions that might be failures. Return your answer as a json, including the message, the transaction id and with the reasoning in a 'reason' key in the response"+ str(logs)},
            {"role": "user", "content": "Do you think any of these logs have failures?"+
              "I'm especially interested in users who may have started the process but not finished." +
              "The order of pages is Welcome, Menu, Order, Confirm. There should be a log for each page."+
              "If there is not a log for each page, then that could be a failure"+ 
              "All transactions have a unique transactionId to identify the transaction."+ 
              "Transactions must reach the webpage Confirm to be successful." + 
              "Return a success or failure status for each transaction. Return your answer as a json,"+
              " including the message, the transaction id and with the reasoning in a 'reason' key in the response: "+ str(logs)},
        ]
    )
    return response.choices[0].message.content



logs = ['{message:"successful response", transId:2222}', 'great success', 'everything worked', 'incomplete transId=1236', '200 http success','successful response', 'great success', 'everything worked', 'failed to complete transId=1235', '200 http success', 'successful response', 'great success', 'everything worked', 'incomplete transId=1234', '200 http success','successful response', 'great success', 'everything worked', 'failed to complete transId=1237', '200 http success']
logs2 = ['{message:"successful response", transId:2222}', '{message:"great success", transId:2223}', '{message:"transaction started", transId:2229}', '{message:"everything worked", transId:2224}', '{message:"incomplete", transId:1236}', '{message:"500 failed to complete", transId:1237}' ]
complexlogs = ['{transactionId:"4719433006",message:"Successful Response", httpStatusCode:200, webPage:"Welcome", ipAddress:"126.76.229.194"}',
               '{transactionId:"4719433006",message:"Failed to load data", httpStatusCode:500, webPage:"Menu", ipAddress:"126.76.229.194"}',
               '{transactionId:"4719433006",message:"Successful Response", httpStatusCode:200, webPage:"Order", ipAddress:"126.76.229.194"}',
               '{transactionId:"4719433006",message:"Successful Response", httpStatusCode:200, webPage:"Confirm", ipAddress:"126.76.229.194"}', 
               '{transactionId:"0567270564",message:"Success", httpStatusCode:200, webPage:"Welcome", ipAddress:"35.59.18.1"}']
result = analyze_logs(complexlogs)
print(result)
# print(*json.loads(result))
failureKey = str(*json.loads(result))
# print('first failure:   ' + str(json.loads(result)[failureKey][0]['message']))