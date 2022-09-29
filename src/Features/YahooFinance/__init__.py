import os 
import re

# Initiate modules in this package 
path = os.path.dirname(__file__)
with os.scandir(path) as entries:
    for entry in entries:

        if not re.search(r"__", entry.name):

            if not re.search(r".py", entry.name):
                package = f"{__name__}.{entry.name}" 
                __import__(package)

            if re.search(r".py", entry.name):
                module = f"{__name__}.{entry.name[0:-3]}"
                __import__(module)
                