import os
import sys
import re 

# Initiate project system paths
path = os.path.dirname(__file__)
while True:
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir() and re.search("__pycache__", entry.name) == None:
                sys.path.append(entry.path)

    if os.path.basename(path) == "src": 
        sys.path.insert(0, path)
        break    

    path = os.path.dirname(path)
