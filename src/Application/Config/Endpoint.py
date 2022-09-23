# YAHOO FINANCE ENDPOINTS

USER_AGENT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

URL_HOMEPAGE = "https://finance.yahoo.com"
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
EP_QUOTE = "https://query1.finance.yahoo.com/v6/finance/quote?symbols={symbol},{symbol}"
EP_QUOTE_ALT = "https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol},{symbol}"
EP_OPTIONS = "https://query1.finance.yahoo.com/v7/finance/options/{symbol}"
EP_DOWNLOAD = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
EP_HISTORY = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}" 
EP_SUMMARY = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules={modules}"
