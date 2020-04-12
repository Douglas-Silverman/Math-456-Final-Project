import csv

import pandas as pd

def create_struct(file_name) :
    data_struct = [] # [V Team, V ML, H Team, H ML, Winner name]
                 #    0       1      2      3        4
    data = pd.read_csv(file_name)

    indexNames = data[ pd.isnull(data['Team']) ].index
    data.drop(indexNames , inplace=True)

    for index, row in data.iterrows():
        if(index % 2 == 0) :
            if(type(row['ML']) == type("NL")):
                row['ML'] = row['Close']
            data_struct.append([ row['Team'], row['ML'], -1, -1, row['Final'] ])
        else :
            if(type(row['ML']) == type("NL")):
                row['ML'] = row['Close']
            data_struct[len(data_struct) - 1][2] = row['Team']
            data_struct[len(data_struct) - 1][3] = row['ML']
            if(data_struct[len(data_struct) - 1][4] > row['Final']) :
                data_struct[len(data_struct) - 1][4] = data_struct[len(data_struct) - 1][0]
            elif(data_struct[len(data_struct) - 1][4] == row['Final']) :
                data_struct[len(data_struct) - 1][4] = 'Tie'
            else :
                data_struct[len(data_struct) - 1][4] = data_struct[len(data_struct) - 1][2]

    return data_struct