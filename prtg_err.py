import time
import eventlet
import requests
import logging
import telebot
import json
import io
from time import sleep

URL = 'api_prtg'
FILENAME = 'last_search.txt'
BOT_TOKEN = 'token'
CHANNEL_NAME = '@channel'
SINGLE_RUN = True

bot = telebot.TeleBot(BOT_TOKEN)

#Get json data from API PRTG
def get_data():
    timeout = eventlet.Timeout(10)
    try:
        feed = requests.get(URL)
        return feed.json()
    except eventlet.timeout.Timeout:
        logging.warning('Got Timeout while retrieving data. Cancelling...')
        return None
    finally:
        timeout.cancel()

#Send new errors (device, name)
def send_new_errors(items):
	for item in items:
		link ="{0} {1}".\
		format(item['device'], item['sensor'])
		read = open(FILENAME,'r').read()
		print (link)
		if link not in read:
			bot.send_message(CHANNEL_NAME, link)
		sleep(1)
	return

#Check new Errors	
def check_new_errors():
    with open(FILENAME,'r') as file:
        last_search = file.readlines()
    feed = get_data()
    if feed is not None:
        entries = feed['sensors']
        send_new_errors(entries)
        with open(FILENAME,'wt') as file:
            a=0
            b=len(entries)
            while a<b:
                file.write(entries[a]['device'])
                file.write(' ')
                file.write(entries[a]['sensor'])
                file.write(' \n')
                a=a+1
    return

if not SINGLE_RUN:
        while True:
            check_new_errors()
            sleep(3)
else:
    check_new_errors()
