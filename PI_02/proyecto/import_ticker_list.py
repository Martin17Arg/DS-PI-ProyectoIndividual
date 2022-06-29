import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import json

def main():
    
    print('1. Cargando configuración...')
    config = json.load(open('config.json'))
    
    print('2. Request a Wikipedia...')
    response=requests.get(config['URL_TICKERS'])

    print('3. Soup...')
    soup = BeautifulSoup(response.text,features="lxml")
    tickers_table = soup.find('table',{'id':config['TABLE_ID_TICKERS']})  

    print('4. Cargando dataframe...')
    tickers = pd.read_html(str(tickers_table))
    tickers = pd.DataFrame(tickers[0])
    
    print(f'5. Exportando dataframe... ({config["ARCHIVO_LISTA_TICKERS"]})')    
    tickers.to_csv(config['ARCHIVO_LISTA_TICKERS'],index=False)

    print('6. Finalizado.')

if __name__ == '__main__':
    main()