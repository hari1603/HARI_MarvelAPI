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

def hash_gen(private_key, api_key):
    #Generating the Hash
    m = hashlib.md5()

    ts = str(time.time())   #creates time stamp as string
    m.update(bytes(ts, 'utf-8'))  # add the timestamp to hash
    m.update(bytes(private_key, 'utf-8')) #add the private key to 
        #the hash in byte format
    m.update(bytes(api_key, 'utf-8')) #add the public key to 
        #the hash in byte format
    hasht = m.hexdigest()    #Marvel requires the string to be in hex(mentioned nowhere)
    return hasht

def API_call(api_key, hasht, nameStartsWith):
    #constructing the query

    base_url = "https://gateway.marvel.com"  #base url
    query = "/v1/public/characters" +"?"  #Query for all characters

    #Actual query look like:
    #query_url = base_url + query +"nameStartsWith=spider&limit=10&"+"ts=" + ts+ "&apikey=" + api_key + "&hash=" + hasht
    #print(query_url) 
    
    query_url = base_url + query
    ts = str(time.time())
    payload = {
        'nameStartsWith':nameStartsWith,
        'limit':100,
        'ts':ts,
        'apikey':api_key,
        'hash':hasht
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
        return df_select
    
    except:
        if data["code"] == 200:
            print(nameStartsWith, "queried characters: 0")
        else:
            print(data)

def All_calls(api_key):
    #All marvel characters fetched by going through every ascii characters
    i = 0
    df_final = pd.DataFrame() 
    while i<129:
        df_select = API_call(api_key, hash_gen(os.getenv("private_key"), os.getenv("api_key")), chr(i))
        df_final = pd.concat([df_final, df_select])   #appending every call data
        i=i+1
    return df_final

configure()
df_final = All_calls(os.getenv("api_key"))

print(df_final.head())
print(df_final.shape)