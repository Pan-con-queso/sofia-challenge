from pathlib import Path
from tqdm import tqdm

path = Path.cwd() / "vo2_max_data"
for folder in tqdm(sorted(path.iterdir())):
  if folder.is_dir():
    for file in folder.iterdir():
      #If we want to start the iteration where we left it
      if file.suffix == ".DONE":
        file.unlink()