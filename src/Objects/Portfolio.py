from typing import List 

from Objects.Ticker import Ticker
from Objects.Contract import Contract 
from Objects.Code import HybridCode 

class Portfolio:
    bonds       : List[Ticker]
    stocks      : List[Ticker] 
    derivatives : List[Contract]
    hybrids     : List[HybridCode] 
    