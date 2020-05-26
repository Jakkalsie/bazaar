import pymongo
import datetime
import requests
import pandas as pd
import numpy as np


def update_request():
    request = requests.get('https://api.hypixel.net/skyblock/bazaar',
                           params={'key': API_KEY})
    return request.json()


client = pymongo.MongoClient(
    "mongodb+srv://Devya:luca19741974@bazaaranalytica-2xjrf.mongodb.net/Bazaar?retryWrites=true&w=majority")
db = client.Bazaar

API_KEY = 'd5a0321f-aca1-4dd3-b4ac-2c35ed175787'

feedback = update_request()

for product in feedback['products']:
    if product != "ENCHANTED_CARROT_ON_A_STICK":
        db.Products.insert_one({
            'Name': product,
            'Buy Price': feedback['products'][product]['sell_summary'][0]['pricePerUnit'],
            'Sell Price': feedback['products'][product]['buy_summary'][0]['pricePerUnit'],
            'Buy Volume': feedback['products'][product]['quick_status']['buyMovingWeek'],
            'Sell Volume': feedback['products'][product]['quick_status']['sellMovingWeek'],
            'Buy Order Volume': feedback['products'][product]['quick_status']['buyVolume'],
            'Sell Order Volume': feedback['products'][product]['quick_status']['sellVolume'],
            'TimeStamp': datetime.datetime.utcnow()})
