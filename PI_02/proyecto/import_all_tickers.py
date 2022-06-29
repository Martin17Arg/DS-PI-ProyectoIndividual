import pandas_datareader.data as web
import pandas as pd
import os, json
import datetime as dt

def main():
    
    print('1. Cargando configuración...')
    config = json.load(open('config.json'))
    
    print('2. Leyendo lista de tickers...')
    tickers = pd.read_csv(config['ARCHIVO_LISTA_TICKERS'], usecols=['Symbol'])

    # Corrección de separador por punto a guión.
    tickers.Symbol = tickers.Symbol.apply(lambda x: x.replace('.','-'))

    print('3. Importar cada ticker:')
    for ticker in  tickers.Symbol:
        filename = f'{ticker}.csv'
        if filename not in os.listdir(config["DIRECTORIO_DATASETS"]):
            try:
                df = web.DataReader(ticker, 'yahoo', start_date, end_date)
                df.to_csv(f'{config["DIRECTORIO_DATASETS"]}/{ticker}.csv',index='False')     
            except:
                print(f'WARNING: Error carga ({ticker})')
    
    print('4. Finalizado.')

if __name__ == '__main__':
    main()