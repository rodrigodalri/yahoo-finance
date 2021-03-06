from pandas_datareader import data as pdr
from matplotlib import pyplot as plt
import yfinance as yf
import seaborn as sns
import pandas as pd
import time
import toml

def plot_price_time(data_price, assets_name=str):
    """[summary]

    Args:
        data_price ([type]): [description]
        assets_name ([type], optional): [description]. Defaults to str.
    """
    tickers = list(data_price.drop(["Date"], axis = 1).columns)
    plt.clf() 
    plt.figure(figsize=(32,12))

    for i in tickers:
            plt.plot(data_price["Date"], data_price[i])
    plt.legend(tickers)
    plt.grid()
    plt.title("Price x Time", fontsize = 15)
    plt.savefig(f"plots/{assets_name}_priceXtime.png")
 
def plot_heatmap_correlation(data_price, assets_name=str):
    """[summary]

    Args:
        data_price ([type]): [description]
        assets_name ([type], optional): [description]. Defaults to str.
    """
    sns.heatmap(data_price.corr(), annot = True)
    plt.savefig(f"plots/{assets_name}_correlation.png")


def plot_return_time(data_price, tickers=list, assets_name=str):
    """[summary]

    Args:
        data_price ([type]): [description]
        tickers ([type], optional): [description]. Defaults to list.
        assets_name ([type], optional): [description]. Defaults to str.
    """
    returns = pd.DataFrame()
    for i in tickers:
        returns[i] = data_price[i].pct_change()
    returns["Date"] = data_price["Date"]

    returns.describe()

    return_sum = pd.DataFrame()
    for ticker in tickers:
        return_sum[ticker] = (returns[ticker]+1).cumprod()
    return_sum["Date"] = returns["Date"]

    plt.clf() 
    plt.figure(figsize=(32,12))
    plt.plot(return_sum["Date"], return_sum.drop(["Date"], axis = 1), alpha = 0.9)
    plt.legend(tickers)
    plt.title("Returns x Time", fontsize = 15)
    plt.grid()
    plt.savefig(f"plots/{assets_name}_returnsXtime.png")

def get_yahoo_data(tickers=list):
    """[summary]

    Args:
        tickers ([type], optional): [description]. Defaults to list.

    Returns:
        [type]: [description]
    """
    data_price = pd.DataFrame()
    data = []

    # TODO: date by parameter
    for i in tickers:
        try:
            data_price[i] = pdr.get_data_yahoo(i,"01/01/2019")["Adj Close"]
            data.append(yf.Ticker(i))
        except:
            time.sleep(10)
            data_price[i] = pdr.get_data_yahoo(i,"01/01/2019")["Adj Close"]
            data.append(yf.Ticker(i))
            
    data_price.reset_index(inplace = True)
    
    return (data_price, data)

def parse_ticker_data(ticker=str):
    """[summary]

    Args:
        ticker ([type], optional): [description]. Defaults to str.

    Returns:
        [type]: [description]
    """
    # TODO: parse info and store in db 
    
    # get stock info
    #msft.info
    
    # get historical market data
    #msft.history(period="max")
    
    # show actions (dividends, splits)
    #msft.actions
    
    return 0

def main():
    """[summary]
    """
    assets = toml.load("assets.toml", _dict=dict)
    
    for key in assets.keys():
        if key != "title":
            assets_name = assets[key]["name"]
            tickers = assets[key]["tickers"]
            data_price,data = get_yahoo_data(tickers=tickers)

            plot_heatmap_correlation(data_price=data_price,assets_name=assets_name)
            plot_price_time(data_price=data_price,assets_name=assets_name)
            plot_return_time(data_price=data_price,tickers=tickers,assets_name=assets_name)

if __name__== "__main__":
    main()