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

def API_call(api_key, hasht, nameStartsWith, offset):
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

def All_calls(api_key):
    #All marvel characters fetched by going through every ascii characters
    i = 0
    df_final = pd.DataFrame() 
    while i<129:
        offset=0
        c=0
        while (c==0 and offset==0) or c==100:    #c is the count returned after every call
            df_select, c = API_call(api_key, hash_gen(os.getenv("private_key"), os.getenv("api_key")), chr(i), offset)
            df_final = pd.concat([df_final, df_select])   #appending every call data
            offset = offset+100      #offset increased by 100
        i=i+1
    return df_final

configure()
df_final = All_calls(os.getenv("api_key"))

print("Initial DF shape:", df_final.shape)
print(df_final.head())
df_rm_duplicates = df_final.drop_duplicates(subset=["id"])
print("Final DF shape:", df_rm_duplicates.shape)
df_rm_duplicates.to_csv("./marvel_data.csv", index_label=None)