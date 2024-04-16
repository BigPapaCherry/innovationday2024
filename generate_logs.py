import json
import os
from openai import OpenAI

openai_keys = json.load(open("C:/shared/content/config/api-keys/openai.json"))
my_openai_key = openai_keys["team-7"]
os.environ["OPENAI_API_KEY"] = my_openai_key


def generate_logs():
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.5,
        messages=[
            {
                "role": "user",
                "content": "Generate 10 logs using the following format, correcting it so that it is valid JSON as needed: \n"
                + "{ logs: [ { transactionId: <TRANSACTIONID>, poid: <POID>, userType: <USERTYPE>, data: { eventType: <EVENTTYPE>, message: <MESSAGE> } }, <additional logs>...] }\n"
                + "Insert these values as necessary: \n"
                + 'transactionId: a string matching the following format: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", where X is any alphanumeric character (lowecase),\n'
                + "poid: a 10 digit integer,\n"
                + 'userType: a string matching either "CLIENT" or "PROSPECT",\n'
                + "eventType: a hyphenated description of the event, including the acronym of the calling service, the process, and whether it passed or failed,\n"
                + "message: a message describing the precise nature of the error.\n"
                + "For each log, come up with a 3-letter acronym for a fictional service pertaining to the financial/investments industry.  For example, \"BNK\" could be used as the client bank lookup service.\n"
                + "Additionally, come up with the specific process that is being referenced and whether it passed or failed.  Ultimately, the eventType should look something like this: BNK-bank-lookup-failure.\n"
                + "Other rules: There should only be 1-3 error logs, poid, transactionId, and userType should be the same for every log."
                + "Ensure that you ONLY ouput the requested JSON."
            }
        ],
    )
    return response.choices[0].message.content


logs = generate_logs()
parsed_json = json.loads(logs)
prettified_json = json.dumps(parsed_json, indent=4)
print(prettified_json)

with open('generated_logs.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_json, f, ensure_ascii=False, indent=4)