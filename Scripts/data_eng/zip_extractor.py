from zipfile import ZipFile 

def main(zip_name: str):
    with ZipFile(zip_name, 'r') as zObject:
       zObject.extractall() 


if __name__ == "__main__":
  zip_name = "vo2_max_data.zip"
  main(zip_name)