import json
import os
from openai import OpenAI

# client= OpenAI
openai_keys = json.load(open("C:/shared/content/config/api-keys/openai.json"))
my_openai_key = openai_keys["team-7"]
os.environ["OPENAI_API_KEY"] = my_openai_key
# print(my_openai_key)

# OpenAI.api_key = my_openai_key

hardcoded_logs = [
    '{transactionId:"4719433006",message:"Successful Response", httpStatusCode:200, webPage:"Welcome", ipAddress:"126.76.229.194"}',
    '{transactionId:"4719433006",message:"Failed to load data", httpStatusCode:500, webPage:"Menu", ipAddress:"126.76.229.194"}',
    '{transactionId:"4719433006",message:"Successful Response", httpStatusCode:200, webPage:"Order", ipAddress:"126.76.229.194"}',
    '{transactionId:"4719433006",message:"Successful Response", httpStatusCode:200, webPage:"Confirm", ipAddress:"126.76.229.194"}',
    '{transactionId:"0567270564",message:"Success", httpStatusCode:200, webPage:"Welcome", ipAddress:"35.59.18.1"}',
]

use_hardcoded = True

def analyze_logs(logs):
    # print('logs inside function: ' + str(logs))

    client = OpenAI()
    # client.api_key = my_openai_key
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.2,
        messages=[
            # {"role": "user", "content": "Do you think any of these logs have failures? I'm especially interested in users who may have started the process but not finished. The order of pages is Welcome, Menu, Order, Confirm. All transactions have a unique transactionId to identify the transaction. Transactions must reach the webpage Confirm to be successful. Only tell me the ones that might be a failure or potential failure. Make sure to list all transactions that might be failures. Return your answer as a json, including the message, the transaction id and with the reasoning in a 'reason' key in the response"+ str(logs)},
            {
                "role": "user",
                "content":
                # "Do you think any of these logs have failures?"+
                # "I'm especially interested in users who may have started the process but not finished." +
                # "The order of pages is Welcome, Menu, Order, Confirm. There should be a log for each page."+
                # "If there is not a log for each page, then that could be a failure"+
                # "All transactions have a unique transactionId to identify the transaction."+
                # "Transactions must reach the webpage Confirm to be successful." +
                # "Return a success or failure status for each transaction. Return your answer as a json,"+
                # " including the message (use the value from the log), the transaction id and with the reasoning in a 'reason' key in the response: "+ str(logs),
                "You will be provided with an array of logs. "
                + "Determine which ones are failures and output them as JSON as the following: "
                + '{ "failingLogs": [ { "original": { <FAILING LOG> }, "assessment": <ASSESSMENT> }, ...] , "patterns": <PATTERNS> }.\n'
                + "For <ASSESSMENT>, insert your assessment as to why this log might be failing, specifically given the context of this log and the logs preceding it.  Determine if there are any patterns as well.\n"
                + "For <PATTERNS>, write (in plain English) any patterns you observe regarding failing logs.  If there are none, just output undefined.\n"
                + 'For each failure, add a property called "certainty" which indicates your level of certainty on how likely the log is a failure, on a scale of 0.00 to 1.00.\n'
                + 'If you are not able to find any log failures, return that same JSON, but replace the value of "failingLogs" with undefined.\n'
                + "Logs: "
                + str(logs),
            }
        ],
    )
    return response.choices[0].message.content


if use_hardcoded:
    logs = hardcoded_logs
else:
    with open("generated_logs.json") as f:
        logs = json.load(f)

result = analyze_logs(logs)
parsed_json = json.loads(result)
prettified_json = json.dumps(parsed_json, indent=4)
print(prettified_json)
