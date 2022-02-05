from os import environ,listdir, getcwd
from os.path import join,dirname
from random import choice
from typing import List,Union
from json import loads


from flask import Flask, request, send_from_directory
from pymongo import MongoClient
from twilio.rest import Client
from pyjokes import get_joke

from strings import *



# Setup Flask
app = Flask(__name__)

# Configs 
db_string, db_password = environ["DB_STRING"],environ["DB_PASSWORD"]

account_sid, auth_token = environ['TWILIO_ACCOUNT_SID'], environ['TWILIO_AUTH_TOKEN']


# Setup DB
client = MongoClient(db_string.replace("pwd",db_password))
db = client.assignbot
users , messages = db['users'] , db['messages']

# Setup Twillio Client
client = Client(account_sid, auth_token)



# messages.delete_many({})
# users.delete_many({})

@app.route("/")
@app.route("/index")
@app.route("/assignbot")
def index():
    return "Hello, World!"


@app.route("/sms", methods=['POST'])
def on_message():
    
    raw_message = request.form
    msg :dict = {key:value for key,value in raw_message.items()}

    messages.insert_one(msg) # add to db

    user_number, user_name = msg.get("From").split(":")[1], msg.get("ProfileName")
    text = msg.get("Body").lower() # Original Message Body(if text it is text message)
    words:List[str] = text.split(" ")


    if users.count_documents({ 'number':user_number }, limit = 1) == 0:
        users.insert_one({ # User not Exits in db / Message from New User
            'ProfileName' : user_name,
            'WaId' : msg.get('WaId'),
            'number' : user_number
        })
        text = str(welcome + intro).replace('user_name',user_name)

    elif text in help : text = intro
    elif text in what_is_my_name : text = f"Hey Hi ... {user_name}"
    elif text in give_me_joke : text = get_joke()
    elif text in picuture : media_url = [picsum_link]
    elif text in  documents : media_url = [request.url_root + "random-file"]

    elif ( 'file' in words or 'document' in words ) and words[-1].isnumeric():
            if int(words[-1]) > 10 : text = max_files
            else : media_url =  [request.url_root + "random-file" for _ in  range(int(words[-1]))]

    else : text = f"You Said : *{msg['Body']}* " # If nothing to say >>> return what he say

    if media_url :
        for url in media_url : client.messages.create( media_url=[url], from_= msg["To"], to=msg["From"] )
    else :  client.messages.create( body=text, from_=msg["To"], to=msg["From"] )

    return empty_responce_xml # Empty Responce to Twilio


@app.route('/sms-status',methods=['POST'])
def on_sms_status():

    message = {key:value  for key, value in request.form.items()} # Actual Message

    if messages.count_documents({'SmsMessageSid' : message.get('SmsMessageSid')}, limit = 1) == 0:  
        messages.insert_one(message) # If message not in database

    elif messages.find_one({'SmsMessageSid' : message.get('SmsMessageSid')},limit=1)["SmsStatus"] != 'read':
        messages.update_one( # Update if status updated
            {'SmsMessageSid' : message.get('SmsMessageSid')},
            {"$set":{'SmsStatus':message.get('SmsStatus')}})
    
    return empty_responce_xml 

@app.route("/random-file", methods =['GET'])
def random_file():
    """
    To get random file from static files 
    @returns: returns any random file from static files
    """
    files =  join(getcwd(),"static",'files')
    file = choice(listdir(files))
    return send_from_directory(files, file)

