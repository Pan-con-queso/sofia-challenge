# Generate Data 
import pandas as pd
from datetime import datetime
import random
import string
import csv
import argparse


def generate_header(list_csv):
    sup_fit_header = list(list_csv)
    other_elements = ['age', 'gender', 'name', 'vo2_max', 'date']
    header = other_elements[:3] + sup_fit_header + other_elements[3:]
    return header

def generate_row(df_sorted, date_time):
   #Mandar todo este codigo a una función
       list_to_add = []
       # generate age
       list_to_add.append(random.randint(20,80))
       # generate gender
       list_to_add.append(random.choice(['M', 'F']))
       # generate name
       list_to_add.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
       # generate columns from csv
       for index, row in df_sorted.iterrows():
          if row['Category'] == 'Fitness':
             list_to_add.append(random.randint(0,row['Optimal Dose']))
          else:
             list_to_add.append(random.uniform(0,row['Optimal Dose']))
       # generate vo2_max
       list_to_add.append(random.uniform(14.6938,45.9026))
       list_to_add.append(date_time)
       return list_to_add
   

def main(args):
    #Open file with optimal values
    df_opt = pd.read_csv("Optimal Protocol Levels.csv")
    fitness_data = df_opt[df_opt['Category'] == 'Fitness']
    supplements_data = df_opt[df_opt['Category'] == 'Supplements']
    df_sorted = pd.concat([fitness_data, supplements_data])
    # Create Header
    header = generate_header(df_sorted['Description'])
    # TODO print header in CSV
    date_time = args['date'].replace('/','_')
    file_name = f"data_{date_time}.csv"
    with open(file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for i in range(args['N']):
            csvwriter.writerow(generate_row(df_sorted, args['date']))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Create synthetic data')
  parser.add_argument('date', type=str, 
                    help='date to add to the csv')
  parser.add_argument('N',  type=int, 
                    help='number of arguments')
  args = vars(parser.parse_args())
  main(args)