import Config
import pandas as pd
import numpy as np
import requests
import re 
from datetime import datetime, timedelta

def empty_df(index=[]):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    empty = pd.DataFrame(index=index, data={
        "Open": np.nan, "High": np.nan, "Low": np.nan,
        "Close": np.nan, "Adjusted Close": np.nan, "Volume": np.nan})
    empty.index.name = "Date"
    return empty

def epoch_to_date(timestamp: str) -> datetime:
    if timestamp < 0:
        return datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    else:
        return datetime.fromtimestamp(timestamp)