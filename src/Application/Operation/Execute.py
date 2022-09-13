from typing import Any, Tuple
from Utils import Log
import traceback

def execute(selection: Tuple[Any, Any]) -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Log.info(f"Execute command: {selection[0].__name__}.{selection[1].__name__}")

    try: 
        selection[1]()
    except Exception as ex:
        Log.error(ex)
        traceback.print_exc()

    Log.info(f"Finish command: {selection[0].__name__}.{selection[1].__name__}")
    return None
