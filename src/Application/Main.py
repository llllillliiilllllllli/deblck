from datetime import datetime  
import traceback

from Config import *
from Styles import UI
from Operation import Inspect  
from Operation import Select  
from Operation import Execute  

def main():

    UI.print_console() 

    try: 
        features = Inspect.inspect_features()
        selection = Select.inquire_selection(features)
        execution = Execute.execute(selection) 

    except Exception:
        traceback.print_exc()

    selection = input("\nContinue (Y/N): ")
    if selection == "Y":
        main()
    else:
        return

if __name__ == '__main__':
    beg = datetime.now()
    main()
    end = datetime.now()
    duration = end - beg
    duration = duration.total_seconds()
    
    print(f"\nProgram finished in {duration:.2f} sec")
