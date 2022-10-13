# import dependencies
import sys
import os
import pandas as pd
import hashlib  #hashing library
import time   #produce time stamp
import json   
import requests #request info from the API
from dotenv import load_dotenv

def configure():
    load_dotenv()

def API_call(api_key, hasht, nameStartsWith, offset):
    #constructing the query

    base_url = "https://gateway.marvel.com"  #base url
    query = "/v1/public/characters" +"?"  #Query for all characters

    #Actual query look like:
    #query_url = base_url + query +"nameStartsWith=spider&limit=10&"+"ts=" + ts+ "&apikey=" + api_key + "&hash=" + hasht
    #print(query_url) 
    
    query_url = base_url + query
    ts = str(1)
    payload = {
        'nameStartsWith':nameStartsWith,
        'limit':100,
        'ts':ts,
        'apikey':api_key,
        'hash':hasht,
        'offset':offset
    } # all the parameters for the query

    #Making the API request and receiving info back as a json
    data = requests.get(query_url, params=payload).json()
    # json_obj = json.dumps(data, indent=4) # can be further stored as json dump

    try:
        #Storing the data to a dataframe
        df = pd.DataFrame(data)
        df_norm = pd.json_normalize(df["data"]["results"])  #Breaks down keys to the basic form
        df_select = df_norm[["id", "name", "comics.available", "series.available", "stories.available", "events.available"]]
        print(nameStartsWith, "queried characters: ", data["data"]["count"])
        return df_select, df["data"]["count"]
    
    except:
        if data["code"] == 200:
            print(nameStartsWith, "queried characters: 0")
        else:
            print(data)
        return None, 0

def All_calls(api_key, hash, nameStartWith):
    #All marvel characters fetched by going through every ascii characters
    df_final = pd.DataFrame() 
    offset=0
    c=0
    while (c==0 and offset==0) or c==100:    #c is the count returned after every call
        df_select, c = API_call(api_key, hash, nameStartWith, offset)
        df_final = pd.concat([df_final, df_select])   #appending every call data
        offset = offset+100      #offset increased by 100
    return df_final

configure()
df_final = All_calls(os.getenv("api_key"), os.getenv("hash"), '%')

print("Initial DF shape:", df_final.shape)
print(df_final.head())
df_rm_duplicates = df_final.drop_duplicates(subset=["id"])
print("Final DF shape:", df_rm_duplicates.shape)
df_rm_duplicates.to_csv("./marvel_data.csv", index_label=None)