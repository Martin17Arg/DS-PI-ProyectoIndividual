def load_ticker(ticker):
    
    import pandas as pd
    import numpy as np
    import json

    config = json.load(open('config.json'))
    
    filename = f'{config["DIRECTORIO_DATASETS"]}/{ticker}.csv'
    df = pd.read_csv(filename)
    
    # Series configuration
    df.Date = df.Date.astype('datetime64')
    
    # Adding columns
    df['Gap'] = np.log(df['Open']/df['Close'].shift(1)).fillna(0)
    df['Intra'] = np.log(df['Close']/df['Open'].shift(1)).fillna(0)
    df['Volatilidad'] = df['Adj Close'].pct_change().fillna(0)
    
    df['Weekday'] = df.Date.dt.dayofweek
    df['Weekday name'] = df.Date.dt.day_name()
    #df['Week number'] = df.Date.dt.isocalendar().week
    #df['Year'] = df.Date.dt.year

    # Sort values
    df = df.sort_values(by = 'Date', ascending = True)

    return df

def load_all_tickers():

    import pandas as pd
    import numpy as np
    import json, os

    config = json.load(open('config.json'))

    dfs = []
    
    for filename in os.listdir(config["DIRECTORIO_DATASETS"]):
        
        ticker = filename.split('.')[0]
        df_ticker  = load_ticker(ticker)
        df_ticker['Ticker'] = ticker
        
        dfs.append(df_ticker)
        
    df = pd.concat(dfs, ignore_index=True)

    return df

def comparar_semanas(df, week, year, ticker, medida = 'Gap'):

    '''
    Retorna el día con mejor rendimiento para una determinada semana
    de un determinado año para un determinado ticker.
    La medida es el tipo de rendimiento (Gap [default] o Intra)
    '''

    import pandas as pd

    mask = (df['Week number'] == week) & (df['Year'] == year) & (df['Ticker'] == ticker)

    return df[mask].groupby('Weekday name')[medida].mean().idxmax()