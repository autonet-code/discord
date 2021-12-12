import services
from human import Human
from datetime import datetime, timedelta
from cloud_db import get_db, humans,doc_ref
from sayings import generic
from random import randrange
import os
import discord
import requests
import openai
from collections import UserDict
from datetime import datetime, timedelta
import sys
from discord.utils import get
from discord.member import Member
from discord.message import Message
from discord.channel import TextChannel
from discord.guild import Guild
from discord.utils import find
from random import randrange
from discord.ext import commands
import typing as t
import sqlite3

master_commands = {"restart":services.restart,"say":None}
chat_channels = {"🏮gpt-3":services.chat_neutral}
tools_channels = {"❓ask-a-question":services.codx_qna,"💻write-python-code":services.codex,"📓explain-code":services.codx_xplain,"💭simplify":services.codx_simplify}

autonet: Guild
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix='.')

@client.event
async def on_ready():
    global cursor
    global humans
    global autonet
    autonet = client.get_guild(856143944453455912)
    m: Member = autonet.members[3]
    print(m.display_name+" nick ", m.nick)
    print("bot is online")

print("length ",len(humans))
print("humans ",humans)

def testare():
    print("se testeaza")

async def master(m: Message):
    zice = m.content
    com = zice.split(" ")[0]
    if com in master_commands:
        if com == "say":
            unde = zice.split(" ")[1]
            ce = " ".join(zice.split(" ")[2:])
            lacare = discord.utils.get(autonet.channels, name=unde)
            await lacare.send(ce)
        if com == "restart":
            services.restart()

def get_prompt(cine, zice):
    prompt=""
    if not os.path.isfile('chat_logs/'+cine+'.txt'):
        prompt= "The following is a conversation with an AI assistant. The assistant is creative, clever, and very friendly. Human: Hello, who are you? AI: I am an Autonet agent specializing in Natural Language Processing. Human: "+zice+" AI:"
    else:
        with open('chat_logs/'+cine+'.txt', 'r') as file:
            history=file.read()
            if len(history)<800:
                prompt=history+" Human: "+zice+" AI:"
            else:
                prompt=history[-800:]+" Human: "+zice+" AI:"
    return prompt

async def deal_with_it(m):
    canal = str(m.channel)
    cine = str(m.author)
    zice= str(m.content)
    print("serving "+canal+" for "+cine+" with "+zice)
    reply=generic[randrange(0,len(generic))]
    ramane=reply

    if "gpt" in canal:
        prompt=get_prompt(cine,zice)
        print("prompt length" + str(len(prompt)) +" prompt: ",prompt)
        reply=chat_channels[canal](prompt)
        with open('chat_logs/'+cine+'.txt', 'w') as file:
            file.write(prompt+reply)
        await m.reply(content=reply)
    elif "trusty" in canal:
        reply=services.call_direct_chatbot(zice, cine)
        await m.reply(content=reply)

    else:
        if len(zice)>600:
            reply="Keep your input under 600 characters, please (a little more than two tweets)"
        else:
            reply=tools_channels[canal](zice)
        await m.reply(content=reply)
    
@client.event
async def on_message(mess): 
    m: Message = mess
    try:
        canal = str(m.channel)
        cine = str(m.author)    
        zice= str(m.content)
        if "auto#1967" in cine:
            return None
        if "***" in zice:
            return None
        if "Eight Rice#1340" in canal and zice.split(" ")[0]in master_commands:
            print("executing master command ",zice)

            await master(m)
            return None
        if "trusty" in canal:
            await deal_with_it(m)
        if canal in chat_channels or canal in tools_channels:
            registered=False
            h:Human
            for h in humans:
                if cine==h.discord_id:
                    registered=True
                    print("e inregistrat")
                    expired=h.lastUpdate<datetime.now()-timedelta(days=1)
                    print("expired: ",expired)
                    if expired:
                        print("resetting credits")
                        h.testCredits=50
                        h.lastUpdate=datetime.now()
                    if h.testCredits<1:
                        
                        if h.msg_out_of_credits==False:
                            h.msg_out_of_credits=True
                            try:
                                await m.author.send(content="You're all out of requests for today. You'll get more on "+str((h.lastUpdate+timedelta(minutes=4)).strftime("%d-%m-%Y, at %H:%M. You can check your credits on autonet.live/#/assets")))
                                return None
                            except:
                                await m.reply(content="You're all out of requests for today. You'll get more on "+str((h.lastUpdate+timedelta(minutes=4)).strftime("%d-%m-%Y, at %H:%M. You can check your credits on autonet.live/#/assets" )))
                                return None
                        else:
                            await m.delete(delay=None)
                            return None
                    h.testCredits=h.testCredits-1
                    await deal_with_it(m)
                    doc_ref.document(h.address).set(h.to_dict())
            if not registered and h.not_registered_msg==False:
                await m.delete(delay=None)
                h.not_registered_msg=True
                try:
                    await m.author.send(content="Your Discord ID is not registered. To get your free daily credits and unlimited chat with Trusty, go to www.autonet.live, sign in, grab your Access Token from the Profile section (click on your address on the top right and go to Credits). Once you've done that, come back here and type *auth YOUR_ACCESS_TOKEN. It sounds more complicated than it actually is, just try to do it and if you have any issues ask somebody, but don't give them your access_token. Only paste that as a private message here. ")
                except:
                    await m.reply(content="Get your access token from https://autonet.live and put it in a private message to me like this: *auth ACCESS_TOKEN.")
                return None
        if zice[:5]=="*auth":   
            get_db()
            h:Human
            access_token=zice[5:]
            found_access_token=False
            for h in humans:
                if h.accessToken in zice:
                    found_access_token=True
                    await m.author.send(content="GREAT SUCCESS! You're now registered.")   
                    h.discord_id=cine
                    doc_ref.document(h.address).set(h.to_dict())
                    break
            if not found_access_token and h.auth_tries<10:
                h.auth_tries=h.auth_tries+1
                await m.author.send(content="There is no such access token.")
                return None
    except Exception as e:
        print("big error. Big! ",e) 

client.run(os.getenv("DISCORD_BOT_TOKEN"))