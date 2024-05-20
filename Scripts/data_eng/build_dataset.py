import sqlite3
import zlib 
import json 
from tqdm import tqdm
from pathlib import Path
from jmespath import search
import csv
import os

def flatten_json(json: json) -> dict:
  flattened_dict_from_json = {}
  for key in json:
    columns = search(f"{key}[0]", json)
    # REVISE THIS IF-ELSE
    if columns is None:
        flattened_dict_from_json.update({key: json.get(key)})
    else:
        flattened_dict_from_json.update(columns)
  return flattened_dict_from_json

def get_next_row():
  fields_written = False
  path = Path.cwd() / "vo2_max_data"
  for folder in tqdm(sorted(path.iterdir())):
    if folder.is_dir():
      for file in folder.iterdir():
        if file.suffix != ".json":
          continue 
        #If we want to start the iteration where we left it
        if file.with_suffix(".DONE").exists():
          continue 

        data_str = file.read_text()
        data_json = json.loads(data_str)
        # revise if we have a json added by Ziggy 
        name = search("personal_data[0].name", data_json)
        if name is None:
          continue

        flattened_json = flatten_json(data_json)
        
        if not fields_written:
          fields_written = True
          yield list(flattened_json.keys())
        yield list(flattened_json.values())
        file.with_suffix(".DONE").touch()

def insert_row_into_sqlite(con, cur, row):
  #IF HEADERS: crear tabla
  if "vo2_max" in row:
    row = [column_name.replace(column_name, "int"+column_name) if column_name[0].isdigit() else column_name for column_name in row]
    row = [string.replace(",","_").replace(" ", "_").replace("-","_").replace("+","_").replace("%","_").replace("/","_").replace(":","_").replace("(","").replace(")","") for string in row]
    #row = [string.replace("name", "name UNIQUE") for string in row]
    row_string =', '.join(row)
    command = f"CREATE TABLE IF NOT EXISTS vo2_max({row_string})"
  else:
    # We need to insert the string values with quote marks in the query
    row = ['"' + value + '"' if isinstance(value,str) else value for value in row]
    row_string =', '.join(str(value) for value in row)
    command = f"INSERT INTO vo2_max VALUES ({row_string})"
  cur.execute(command)
  con.commit()

  #ELSE agregar a tabla


def main():
  con = sqlite3.connect("vo2_max_data.db")
  cur = con.cursor()
  with open('full_data.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    row_iterator = get_next_row()
    while True:
      try:
        next_row = next(row_iterator)
        csvwriter.writerows([next_row])
        insert_row_into_sqlite(con, cur, next_row)
      except StopIteration:
        print('Finished creating data csv')
        con.close()
        break
  csvfile.close()




if __name__ == "__main__":
  main()