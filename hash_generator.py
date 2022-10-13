import sys
import os
import hashlib  #hashing library
import time   #produce time stamp
from dotenv import load_dotenv

def hash_gen(private_key, api_key):
    #Generating the Hash
    m = hashlib.md5()

    ts = str(1)   #creates time stamp as 1
    m.update(bytes(ts, 'utf-8'))  # add the timestamp to hash
    m.update(bytes(private_key, 'utf-8')) #add the private key to 
        #the hash in byte format
    m.update(bytes(api_key, 'utf-8')) #add the public key to 
        #the hash in byte format
    hasht = m.hexdigest()    #Marvel requires the string to be in hex(mentioned nowhere)
    return hasht

load_dotenv()
hash = hash_gen(os.getenv("private_key"), os.getenv("api_key"))
env_file = open(".env", "a")
env_file.write(f"\nhash={hash}")
env_file.close()

print(f"hash is {hash}")