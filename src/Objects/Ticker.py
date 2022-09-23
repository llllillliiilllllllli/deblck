class Ticker():

    def __init__(self, symbol: str):
        self.symbol = symbol.upper()

        self._history = None
        self._fundamentals = False 
        self._info = None 
        self._analysis = None 
        self._sustainability = None 
        self._recommendations = None 
        self._major_holders = None
        self._institutional_holders = None
        self._mutualfund_holders = None 
        self._isin = None 
        self._news = []
        self._shares = None 

        self._calendar = None 
        self._expirations = {}
        self._earnings_dates = None 
        self._earnings_history = None 

        self._earnings = {
            "yearly": {},
            "quarterly": {},
        }

        self ._financials = {
            "yearly": {},
            "quarterly": {},
        }

        self._balancesheet = {
            "yearly": {},
            "quarterly": {}
        }

        self._cashflow = {
            "yearly": {},
            "quarterly": {}
        }
