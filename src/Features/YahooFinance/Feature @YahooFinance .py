# YAHOO FINANCE ENDPOINTS

USER_AGENT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

URL_BASE = "https://finance.yahoo.com"
URL_QUOTE = "https://finance.yahoo.com/quote/{symbol}"
URL_SUMMARY = "https://finance.yahoo.com/quote/{symbol}?p={symbol}"
URL_CHART = "https://finance.yahoo.com/quote/{symbol}/chart?p={symbol}"
URL_CONVERSATION = "https://finance.yahoo.com/quote/{symbol}/community?p={symbol}"
URL_STATISTICS = "https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}"
URL_HISTORY = "https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"
URL_PROFILE = "https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}"
URL_FINANCIALS = "https://finance.yahoo.com/quote/{symbol}/financials?p={symbol}"
URL_ANALYSIS = "https://finance.yahoo.com/quote/{symbol}/analysis?p={symbol}"
URL_OPTIONS = "https://finance.yahoo.com/quote/{symbol}/options?p={symbol}" 
URL_HOLDERS = "https://finance.yahoo.com/quote/{symbol}/holders?p={symbol}"
URL_SUSTAINABILITY = "https://finance.yahoo.com/quote/{symbol}/sustainability?p={symbol}"

EP_SEARCH = "https://query1.finance.yahoo.com/v1/finance/search?q={query}"
EP_QUOTE = "https://query1.finance.yahoo.com/v6/finance/quote?symbols={symbols}"
EP_QUOTE_ALT = "https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
EP_OPTIONS = "https://query1.finance.yahoo.com/v7/finance/options/{symbol}"
EP_DOWNLOAD = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
EP_HISTORY = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}" 
EP_SUMMARY = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules={modules}"

from typing import Any 
from datetime import datetime
import os, re

import numpy as np
import pandas as pd
import requests

from Application.Utils import Validation
from Application.Utils import Convertion

from Objects.Ticker import Ticker

class YahooFinance:

    summary_modules = [
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

    ### Request Configuration

    def config_url(ticker: Ticker) -> str:
        return NotImplemented

    def config_headers(ticker: Ticker) -> Any:
        return NotImplemented

    def config_cookies(ticker: Ticker) -> Any:
        return NotImplemented

    def config_files(ticker: Ticker) -> Any:
        return NotImplemented

    def config_auth(ticker: Ticker) -> Any:
        return NotImplemented
    
    def config_timeout() -> Any:
        return 20

    def config_redirects(ticker: Ticker) -> Any:
        return NotImplemented
    
    def config_proxies(proxies: dict=None) -> dict:
        if proxies != None:
            if isinstance(proxies, dict) and "https" in proxies:
                proxies = proxies["https"]
            proxies = {"https": proxies}
        return proxies

    ### Ticker Checking

    def get_ticker_by_isin(isin, proxy=None, session=None):    
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if not(Validation.is_isin(isin)):
            raise ValueError("Invalid ISIN number")

        session = session or requests
        url = "{}/v1/finance/search?q={}".format(URL_BASE, isin)
        data = session.get(url=url, proxies=proxy, headers=USER_AGENT_HEADERS)
        try:
            data = data.json()
            ticker = data.get("quotes", [{}])[0]
            return {
                "ticker": {
                    "symbol": ticker["symbol"],
                    "shortname": ticker["shortname"],
                    "longname": ticker["longname"],
                    "type": ticker["quoteType"],
                    "exchange": ticker["exchDisp"],
                },
                "news": data.get("news", [])
            }
        except Exception:
            return {}

    ### Financial Data Collection

    def collect_search() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Collect data from search endpoint by Yahoo Finance API 

        >>> param: str  # inquire input file having list of queries
        >>> param: str  # inquire output folder for exporting file 
        >>> param: str  # inquire output file name for renaming file

        >>> funct: 0    # inquire user input for input and output
        >>> funct: 1    # for each query, send request to Yahoo API
        >>> funct: 2    # configure properties for web request
        >>> funct: 3    # save all reponse data to json file
        >>> funct: 4    # convert response data to json format
        >>> funct: 5    # extract quotes in search data to data frame
        >>> funct: 6    # extract news in search data to data frame
        >>> funct: 7    # export quotes in data frame to csv file
        >>> funct: 8    # export news in data frame to csv file
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""        
        ### 0
        in_file = input("\nEnter input file path: ").replace("\"", "").strip()
        out_dir = input("\nEnter output folder path: ").replace("\"", "").strip()
        out_file = input("\nEnter output file name: ").replace(" ", "").strip()

        try:
            queries_df = pd.read_csv(in_file, header=0, encoding="utf-8-sig")
        except:
            raise Exception(f"Cannot read file {in_file}")

        quotes_df = pd.DataFrame(columns=["query", "exchange", "shortname", "quoteType", \
            "symbol", "index", "score", "typeDisp", "longname", "exchDisp", "sector", \
            "industry", "dispSecIndFlag", "isYahooFinance"])

        news_df = pd.DataFrame(columns=["query", "uuid", "title", "publisher", "link", \
            "providerPublishTime", "type", "thumbnailUrl", "thumbnailWidth", \
            "thumbnailHeight", "thumbnailTag", "relatedTickers", ])

        ### 1
        for _, series in queries_df.iteritems():
            for _, query in series.iteritems():

        ### 2
                url = EP_SEARCH.replace("{query}", query)
                timeout = YahooFinance.config_timeout()
                proxies = YahooFinance.config_proxies()

                try:
                    print(f"\nCollect: {url}")
                    response = requests.get(
                        url=url,
                        headers=USER_AGENT_HEADERS,
                        timeout=timeout,
                        proxies=proxies,
                    )            
                except:
                    raise Exception(f"Cannot request {url}")   
        ### 3
                path = f"{out_dir}\\Datason @{query.replace(' ', '')}Search #-------------- .json"
                with open(path, mode="w", encoding="utf-8-sig") as file:
                    file.write(response.text)

                timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")
                os.rename(path, path.replace("#--------------", f"#{timestamp}"))
        ### 4
                try:
                    response = response.json()
                except:
                    raise Exception(f"Invalid JSON format {response}")
        ### 5
                for result in response["quotes"]:            
                    values = [query]
                    for column in quotes_df.columns[1:]:
                        try: 
                            values.append(result[column])
                        except:
                            values.append("—")

                    quotes_df.loc[len(quotes_df)] = values
        ### 6
                for result in response["news"]:
                    providerPublishTime = Convertion.epoch_to_date(result["providerPublishTime"])
                    try:
                        thumbnail_url = result["thumbnail"]["resolutions"][0]["url"]
                    except:
                        thumbnail_url = "—"
                    try:
                        thumbnail_width = result["thumbnail"]["resolutions"][0]["width"]
                    except:
                        thumbnail_width = "—"
                    try:
                        thumbnail_height = result["thumbnail"]["resolutions"][0]["height"]
                    except:
                        thumbnail_height = "—"
                    try:
                        thumbnail_tag = result["thumbnail"]["resolutions"][0]["tag"]
                    except:
                        thumbnail_tag = "—"
                    try:
                        relatedTickers = result["relatedTickers"]
                    except:
                        relatedTickers = "—"

                    news_df.loc[len(news_df)] = [query, result["uuid"], result["title"], result["publisher"], \
                        result["link"], providerPublishTime, result["type"], thumbnail_url, \
                        thumbnail_width, thumbnail_height, thumbnail_tag, relatedTickers]
        
        ### 7
        path = f"{out_dir}\\Dataset @{out_file}Quotes #-------------- .csv"                
        quotes_df.to_csv(path, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
        os.rename(path, path.replace("#--------------", f"#{timestamp}")) 
        
        ### 8
        path = f"{out_dir}\\Dataset @{out_file}News #-------------- .csv"                
        news_df.to_csv(path, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
        os.rename(path, path.replace("#--------------", f"#{timestamp}")) 

        return None

    def collect_quotes() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Collect data from quotes endpoint by Yahoo Finance API 

        >>> param: str  # inquire input file containing list of symbols
        >>> param: str  # inquire output folder for exporting file 
        >>> param: str  # inquire output file name for renaming file

        >>> funct: 0    # instantiate tickers based on symbols
        >>> funct: 1    # configure properties for web requests
        >>> funct: 2    # send requests to Yahoo and handle errors 
        >>> funct: 3    # select data points from web reponses
        >>> funct: 4    # export collected data to the output file
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""        
        ### 0
        in_file = input("\nEnter input file path: ").replace("\"", "").strip()
        out_dir = input("\nEnter output folder path: ").replace("\"", "").strip()
        out_file = input("\nEnter output file name: ").replace(" ", "").strip()

        try:
            symbols_df = pd.read_csv(in_file, header=0, encoding="utf-8-sig")
        except:
            raise Exception(f"Cannot read file {in_file}")

        tickers = []
        for _, series in symbols_df.iteritems():
            for _, value in series.iteritems():
                ticker = Ticker(value)
                tickers.append(ticker)

        ### 1
        symbols = ",".join([ticker.symbol for ticker in tickers])
        url = EP_QUOTE.replace("{symbols}", symbols)
        timeout = YahooFinance.config_timeout()
        proxies = YahooFinance.config_proxies()

        ### 2
        try:
            print(f"\nCollect: {url}")
            response = requests.get(
                url=url,
                headers=USER_AGENT_HEADERS,
                timeout=timeout,
                proxies=proxies,
            )            
        except:
            error_msg = response["quoteResponse"]["error"]
            raise Exception(f"Cannot request {error_msg}")  

        ### 3
        path = f"{out_dir}\\Datason @{out_file}Quotes #-------------- .json"
        with open(path, mode="w", encoding="utf-8-sig") as file:
            file.write(response.text)

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")
        os.rename(path, path.replace("#--------------", f"#{timestamp}"))

        ### 4
        try:
            response = response.json()
        except:
            raise Exception(f"Invalid JSON format {response}")
        
        ### 5
        quotes_df = pd.DataFrame(columns=["ticker", "language", "region", "quoteType", "typeDisp", \
            "quoteSourceName", "triggerable", "customPriceAlertConfidence", "currency", \
            "exchangeTimezoneName", "gmtOffSetMilliseconds", "exchangeTimezoneShortName", \
            "messageBoardId", "esgPopulated", "exchange", "longName", "shortName", \
            "firstTradeDateMilliseconds", "priceHint", "circulatingSupply", "lastMarket", \
            "volume24Hr", "volumeAllCurrencies", "fromCurrency", "toCurrency", "coinMarketCapLink", \
            "regularMarketPrice", "regularMarketChangePercent", "postMarketChangePercent", \
            "postMarketTime", "postMarketPrice", "postMarketChange", "regularMarketChange", \
            "regularMarketTime", "regularMarketDayHigh", "regularMarketDayRange", \
            "regularMarketDayLow", "regularMarketVolume", "regularMarketPreviousClose", \
            "bid", "ask", "bidSize", "askSize", "fullExchangeName", "financialCurrency", \
            "regularMarketOpen", "averageDailyVolume3Month", "averageDailyVolume10Day", \
            "startDate", "coinImageUrl", "logoUrl", "fiftyTwoWeekLowChange", \
            "fiftyTwoWeekLowChangePercent", "fiftyTwoWeekRange", "fiftyTwoWeekHighChange", \
            "fiftyTwoWeekHighChangePercent", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "dividendDate", \
            "earningsTimestamp", "earningsTimestampStart", "earningsTimestampEnd", \
            "trailingAnnualDividendRate", "trailingPE", "trailingAnnualDividendYield", \
            "epsTrailingTwelveMonths", "epsForward", "epsCurrentYear", "priceEpsCurrentYear", \
            "sharesOutstanding", "bookValue", "fiftyDayAverage", "fiftyDayAverageChange", \
            "fiftyDayAverageChangePercent", "twoHundredDayAverage", "twoHundredDayAverageChange", \
            "twoHundredDayAverageChangePercent", "marketCap", "forwardPE", "priceToBook", \
            "sourceInterval", "exchangeDataDelayedBy", "averageAnalystRating", "tradeable", \
            "cryptoTradeable", "market", "marketState", "displayName", "symbol"]) 

        for result in response["quoteResponse"]["result"]:
            ticker = result["symbol"]
            values = [ticker]
            for column in quotes_df.columns[1:]:
                try:
                    values.append(result[column])
                except:
                    values.append("—")
                  
            quotes_df.loc[len(quotes_df)] = values

        ### 6
        path = f"{out_dir}\\Dataset @{out_file}Quotes #-------------- .csv"                
        quotes_df.to_csv(path, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
        os.rename(path, path.replace("#--------------", f"#{timestamp}")) 

        return None

    def collect_options() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Collect data from options endpoint by Yahoo Finance API 

        >>> param: str  # inquire input file containing list of symbols
        >>> param: str  # inquire output folder for exporting file 
        >>> param: str  # inquire output file name for renaming file

        >>> funct: 0    # inquire user input for input and output
        >>> funct: 1    # for each symbol, send request to Yahoo API
        >>> funct: 2    # configure properties for web request
        >>> funct: 3    # save all reponse data to json file
        >>> funct: 4    # convert response data to json format
        >>> funct: 5    # if options not available, add empty values
        >>> funct: 6    # extract calls in options data to data frame
        >>> funct: 7    # extract puts in options data to data frame
        >>> funct: 8    # export calls in data frame to csv file
        >>> funct: 9    # export puts in data frame to csv file
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""        
        ### 0
        in_file = input("\nEnter input file path: ").replace("\"", "").strip()
        out_dir = input("\nEnter output folder path: ").replace("\"", "").strip()
        out_file = input("\nEnter output file name: ").replace(" ", "").strip()

        try:
            symbols_df = pd.read_csv(in_file, header=0, encoding="utf-8-sig")
        except:
            raise Exception(f"cannot read file {in_file}")

        calls_df = pd.DataFrame(columns=["ticker", "contractSymbol", "strike", "currency", "lastPrice", \
            "change", "percentChange", "volume", "openInterest", "bid", "ask", "contractSize", \
            "expiration", "lastTradeDate", "impliedVolatility", "inTheMoney"])

        puts_df = pd.DataFrame(columns=["ticker", "contractSymbol", "strike", "currency", "lastPrice", \
            "change", "percentChange", "volume", "openInterest", "bid", "ask", "contractSize", \
            "expiration", "lastTradeDate", "impliedVolatility", "inTheMoney"])

        ### 1
        for _, series in symbols_df.iteritems():
            for _, symbol in series.iteritems():
        ### 2
                url = EP_OPTIONS.replace("{symbol}", symbol)
                timeout = YahooFinance.config_timeout()
                proxies = YahooFinance.config_proxies()

                try:
                    print(f"\nCollect: {url}")
                    response = requests.get(
                        url=url,
                        headers=USER_AGENT_HEADERS,
                        timeout=timeout,
                        proxies=proxies,
                    )            
                except:
                    error_msg = response["optionChain"]["error"]
                    raise Exception(f"Cannot request {error_msg}")  
        ### 3
                path = f"{out_dir}\\Datason @{symbol}Options #-------------- .json"
                with open(path, mode="w", encoding="utf-8-sig") as file:
                    file.write(response.text)

                timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")
                os.rename(path, path.replace("#--------------", f"#{timestamp}"))
        ### 4
                try:
                    response = response.json()
                except:
                    raise Exception(f"Invalid JSON format {response}")
        ### 5
                try: 
                    _ = response["optionChain"]["result"][0]["options"]
                
                except IndexError:
                    values = [symbol]
                    for column in calls_df.columns[1:]:
                        values.append("—")
                    calls_df.loc[len(calls_df)] = values

                    values = [symbol]
                    for column in puts_df.columns[1:]:
                        values.append("—")
                    puts_df.loc[len(puts_df)] = values                    
                    
                    continue

                except KeyError:
                    values = [symbol]
                    for column in calls_df.columns[1:]:
                        values.append("—")
                    calls_df.loc[len(calls_df)] = values

                    values = [symbol]
                    for column in puts_df.columns[1:]:
                        values.append("—")
                    puts_df.loc[len(puts_df)] = values                    
                    
                    continue
        ### 6
                try:
                    for result in response["optionChain"]["result"][0]["options"][0]["calls"]:            
                        values = [symbol]
                        for column in calls_df.columns[1:]:
                            try: 
                                values.append(result[column])
                            except:
                                values.append("—")

                        calls_df.loc[len(calls_df)] = values
                except IndexError:
                     calls_df.loc[len(calls_df)] = ["—" for _ in range(len(calls_df.columns))]
        ### 7
                try:
                    for result in response["optionChain"]["result"][0]["options"][0]["puts"]:            
                        values = [symbol]
                        for column in puts_df.columns[1:]:
                            try: 
                                values.append(result[column])
                            except:
                                values.append("—")

                        puts_df.loc[len(puts_df)] = values
                except IndexError:
                     puts_df.loc[len(puts_df)] = ["—" for _ in range(len(puts_df.columns))]

        ### 8
        path = f"{out_dir}\\Dataset @{out_file}Calls #-------------- .csv"                
        calls_df.to_csv(path, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
        os.rename(path, path.replace("#--------------", f"#{timestamp}")) 
        
        ### 9
        path = f"{out_dir}\\Dataset @{out_file}Puts #-------------- .csv"                
        puts_df.to_csv(path, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
        os.rename(path, path.replace("#--------------", f"#{timestamp}")) 

        return None

    def collect_download() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 0
        in_file = input("\nEnter input file path: ").replace("\"", "").strip()

        try:
            symbols_df = pd.read_csv(in_file, header=0, encoding="utf-8-sig")
        except:
            raise Exception(f"cannot read file {in_file}")

        ### 1
        for _, series in symbols_df.iteritems():
            for _, symbol in series.iteritems():                
        ### 2
                url = EP_DOWNLOAD.replace("{symbol}", symbol)
                print(f"\nCollect: {url}")

                timeout = YahooFinance.config_timeout()
                proxies = YahooFinance.config_proxies()
                params = "..."

                try:
                    response = requests.get(
                        url=url,
                        headers=USER_AGENT_HEADERS,
                        timeout=timeout,
                        proxies=proxies,
                    )            
                except:
                    raise Exception(f"Cannot download data for {symbol}") 

        return None

    def collect_history() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Collect data from history endpoint by Yahoo Finance API 

        >>> param: path         str  # inquire input file containing list of symbols
        >>> param: path         str  # inquire output folder for exporting file 
        >>> param: path         str  # inquire output file name for renaming file

        >>> param: period       str  # [1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max]
        >>> param: interval     str  # [1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo]
        >>> param: prepost      bool # option to include pre and post market data 
        >>> param: events       bool # option to include corporate actions data 
        >>> param: adjusted     bool # adjust closing prices due to corporate actions 
        
        >>> funct: 0    # process paths input by user and read symbols from file
        >>> funct: 1    # process other paramters including interval and options
        >>> funct: 2    # instantiate meta and indicator data frames to store results 
        >>> funct: 3    # configure header, proxies, and parameters for web request
        >>> funct: 4    # send request to Yahoo Finance for history of each symbol
        >>> funct: 5    # save raw data from API response for later usage 
        >>> funct: 6    # convert raw data to json format to select data points 
        >>> funct: 7    # extract values from response for stock meta data frame
        >>> funct: 8    # extract values from response for stock indicator data frame
        >>> funct: 9    # write collect data in meta data frame to csv file
        >>> funct: 0    # write collect data in indicator data frame to csv file
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 0
        in_file = input("\nEnter input file path: ").replace("\"", "").strip()
        out_dir = input("\nEnter output folder path: ").replace("\"", "").strip()
        out_file = input("\nEnter output file name: ").replace(" ", "").strip()

        try:
            symbols_df = pd.read_csv(in_file, header=0, encoding="utf-8-sig")
        except:
            raise Exception(f"Cannot read file {in_file}")

        ### 1
        interval = input("\nEnter interval [1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo]: ").strip()
        if interval not in ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]: 
            raise Exception(f"Invalid interval {period}")
        
        period = input("\nEnter period [1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max]: ").strip()
        start_end_dates = False
        if period not in ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]: 
            if re.search(r"[\d]+[-][\d]+[-][\d]+[ ][\d]+[-][\d]+[-][\d]+", period) != None:
                start_end_dates = True
                period1 = period.split(" ")[0]
                period2 = period.split(" ")[1]
            else:
                raise Exception(f"Invalid range {period}")        

        adjusted = input("\nAdjust closing prices (Y/N): ").strip()
        if adjusted == "Y": close = "adjusted"
        else: close = "unadjusted"

        events = input("\nInclude events (Y/N): ").strip()
        if events == "Y": events = "div%7Csplit"
        else: events = ""
        
        prepost = input("\nInclude prepost (Y/N): ").strip()
        if prepost == "Y": prepost = "true"
        else: prepost = "false"

        ### 2
        params = {}
        params["interval"] = interval
        if start_end_dates == False:
            params["range"] = period
        else: 
            params["period1"] = period1
            params["period2"] = period2

        params["close"] = close
        params["events"] = events
        params["prepost"] = prepost

        timeout = YahooFinance.config_timeout()
        proxies = YahooFinance.config_proxies()

        ### 3
        meta_df = pd.DataFrame(columns=["ticker", "currency", "symbol", "exchangeName", \
            "instrumentType", "firstTradeDate", "regularMarketTime", "gmtoffset", "timezone", \
            "exchangeTimezoneName", "regularMarketPrice", "chartPreviousClose", "previousClose", \
            "scale", "priceHint", "currentTradingPeriodPreTimezone", "currentTradingPeriodPreStart", \
            "currentTradingPeriodPreEnd", "currentTradingPeriodPreGmtoffset", \
            "currentTradingPeriodRegularTimezone", "currentTradingPeriodRegularStart", \
            "currentTradingPeriodRegularEnd", "currentTradingPeriodRegularGmtoffset", \
            "currentTradingPeriodPostTimezone", "currentTradingPeriodPostStart", \
            "currentTradingPeriodPostEnd", "currentTradingPeriodPostGmtoffset", \
            "tradingPeriodsTimezone", "tradingPeriodsStart", "tradingPeriodsEnd", \
            "tradingPeriodsGmtoffset", "dataGranularity", "range", "validRanges"])

        indicators_df = pd.DataFrame(columns=[
            "ticker", "timestamp", "open", "high", "low", "close", "volume"])

        ### 4
        for _, series in symbols_df.iteritems():
            for _, symbol in series.iteritems(): 
                url = EP_HISTORY.replace("{symbol}", symbol)

                try:
                    print(f"\nCollect: {url}")
                    response = requests.get(
                        headers=USER_AGENT_HEADERS,
                        url=url,
                        params=params,
                        timeout=timeout,
                        proxies=proxies,
                    )            
                except:
                    error_msg = response["chart"]["error"]
                    raise Exception(f"Cannot request {error_msg}")    
        ### 5
                path = f"{out_dir}\\Datason @{symbol}History #-------------- .json"
                with open(path, mode="w", encoding="utf-8-sig") as file:
                    file.write(response.text)

                timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")
                os.rename(path, path.replace("#--------------", f"#{timestamp}"))
        ### 6
                try:
                    response = response.json()
                except:
                    raise Exception(f"Invalid JSON format {response}")
        ### 7
                values = [symbol]
                for column in meta_df.columns[1:]:
                    if column == "firstTradeDate":
                        try:
                            firstTradeDate = response["chart"]["result"][0]["meta"]["firstTradeDate"]
                            firstTradeDate = Convertion.epoch_to_date(firstTradeDate).strftime("%Y-%m-%d %H:%M:%S") 
                            values.append(firstTradeDate)
                        except:
                            values.append("—")
                        continue
                    if column == "regularMarketTime":
                        try:
                            regularMarketTime = response["chart"]["result"][0]["meta"]["regularMarketTime"]
                            regularMarketTime = Convertion.epoch_to_date(regularMarketTime).strftime("%Y-%m-%d %H:%M:%S")
                            values.append(regularMarketTime)
                        except:
                            values.append("—")
                        continue  
                    if column == "currentTradingPeriodPreTimezone":
                        try:
                            values.append(response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["pre"]["timezone"]) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodPreStart":
                        try:
                            pre_start = response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["pre"]["start"]
                            values.append(Convertion.epoch_to_date(pre_start).strftime("%Y-%m-%d %H:%M:%S"))
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodPreEnd":
                        try:
                            pre_end = response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["pre"]["end"]
                            values.append(Convertion.epoch_to_date(pre_end).strftime("%Y-%m-%d %H:%M:%S"))
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodPreGmtoffset":
                        try:
                            values.append(response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["pre"]["gmtoffset"])
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodRegularTimezone":
                        try:
                            values.append(response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["regular"]["timezone"]) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodRegularStart":
                        try:
                            reg_start = response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["regular"]["start"]
                            values.append(Convertion.epoch_to_date(reg_start).strftime("%Y-%m-%d %H:%M:%S")) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodRegularEnd":
                        try:
                            reg_end = response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["regular"]["end"]
                            values.append(Convertion.epoch_to_date(reg_end).strftime("%Y-%m-%d %H:%M:%S")) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodRegularGmtoffset":       
                        try:                     
                            values.append(response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["regular"]["gmtoffset"]) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodPostTimezone":
                        try:
                            values.append(response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["post"]["timezone"]) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodPostStart":
                        try:
                            pos_start = response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["post"]["start"]
                            values.append(Convertion.epoch_to_date(pos_start).strftime("%Y-%m-%d %H:%M:%S")) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodPostEnd":
                        try:
                            pos_end = response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["post"]["end"]
                            values.append(Convertion.epoch_to_date(pos_end).strftime("%Y-%m-%d %H:%M:%S")) 
                        except:
                            values.append("—")
                        continue
                    if column == "currentTradingPeriodPostGmtoffset":
                        try:
                            values.append(response["chart"]["result"][0]["meta"]["currentTradingPeriod"]["post"]["gmtoffset"]) 
                        except:
                            values.append("—")
                        continue
                    if column == "tradingPeriodsTimezone":
                        try:
                            values.append(response["chart"]["result"][0]["meta"]["tradingPeriods"][0][0]["timezone"])
                        except:
                            values.append("—")
                        continue
                    if column == "tradingPeriodsStart":
                        try:
                            pos_start = response["chart"]["result"][0]["meta"]["tradingPeriods"][0][0]["start"]
                            values.append(Convertion.epoch_to_date(pos_start).strftime("%Y-%m-%d %H:%M:%S")) 
                        except:
                            values.append("—")
                        continue
                    if column == "tradingPeriodsEnd":
                        try:
                            pos_end = response["chart"]["result"][0]["meta"]["tradingPeriods"][0][0]["end"]
                            values.append(Convertion.epoch_to_date(pos_end).strftime("%Y-%m-%d %H:%M:%S")) 
                        except:
                            values.append("—")
                        continue
                    if column == "tradingPeriodsGmtoffset":
                        try:
                            values.append(response["chart"]["result"][0]["meta"]["tradingPeriods"][0][0]["gmtoffset"]) 
                        except:
                            values.append("—")
                        continue
                    
                    try:
                        values.append(response["chart"]["result"][0]["meta"][column])
                    except:
                        values.append("—")
                    
                meta_df.loc[len(meta_df)] = values
        ### 8
                try: 
                    timestamps = response["chart"]["result"][0]["timestamp"]     
                except:
                    timestamps = "—"    
                try:
                    open_indexes = response["chart"]["result"][0]["indicators"]["quote"][0]["open"]
                except:
                    open_indexes = "—"    
                try:
                    high_indexes = response["chart"]["result"][0]["indicators"]["quote"][0]["high"]
                except:
                    high_indexes = "—"
                try:
                    low_indexes = response["chart"]["result"][0]["indicators"]["quote"][0]["low"]
                except:
                    low_indexes = "—"
                try: 
                    close_indexes = response["chart"]["result"][0]["indicators"]["quote"][0]["close"]
                except:
                    close_indexes = "—"
                try:
                    volumns = response["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
                except: 
                    volumns = "—"

                for index, value in enumerate(timestamps):
                    if timestamps[index] != "—":
                        timestamp = Convertion.epoch_to_date(value).strftime("%Y-%m-%d %H:%M:%S")
                    else: 
                        timestamp = "—"

                    indicators_df.loc[len(indicators_df)] = [
                        symbol, timestamp, open_indexes[index], high_indexes[index],\
                        low_indexes[index], close_indexes[index], volumns[index]]

        ### 9
        path = f"{out_dir}\\Dataset @{out_file}Meta #-------------- .csv"                
        meta_df.to_csv(path, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
        os.rename(path, path.replace("#--------------", f"#{timestamp}")) 

        ### 0
        path = f"{out_dir}\\Dataset @{out_file}Indicators #-------------- .csv"                
        indicators_df.to_csv(path, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
        os.rename(path, path.replace("#--------------", f"#{timestamp}")) 

        return None

    def collect_summary() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 0
        in_file = input("\nEnter input file path: ").replace("\"", "").strip()
        out_dir = input("\nEnter output folder path: ").replace("\"", "").strip()
        out_file = input("\nEnter output file name: ").replace(" ", "").strip()

        try:
            symbols_df = pd.read_csv(in_file, header=0, encoding="utf-8-sig")
        except:
            raise Exception(f"Cannot read file {in_file}")
        
        ### 1
        for i, module in enumerate(YahooFinance.summary_modules):
            print(f"{i+1} {module}")
        
        modules = input("\nSelect modules: ").strip()
        if modules == "all":
            modules = YahooFinance.summary_modules
        else:
            modules = modules.split(", ")
            for module in modules:
                if module not in YahooFinance.summary_modules:
                    raise Exception(f"Module not found {module}")

        ### 2
        if "assetProfile" in modules:
            asset_profile_df = pd.DataFrame(columns=["ticket", "address1", "address2", "city", \
                "state", "zip", "country", "phone", "fax", "website", "industry", "sector", \
                "longBusinessSummary", "fullTimeEmployees", "companyOfficers", "auditRisk", \
                "boardRisk", "compensationRisk", "shareHolderRightsRisk", "overallRisk", \
                "governanceEpochDate", "compensationAsOfEpochDate", "maxAge"])                

        if "defaultKeyStatistics" in modules:
            default_key_stats_df = pd.DataFrame(columns=["ticker", "maxAge", "priceHint", "enterpriseValue", \
                "forwardPE", "profitMargins", "floatShares", "sharesOutstanding", "sharesShort", \
                "sharesShortPriorMonth", "sharesShortPreviousMonthDate", "dateShortInterest", \
                "sharesPercentSharesOut", "heldPercentInsiders", "heldPercentInstitutions", \
                "shortRatio", "shortPercentOfFloat", "beta", "impliedSharesOutstanding", \
                "morningStarOverallRating", "morningStarRiskRating", "category", "bookValue", \
                "priceToBook", "annualReportExpenseRatio", "ytdReturn", "beta3Year", "totalAssets", \
                "yield", "fundFamily", "fundInceptionDate", "legalType", "threeYearAverageReturn", \
                "fiveYearAverageReturn", "priceToSalesTrailing12Months", "lastFiscalYearEnd", \
                "nextFiscalYearEnd", "mostRecentQuarter", "earningsQuarterlyGrowth", \
                "revenueQuarterlyGrowth", "netIncomeToCommon", "trailingEps", "forwardEps", \
                "pegRatio", "lastSplitFactor", "lastSplitDate", "enterpriseToRevenue", \
                "enterpriseToEbitda", "52WeekChange", "SandP52WeekChange", "lastDividendValue", \
                "lastDividendDate", "lastCapGain", "annualHoldingsTurnover"])                

        if "recommendationTrend" in modules:
            recommendation_trend_df = pd.DataFrame(columns=[
                "ticker", "period", "strongBuy", "buy", "hold", "sell", "strongSell", "maxAge"])                

        if "financialData" in modules:
            financial_data_df = pd.DataFrame(columns=["ticker", "maxAge", "currentPrice", \
            "targetHighPrice", "targetLowPrice", "targetMeanPrice", "targetMedianPrice", \
            "recommendationMean", "recommendationKey", "numberOfAnalystOpinions", "totalCash", \
            "totalCashPerShare", "ebitda", "totalDebt", "quickRatio", "currentRatio", \
            "totalRevenue", "debtToEquity", "revenuePerShare", "returnOnAssets", "returnOnEquity", \
            "grossProfits", "freeCashflow", "operatingCashflow", "earningsGrowth", "revenueGrowth", \
            "grossMargins", "ebitdaMargins", "operatingMargins", "profitMargins", "financialCurrency"])                

        if "majorHoldersBreakdown" in modules:
            major_holders_df = pd.DataFrame(columns=["ticker", "maxAge", "insidersPercentHeld", \
                "institutionsPercentHeld", "institutionsFloatPercentHeld", "institutionsCount"])                

        if "earnings" in modules:
            earnings_chart_df = pd.DataFrame(columns=["ticker", "maxAge", "quarterlyDate", \
                "quarterlyActual", "quarterlyEstimate", "currentQuarterEstimate", \
                "currentQuarterEstimateDate", "currentQuarterEstimateYear", "earningsDate", \
                "financialCurrency"])                
            financials_chart_df = pd.DataFrame(columns=["ticker", "maxAge", "yearlyDate", \
                "yearlyRevenue", "yearlyEarnings", "quarterlyDate", "quarterlyRevenue", \
                "quarterlyEarnings", "financialCurrency"])     

        if "earningsHistory" in modules:
            earnings_history_df = pd.DataFrame(columns=["ticker", "maxAge", "epsActual", \
                "epsEstimate", "epsDifference", "surprisePercent", "quarter", "period"])  

        if "earningsTrend" in modules:
            earnings_trend_df = pd.DataFrame(columns=["ticker", "maxAge", "period", "endDate", \
                "growth", "avgEarningsEstimate", "lowEarningsEstimate", "highEarningsEstimate", \
                "yearAgoEps", "numberOfAnalystsEarningsEstimate", "growthEarningsEstimate", \
                "avgRevenueEstimate", "lowRevenueEstimate", "highRevenueEstimate", \
                "numberOfAnalystsRevenueEstimate", "yearAgoRevenue", "growthRevenueEstimate", \
                "epsTrendCurrent", "epsTrend7DAgo", "epsTrend30DAgo", "epsTrend60DAgo", "epsTrend90DAgo", \
                "epsRevisionsUp7D", "epsRevisionsUp30D", "epsRevisionsDown30D", "epsRevisionsDown90D"]) 

        if "indexTrend" in modules:
            index_trend_df = pd.DataFrame(columns=["ticker", "maxAge", "symbol", "peRatio", \
                "pegRatio", "estimatePeriod", "estimateGrowth"])   

        if "industryTrend" in modules:
            pass               

        if "netSharePurchaseActivity" in modules:
            net_share_purchase_df = pd.DataFrame(columns=["ticker", "maxAge", "period", \
                "buyInfoCount", "buyInfoShares", "sellInfoCount", "sellInfoShares", "netInfoCount", \
                "netInfoShares", "netPercentInsiderShares", "totalInsiderShares"])

        if "sectorTrend" in modules:
            pass    

        if "insiderHolders" in modules:
            insider_holders_df = pd.DataFrame(columns=["ticker", "maxAge", "name", "relation", \
                "url", "transactionDescription", "latestTransDate", "positionDirect", \
                "positionDirectDate"])         

        if "upgradeDowngradeHistory" in modules:
            upgrade_downgrade_df = pd.DataFrame(columns=["ticker", "epochGradeDate", "firm", \
                "toGrade", "fromGrade", "action"])         

        ### 3
        timeout = YahooFinance.config_timeout()
        proxies = YahooFinance.config_proxies()

        ### 4
        for _, series in symbols_df.iteritems():
            for _, symbol in series.iteritems():
                url = EP_SUMMARY\
                    .replace("{symbol}", symbol)\
                    .replace("{modules}", ",".join(modules))

                try:
                    print(f"\nCollect: {url}")
                    response = requests.get(
                        headers=USER_AGENT_HEADERS,
                        url=url,
                        timeout=timeout,
                        proxies=proxies,
                    )            
                except:
                    raise Exception(f"Cannot request {url}")
        ### 6
                path = f"{out_dir}\\Datason @{symbol}Summary #-------------- .json"
                with open(path, mode="w", encoding="utf-8-sig") as file:
                    file.write(response.text)

                timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")
                os.rename(path, path.replace("#--------------", f"#{timestamp}"))
        ### 6
                try:
                    response = response.json()
                except:
                    raise Exception(f"Invalid JSON format {response}")
        ### 7                
                if "assetProfile" in modules:
                    try:
                        result = response["quoteSummary"]["result"][0]["assetProfile"]
                        values = [symbol]
                        for column in asset_profile_df.columns[1:]:
                            if column == "companyOfficers":
                                officers = [item["name"] for item in result["companyOfficers"]]
                                values.append(", ".join(officers)) 
                                continue

                            try: 
                                values.append(result[column])
                            except:
                                values.append("—")                       

                        asset_profile_df.loc[len(asset_profile_df)] = values                    
                    except: pass
        ### 8
                if "defaultKeyStatistics" in modules:
                    try:
                        result = response["quoteSummary"]["result"][0]["defaultKeyStatistics"]
                        values = [symbol]
                        for column in default_key_stats_df.columns[1:]:
                            if column == "maxAge":
                                try:
                                    values.append(result["maxAge"])
                                except:
                                    values.append("—") 
                                continue

                            try: 
                                values.append(result[column]["raw"])
                            except:
                                values.append("—")  

                        default_key_stats_df.loc[len(default_key_stats_df)] = values
                    except: pass
        ### 9
                if "recommendationTrend" in modules:
                    try:
                        results = response["quoteSummary"]["result"][0]["recommendationTrend"]["trend"]
                        for result in results:
                            values = [symbol]
                            for column in recommendation_trend_df.columns[1:]:
                                if column == "maxAge":
                                    try:
                                        values.append(
                                            response["quoteSummary"]["result"][0]["recommendationTrend"]["maxAge"])
                                    except:
                                        values.append("—") 
                                    continue

                                try: 
                                    values.append(result[column])
                                except:
                                    values.append("—")  

                        recommendation_trend_df.loc[len(recommendation_trend_df)] = values
                    except: pass
        ### 0   
                if "financialData" in modules:
                    try:
                        result = response["quoteSummary"]["result"][0]["financialData"]
                        values = [symbol]
                        for column in financial_data_df.columns[1:]:
                            if column == "maxAge":
                                maxAge = response["quoteSummary"]["result"][0]["financialData"]["maxAge"] 
                                values.append(maxAge)
                                continue

                            if column == "financialCurrency":
                                currency = response["quoteSummary"]["result"][0]["financialData"]["financialCurrency"] 
                                values.append(currency)
                                continue

                            try: 
                                values.append(result[column]["raw"])
                            except:
                                values.append("—")  

                        financial_data_df.loc[len(financial_data_df)] = values
                    except: pass                        
        ### 1
                if "majorHoldersBreakdown" in modules:
                    try:
                        result = response["quoteSummary"]["result"][0]["majorHoldersBreakdown"]
                        values = [symbol]
                        for column in major_holders_df.columns[1:]:
                            if column == "maxAge":
                                maxAge = response["quoteSummary"]["result"][0]["majorHoldersBreakdown"]["maxAge"] 
                                values.append(maxAge)
                                continue

                            try: 
                                values.append(result[column]["raw"])
                            except:
                                values.append("—")  

                        major_holders_df.loc[len(major_holders_df)] = values
                    except: pass
        ### 2
                if "earnings" in modules:
                    if len(earnings_chart_df.columns) != 0:
                        try:
                            quarterly_earnings = response["quoteSummary"]["result"][0]["earnings"]["earningsChart"]["quarterly"]
                        except:
                            quarterly_earnings = "—"
                        try:
                            maxAge = response["quoteSummary"]["result"][0]["earnings"]["maxAge"]  
                        except: 
                            maxAge = "—"            
                        try:
                            currency = response["quoteSummary"]["result"][0]["earnings"]["financialCurrency"] 
                        except: 
                            currency = "—"            
                        try: 
                            estimate = response["quoteSummary"]["result"][0]["earnings"]["earningsChart"]["currentQuarterEstimate"]["raw"]
                        except:
                            estimate = "—"
                        try:
                            estimateDate = response["quoteSummary"]["result"][0]["earnings"]["earningsChart"]["currentQuarterEstimateDate"]
                        except:
                            estimateDate = "—"
                        try:
                            estimateYear = response["quoteSummary"]["result"][0]["earnings"]["earningsChart"]["currentQuarterEstimateYear"]
                        except: 
                            estimateYear = "—"
                        try:
                            earningDates = response["quoteSummary"]["result"][0]["earnings"]["earningsChart"]["earningsDate"]
                            earningDates = [earningDates[i]["raw"] for i in range(len(earningDates))]
                            if len(earningDates) == 0: earningDates = "—"
                        except:
                            earningDates = "—"

                        for i in range(4):
                            try:
                                quarterlyDate = quarterly_earnings[i]["date"]            
                            except:
                                quarterlyDate = "—"
                            try:
                                quarterlyActual = quarterly_earnings[i]["actual"]["raw"]
                            except: 
                                quarterlyActual = "—"
                            try:
                                quarterlyEstimate = quarterly_earnings[i]["estimate"]["raw"]
                            except: 
                                quarterlyEstimate = "—"

                            earnings_chart_df.loc[len(earnings_chart_df)] = [
                                symbol, maxAge, quarterlyDate, quarterlyActual, quarterlyEstimate, \
                                estimate, estimateDate, estimateYear, earningDates, currency
                            ]

                    if len(financials_chart_df.columns) != 0:
                        try:
                            yearly_financials = response["quoteSummary"]["result"][0]["earnings"]["financialsChart"]["yearly"]
                        except:
                            yearly_financials = "—"
                        try:
                            quarterly_financials = response["quoteSummary"]["result"][0]["earnings"]["financialsChart"]["quarterly"]
                        except:
                            quarterly_financials = "—"

                        try:
                            maxAge = response["quoteSummary"]["result"][0]["earnings"]["maxAge"] 
                        except:
                            maxAge = "—"
                        try:
                            currency = response["quoteSummary"]["result"][0]["earnings"]["financialCurrency"] 
                        except:
                            maxAge = "—"                                           

                        for i in range(4):
                            try:
                                yearly_date = yearly_financials[i]["date"]       
                            except:
                                yearly_date = "—"
                            try:
                                yearly_revenue = yearly_financials[i]["revenue"]["raw"]                       
                            except:
                                yearly_date = "—"
                            try:
                                yearly_earnings = yearly_financials[i]["earnings"]["raw"]
                            except:
                                yearly_date = "—"

                            try:
                                quarterly_date = quarterly_financials[i]["date"]                       
                            except:
                                quarterly_date = "—"
                            try:
                                quarterly_revenue = quarterly_financials[i]["revenue"]["raw"]                        
                            except:
                                quarterly_revenue = "—"
                            try:
                                quarterly_earnings = quarterly_financials[i]["earnings"]["raw"]
                            except:
                                quarterly_earnings = "—"

                            financials_chart_df.loc[len(earnings_chart_df)] = [
                                symbol, maxAge, yearly_date, yearly_revenue, yearly_earnings, \
                                quarterly_date, quarterly_revenue, quarterly_earnings, currency
                            ]
        ### 3
                if "earningsHistory" in modules:
                    try:
                        results = response["quoteSummary"]["result"][0]["earningsHistory"]["history"]
                        for result in results:
                            values = [symbol]
                            for column in earnings_history_df.columns[1:]:
                                if column == "maxAge":
                                    try: 
                                        values.append(result["maxAge"] )
                                    except:
                                        values.append("—")
                                    continue

                                if column == "period":
                                    try:
                                        values.append(result["period"] )
                                    except:
                                        values.append("—")
                                    continue

                                try: 
                                    values.append(result[column]["raw"])
                                except:
                                    values.append("—")  

                            earnings_history_df.loc[len(earnings_history_df)] = values   
                    except: pass
        ### 4
                if "earningsTrend" in modules:
                    try:
                        results = response["quoteSummary"]["result"][0]["earningsTrend"]["trend"]
                        for result in results:
                            values = [symbol]

                            try: values.append(result["maxAge"])
                            except: values.append("—")
                            try: values.append(result["period"])
                            except: values.append("—")
                            try: values.append(result["endDate"])
                            except: values.append("—")
                            try: values.append(result["growth"]["raw"])
                            except: values.append("—")

                            try: values.append(result["earningsEstimate"]["avg"]["raw"])
                            except: values.append("—")
                            try: values.append(result["earningsEstimate"]["low"]["raw"])
                            except: values.append("—")
                            try: values.append(result["earningsEstimate"]["high"]["raw"])
                            except: values.append("—")
                            try: values.append(result["earningsEstimate"]["yearAgoEps"]["raw"])
                            except: values.append("—")
                            try: values.append(result["earningsEstimate"]["numberOfAnalysts"]["raw"])
                            except: values.append("—")
                            try: values.append(result["earningsEstimate"]["growth"]["raw"])
                            except: values.append("—")

                            try: values.append(result["revenueEstimate"]["avg"]["raw"])
                            except: values.append("—")
                            try: values.append(result["revenueEstimate"]["low"]["raw"])
                            except: values.append("—")
                            try: values.append(result["revenueEstimate"]["high"]["raw"])
                            except: values.append("—")
                            try: values.append(result["revenueEstimate"]["numberOfAnalysts"]["raw"])
                            except: values.append("—")
                            try: values.append(result["revenueEstimate"]["yearAgoRevenue"]["raw"])
                            except: values.append("—")
                            try: values.append(result["revenueEstimate"]["growth"]["raw"])
                            except: values.append("—")

                            try: values.append(result["epsTrend"]["current"]["raw"])
                            except: values.append("—")
                            try: values.append(result["epsTrend"]["7daysAgo"]["raw"])
                            except: values.append("—")
                            try: values.append(result["epsTrend"]["30daysAgo"]["raw"])
                            except: values.append("—")
                            try: values.append(result["epsTrend"]["60daysAgo"]["raw"])
                            except: values.append("—")
                            try: values.append(result["epsTrend"]["90daysAgo"]["raw"])
                            except: values.append("—")

                            try: values.append(result["epsRevisions"]["upLast7days"]["raw"])
                            except: values.append("—")
                            try: values.append(result["epsRevisions"]["upLast30days"]["raw"])
                            except: values.append("—")
                            try: values.append(result["epsRevisions"]["downLast30days"]["raw"])
                            except: values.append("—")
                            try: values.append(result["epsRevisions"]["downLast90days"]["raw"])
                            except: values.append("—")

                            earnings_trend_df.loc[len(earnings_trend_df)] = values
                    except: pass 
        ### 5
                if "indexTrend" in modules:
                    try:
                        results = response["quoteSummary"]["result"][0]["indexTrend"]["estimates"]
                        for result in results:
                            values = [symbol]
                            try: values.append(response["quoteSummary"]["result"][0]["indexTrend"]["maxAge"]) 
                            except: values.append("—")
                            try: values.append(response["quoteSummary"]["result"][0]["indexTrend"]["symbol"]) 
                            except: values.append("—")
                            try: values.append(response["quoteSummary"]["result"][0]["indexTrend"]["peRatio"]["raw"]) 
                            except: values.append("—")
                            try: values.append(response["quoteSummary"]["result"][0]["indexTrend"]["pegRatio"]["raw"]) 
                            except: values.append("—")
                            try: values.append(result["period"]) 
                            except: values.append("—")
                            try: values.append(result["growth"]["raw"]) 
                            except: values.append("—")

                        index_trend_df.loc[len(index_trend_df)] = values
                    except: pass
        ### 6
                if "netSharePurchaseActivity" in modules:
                    try:
                        result = response["quoteSummary"]["result"][0]["netSharePurchaseActivity"]
                        values = [symbol]
                        for column in net_share_purchase_df.columns[1:]:
                            if column == "maxAge":
                                try: 
                                    values.append(result["maxAge"])
                                except:
                                    values.append("—")
                                continue
                        
                            if column == "period":
                                try: 
                                    values.append(result["period"])
                                except:
                                    values.append("—")
                                continue

                            try: 
                                values.append(result[column]["raw"])
                            except:
                                values.append("—")  

                        net_share_purchase_df.loc[len(net_share_purchase_df)] = values   
                    except: pass  
        ### 7
                if "insiderHolders" in modules:
                    try:
                        results = response["quoteSummary"]["result"][0]["insiderHolders"]["holders"]
                        for result in results:
                            values = [symbol]
                            try: values.append(result["maxAge"])
                            except: values.append("—")
                            try: values.append(result["name"])
                            except: values.append("—")
                            try: values.append(result["relation"])
                            except: values.append("—")
                            try: values.append(result["url"])
                            except: values.append("—")
                            try: values.append(result["transactionDescription"])
                            except: values.append("—")
                            try: values.append(result["latestTransDate"]["raw"])
                            except: values.append("—")
                            try: values.append(result["positionDirect"]["raw"])
                            except: values.append("—")
                            try: values.append(result["positionDirectDate"]["raw"])
                            except: values.append("—")
                            
                            insider_holders_df.loc[len(insider_holders_df)] = values
                    except: pass
        ### 8
                if "upgradeDowngradeHistory" in modules:
                    try:
                        results = response["quoteSummary"]["result"][0]["upgradeDowngradeHistory"]["history"]
                        for result in results:
                            values = [symbol]
                            for column in upgrade_downgrade_df.columns[1:]:
                                try: 
                                    values.append(result[column])
                                except:
                                    values.append("—")
                            
                            upgrade_downgrade_df.loc[len(upgrade_downgrade_df)] = values
                    except: pass
        ### 
        if "assetProfile" in modules:
            path = f"{out_dir}\\Dataset @{out_file}AssetProfile #-------------- .csv"                
            asset_profile_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))    

        ### 
        if "defaultKeyStatistics" in modules:
            path = f"{out_dir}\\Dataset @{out_file}DefaultKeyStats #-------------- .csv"                
            default_key_stats_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))   
        
        ###
        if "recommendationTrend" in modules:
            path = f"{out_dir}\\Dataset @{out_file}RecommendationTrend #-------------- .csv"                
            recommendation_trend_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))  

        ###
        if "financialData" in modules:
            path = f"{out_dir}\\Dataset @{out_file}FinancialData #-------------- .csv"                
            financial_data_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))    

        ###
        if "majorHoldersBreakdown" in modules:
            path = f"{out_dir}\\Dataset @{out_file}HoldersBreakDown #-------------- .csv"                
            major_holders_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}")) 
               
        ###
        if "earnings" in modules:
            path = f"{out_dir}\\Dataset @{out_file}Earnings #-------------- .csv"                
            earnings_chart_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))

            path = f"{out_dir}\\Dataset @{out_file}Financials #-------------- .csv"                
            financials_chart_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))    

        ###
        if "earningsHistory" in modules:
            path = f"{out_dir}\\Dataset @{out_file}EarningsHistory #-------------- .csv"                
            earnings_history_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))

        ###
        if "earningsTrend" in modules:
            path = f"{out_dir}\\Dataset @{out_file}EarningsTrend #-------------- .csv"                
            earnings_trend_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))

        ###
        if "indexTrend" in modules:
            path = f"{out_dir}\\Dataset @{out_file}IndexTrend #-------------- .csv"                
            index_trend_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))

        ###
        if "netSharePurchaseActivity" in modules:
            path = f"{out_dir}\\Dataset @{out_file}NetSharePurchase #-------------- .csv"                
            net_share_purchase_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))

        ###
        if "insiderHolders" in modules:
            path = f"{out_dir}\\Dataset @{out_file}InsiderHolders #-------------- .csv"                
            insider_holders_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))
        
        ###
        if "upgradeDowngradeHistory" in modules:
            path = f"{out_dir}\\Dataset @{out_file}UpgradeDowngradeHistory #-------------- .csv"                
            upgrade_downgrade_df.to_csv(path, index=False, encoding="utf-8-sig")

            timestamp = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d%H%M%S")      
            os.rename(path, path.replace("#--------------", f"#{timestamp}"))

        return None
