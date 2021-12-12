import openai
import json
import sys
import requests
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def codex(zice):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt="\"\"\"\n"+zice+"\n\"\"\"",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    ceva = response.choices[0].text
    return str(ceva)

def codx_simplify(zice):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt="My second grader asked me what this passage means:\\n\"\"\"\\n"+zice +
        "\\n\"\"\"\\nI rephrased it for him, in plain language a second grader can understand:\\n\"\"\"",
        temperature=0,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0,
        stop=["\"\"\""]
    )
    ceva = response.choices[0].text.split("\\n")[1]
    return str(ceva)

def chat_neutral(zice):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=zice,
        temperature=0.9,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["Human:", " AI:"]
    )
    ceva = response.choices[0].text
    return str(ceva)

def chat_friendly(zice):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt="You: What have you been up to?\\nFriend: Watching old movies.\\nYou: Did you watch anything interesting\\nFriend: Not really\\nYou: "+zice+"\\nFriend: ",
        temperature=0.4,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["\\nYou:"]
    )
    ceva = response.choices[0].text
    return str(ceva)

def chat_sarcastic(zice):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt="Marv is a chatbot that reluctantly answers questions. You: How many pounds are in a kilogram? Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this. You: What does HTML stand for? Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future. You: When did the first airplane fly? Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away. You: What is the meaning of life? Marv: I’m not sure. I’ll ask my friend Google. You: "+zice+". Marv:",
        temperature=0.3,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["Marv:", "You: "]
    )
    ceva = response.choices[0].text
    return str(ceva)

def codx_qna(zice):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt="Q: "+zice+"A:",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Q:"]
    )
    
    try:
        dobis = response.choices[0].text.split("A:")[1]
        return str(dobis)
    except Exception as e:
        return "that's fine, except: "+str(e)

def codx_xplain(zice):
    response = response = openai.Completion.create(
        engine="davinci-codex",
        prompt=zice+"\\n'''\\n#here's what the above code is doing:\\n#1.",
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\\""\\""\\"""]
    )
    print(response)
    ceva = response.choices[0].text
    return str(ceva)

def call_direct_chatbot(zice, uid):
    url =os.getenv('CHATBOT_URL')
    querystring = {"bid": os.getenv('bid'), "key": os.getenv('key'),
                   "uid": uid, "msg": zice}
    headers = {
        'x-rapidapi-host': os.getenv('x-rapidapi-host'),
        'x-rapidapi-key': os.getenv('x-rapidapi-key')
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    return response.text.split("cnt\":\"")[1].split("\"")[0]

def restart():
    # global connection
    import sys
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    import os
    # connection.commit()
    # connection.close()
    os.execv(sys.executable, ['python'] + sys.argv)

