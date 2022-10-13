import pandas as pd

df = pd.read_csv("./marvel_data.csv")   #opening the dataset

def df_filter():
    col = input("Enter the column which needs to be filtered")
    condition = input("Enter the condition")
    val = input("Enter the Value")
    try:
        df_filtered = df[col].apply(lambda x: eval(f"{x} {condition} {val}"))
        print(f"Total queries obtained: {df[df_filtered].shape[0]}")
        print(df[df_filtered])
    except:
        print("Wrong Query. Please try again!")

df_filter()