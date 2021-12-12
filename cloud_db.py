from firebase_admin import credentials
from firebase_admin import credentials, firestore
import firebase_admin
import services
import pandas as pd
import sqlite3
from human import Human
from datetime import datetime

cred=credentials.Certificate('./atntokencreds.json')
default_app=firebase_admin.initialize_app(cred)
db=firestore.client()
doc_ref=db.collection(u'humans')
humans=[]

def get_db():
    global humans
    humans.clear()
    doc_ref.get()
    for doc in doc_ref.get():
        doc=doc.to_dict()
        h:Human=Human(
            address=doc['address'],
            discord_id=doc['discord_id'] if 'discord_id' in doc else None,   
            accessToken=doc['accessToken'],
            lastUpdate=datetime(doc['lastUpdate'].year,doc['lastUpdate'].month,doc['lastUpdate'].day,doc['lastUpdate'].hour,doc['lastUpdate'].minute,doc['lastUpdate'].second),
            testCredits=doc['testCredits'],
            shares=doc['shares'],
            credits=doc['credits']
        )
        humans.append(h)

get_db()