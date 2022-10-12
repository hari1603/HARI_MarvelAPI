import pandas as pd
import num_hari

df = pd.read_csv("./marvel_data.csv")   #opening the dataset

df.head()

def filter(df, op_column, op, value, display_column):
    #make sql like where queries by passing in the column, value , comparision operator
    #and select the columns you want to be displayed
    df_show = pd.DataFrame()
    match op:
        case '>':
            df_show = df[df[op_column]>value][display_column]
            return df_show
        case '<':
            df_show = df[df[op_column]<value][display_column]
            return df_show
        case '=':
            df_show = df[df[op_column]==value][display_column]
            return df_show
        case '>=':
            df_show = df[df[op_column]>=value][display_column]
            return df_show
        case '<=':
            df_show = df[df[op_column]<=value][display_column]
            return df_show

df_show = filter(df, "comics.available", '=', 4, ["id", "name"])
print(df_show)