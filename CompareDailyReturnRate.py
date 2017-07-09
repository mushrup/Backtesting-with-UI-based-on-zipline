from zipline.api import *
from matplotlib import style
from sys import argv
import os

style.use('ggplot')
print(str(argv))
file = open('pink_orange.txt','r')
pink,orange = str(file.readline()).split()
file.close()
count = 0
Int_price = 0
Int_price_b = 0
Int_price_bm = 0
Return_yesterday = 0
Total_revenue = 0
Return_yesterday_b = 0
Total_revenue_b = 0
Revenue_rate = 0
Revenue_rate_b = 0
    
def initialize(context):
    print(pink)
    print(orange)
    context.sab = symbol(pink)
    context.stx = symbol(orange)
    context.spy = symbols('AAPL', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AKAM', 'ALTR', 'ALXN', 'AMAT', 'AMGN', 'AMZN', 'ATVI', 'AVGO', 'BBBY', 'BIDU', 'BIIB', 'BRCM', 'CA', 'CELG', 'CERN', 'CHKP', 'CHRW', 'CHTR', 'CMCSA', 'COST', 'CSCO', 'CTRX', 'CTSH', 'CTXS', 'DELL', 'DISCA', 'DLTR', 'DTV', 'EBAY', 'EQIX', 'ESRX', 'EXPD', 'EXPE', 'FAST', 'FB', 'FFIV', 'FISV', 'FOSL', 'FOXA', 'GILD', 'GMCR', 'GOLD', 'GOOG', 'GRMN', 'HSIC', 'INTC', 'INTU', 'ISRG', 'KLAC', 'KRFT', 'LBTYA', 'LINTA', 'LLTC', 'LMCA', 'MAT', 'MCHP', 'MDLZ', 'MNST', 'MSFT', 'MU', 'MXIM', 'MYL', 'NFLX', 'NTAP', 'NUAN', 'NVDA', 'ORLY', 'PAYX', 'PCAR', 'PCLN', 'QCOM', 'REGN', 'ROST', 'SBAC', 'SBUX', 'SHLD', 'SIAL', 'SIRI', 'SNDK', 'SPLS', 'SRCL', 'STX', 'SYMC', 'TSLA', 'TXN', 'VIAB', 'VOD', 'VRSK', 'VRTX', 'WDC', 'WFM', 'WYNN', 'XLNX', 'XRAY', 'YHOO')

def handle_data(context, data):
    # Save values for later inspection
    global count
    global Int_price
    global Int_price_b
    global Int_price_bm
    global Return_yesterday
    global Total_revenue
    global Return_yesterday_b
    global Total_revenue_b
    global Revenue_rate
    global Revenue_rate_b
    price_sab = data.history(context.sab, "price", bar_count=2, frequency="1d")
    pct_change_sab = (price_sab.ix[-1] - price_sab.ix[0]) / price_sab.ix[0]
    
    price_stx = data.history(context.stx, "price", bar_count=2, frequency="1d")
    pct_change_stx = (price_stx.ix[-1] - price_stx.ix[0]) / price_stx.ix[0]
    
    price_spy = data.history(context.spy,"price", bar_count=2, frequency = "1d")
    price_bm = price_spy.mean(axis=1)
    
    Return_sab=price_sab.ix[-1] - price_sab.ix[0]
    Return_stx=price_stx.ix[-1] - price_stx.ix[0]

    if count == 0:
        Int_price = price_sab.ix[0]
        Int_price_b = price_stx.ix[0]
        Int_price_bm = price_bm.ix[0]
        count = 1

    if Return_yesterday >= 0:
        Total_revenue = Total_revenue + Return_sab
        Revenue_rate = Total_revenue /Int_price
    
    if Return_yesterday < 0:
        Total_revenue = Total_revenue #- Return_sab
        Revenue_rate = Total_revenue/Int_price
    
    Return_yesterday = Return_sab
    
    if Return_yesterday_b >= 0:
        Total_revenue_b = Total_revenue_b + Return_stx 
        Revenue_rate_b = Total_revenue_b/Int_price_b
        
    if Return_yesterday_b < 0:
        Total_revenue_b = Total_revenue_b #- Return_stx
        Revenue_rate_b = Total_revenue_b/Int_price_b
    
    Return_yesterday_b = Return_stx
    
    Return_bm = price_bm.ix[0] / Int_price_bm - 1
    
    record(SAB=pct_change_sab, STX=pct_change_stx, Sum = Revenue_rate, Sum_b = Revenue_rate_b, BM=Return_bm)

def analyze(context=None, results=None): 
    import matplotlib.pyplot as plt
    fig, (ax1) = plt.subplots(num=None, figsize=(10, 5), dpi=80, facecolor='w', edgecolor='k')
    ax1.plot(results.STX,label=orange)
    ax1.plot(results.SAB,label=pink)
    ax1.set_ylabel('%')
    ax1.set_title('Daily Price Percentage Change')
    
    fig, (ax2) = plt.subplots(num=None, figsize=(10, 5), dpi=80, facecolor='w', edgecolor='k')
    ax2.plot(results.Sum,label=pink)
    ax2.plot(results.Sum_b,label=orange)
    ax2.plot(results.BM,label='benchmark')
    ax2.set_ylabel('%')
    ax2.set_title('Keep Full')
    plt.legend()
    plt.show()