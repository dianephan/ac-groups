from io import BytesIO
import os
import random
from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, request, url_for
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

app = Flask(__name__)
client = Client()

playersDictionary = {}

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

def help_text():
    return respond(f'Welcome to the Animal Crossing Gardeners Directory!' 
                + '\n Say "hello" to join the directory'
                + '\n Say "check" to see who else is online'
                + '\n You can change your status to the following: '
                + '\n "watering" - if you are available to water plants for others'
                + '\n "trade" - if you have time to water someone\'s plants if they water yours'
                + '\n "drought" - if you need friends to visit your island to water'
                + '\n "bye" - if you need to log off')

def set_status(status, player):
    playersDictionary[player] = status
    return respond(f'Your status has been changed to: ' + status)

@app.route('/webhook', methods=['POST'])
def webhook():
    player = request.form.get('From')
    twilioNumber = request.form.get('To')
    message = request.form.get('Body').lower()

    if message == 'check':
        if playersDictionary:
            return respond(playersDictionary)
        else:
            return respond(f'No one is here. Invite people to your Animal Crossing directory.')
    if player in playersDictionary and message == 'watering':
        status = 'Available to water plants'
        return set_status(status, player)
    if player in playersDictionary and message == 'trade':
        status = 'Looking to water flower for flower'
        return set_status(status, player)
    if player in playersDictionary and message == 'drought':
        status = 'Island drought - need visitors!'
        return set_status(status, player)
    if player in playersDictionary and message == 'bye':
        status = 'Offline'
        return set_status(status, player)
    if message == 'hello' and player not in playersDictionary:
        status = 'Online'
        playersDictionary[player] = status
        return respond(f'Hello, {player}, you have been added to the directory')
    if message == 'hello' and player in playersDictionary:
        status = 'Online'
        playersDictionary[player] = status
        return respond(f'Welcome back, {player}!')
    else:
        return help_text()

