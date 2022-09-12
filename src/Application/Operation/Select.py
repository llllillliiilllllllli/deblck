from typing import Any, List, Tuple
from Styles import Color 
from Utils import Log 

def inquire_selection(options: List[Tuple[str, str]]) -> Tuple[Any, Any]:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    commandline = input(f"{Color.Green}\u276f{Color.Reset} Commandline: ")

    if commandline != "":
        try:
            entity = commandline.split(" ")[0]
            action = commandline.split(" ")[1]

            for cls, funct in options: 
                if cls.__name__ == entity:
                    if funct.__name__ == action:
                        return (cls, funct) 
        except:
            Log.error(f"Incorrect commandline {commandline}")

    else: 
        print(f"\nSelect from options:")
        for i, option in enumerate(options):
            print(f"{i+1} {option[0].__name__}.{option[1].__name__}")

        selection = input(f"\n{Color.Green}\u276f{Color.Reset} Selection: ")   

        try:
            return options[int(selection)-1]
        except:
           Log.error(f"Inccorect selection {selection}")
