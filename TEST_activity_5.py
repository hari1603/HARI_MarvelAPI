# import dependencies
import sys
import os
import pandas as pd
from activity_5 import Hari_Marvel_API


# Initializing a marvel object
marvel = Hari_Marvel_API()

# Generates the hash
hash = marvel.hash_gen()
print(hash)

# Generates a call to fetch all characters starting with a certain letter
df = marvel.All_calls('a')
print("DF size is ", df.shape)
print(df.head())

# Filters based on your condition given to the above dataset that you made
df_filtered = marvel.df_filter(df)
print("FILTERED DF size is ", df_filtered.shape)
print(df_filtered.head())