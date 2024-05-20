# Script to divide full_data in smaller csv
import pandas as pd
from datetime import datetime, timedelta

SIZE_FILES = 1000

def main():
  start_datetime = datetime(2022,5,21)
  for i,chunk in enumerate(pd.read_csv("full_data.csv", chunksize=SIZE_FILES)):
    chunk['date'] = start_datetime
    chunk.to_csv('bonus/chunks/chunk_{}.csv'.format(i), index=False)
    start_datetime = start_datetime + timedelta(days=30)

if __name__ == "__main__":
  main()