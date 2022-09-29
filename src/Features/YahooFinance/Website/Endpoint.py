from typing import List

class Endpoint: 
    
    EP_BASE = "https://query1.finance.yahoo.com"
    EP_SEARCH = "https://query1.finance.yahoo.com/v1/finance/search{parameters}"
    EP_QUOTE = "https://query1.finance.yahoo.com/v6/finance/quote{parameters}"
    EP_QUOTE_ALT = "https://query1.finance.yahoo.com/v7/finance/quote{parameters}"
    EP_OPTIONS = "https://query1.finance.yahoo.com/v7/finance/options/{symbol}"
    EP_DOWNLOAD = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
    EP_HISTORY = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}{parameters}" 
    EP_SUMMARY = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}{parameters}"

    query : str
    symbol : str
    symbols : List[str]
    modules : List[str] = [
        "assetProfile",
        "defaultKeyStatistics",
        "recommendationTrend",
        "financialData",
        "majorHoldersBreakdown",
        "earnings",
        "earningsHistory",
        "earningsTrend",
        "indexTrend",
        "industryTrend",
        "netSharePurchaseActivity",
        "sectorTrend",
        "insiderHolders",
        "upgradeDowngradeHistory"]

    interval : str = None
    range : str = None
    period : str = None
    period1 : str = None
    period2 : str = None
    close : str = None
    events : str = None
    prepost : str = None

    def __init__(self):
        pass

    def configure_search_endpoint(self) -> str:        
        parameters = ""
        parameters += "?q=" + ",".join(self.symbols)
        return self.EP_QUOTE.replace("{parameters}", parameters) 

    def configure_quote_endpoint(self) -> str:
        parameters = ""
        parameters += "?symbols=" + ",".join(self.symbols)
        return self.EP_QUOTE.replace("{parameters}", parameters) 

    def configure_options_endpoint(self) -> str:   
        parameters = self.symbol
        return self.EP_OPTIONS.replace("{parameters}", parameters) 

    def configure_download_endpoint(self) -> str:        
        parameters = self.symbol
        return self.EP_DOWNLOAD.replace("{parameters}", parameters) 

    def configure_history_endpoint(self) -> str:
        parameters = ""
        parameters += self.symbol
        if self.interval != None: parameters += "?interval=" + self.interval
        if self.range != None: parameters += "?range=" + self.range
        if self.period != None: parameters += "?period=" + self.period
        if self.period1 != None: parameters += "?period1=" + self.period1
        if self.period2 != None: parameters += "?period2=" + self.period2
        if self.close != None: parameters += "?close=" + self.close
        if self.events != None: parameters += "?events=" + self.events
        if self.prepost != None: parameters += "?prepost=" + self.prepost
        
        return self.EP_HISTORY.replace("{parameters}", parameters) 

    def configure_summary_endpoint(self) -> str:        
        parameters = ""
        parameters += "?symbol=" + self.symbol
        parameters += "?modules=" + ",".join(self.modules)        
        return self.EP_SUMMARY.replace("{parameters}", parameters)
