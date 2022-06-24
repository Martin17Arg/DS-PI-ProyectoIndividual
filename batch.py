import pandas as pd
import seaborn as sns
import os
from auxiliares_batch import verificar_calidad, bar_calidad,box_plot_calidad
import json

def main():
    # Configuración
    tablas = ['Clientes', 
        'Compra', 
        'Gasto', 
        'Localidades', 
        'Proveedores', 
        'Sucursales', 
        'Venta', 
        'Tipos De Gasto',
        'Canal de venta'
        ] # Catálogo de tablas

    DIRECTORIO = 'Datasets'
    DIRECTORIO_IMAGES = 'img'
    archivos_a_cargar = [x for x in os.listdir(f'./{DIRECTORIO}') if (x.split('.')[1] == 'csv') | (x.split('.')[1] == 'xlsx')] # Lista de archivos a cargar
    upper_tablas = [x[:4].upper() for x in tablas] # Lista para matchear tablas y archivos

    # Cargar configuración para read_csv
    with open('./Input/config.json') as config_file: # Cargar configuraciones particulares para cada CSV
        config = json.load(config_file)

    # Iterar sobre todas las tablas
    for archivo in archivos_a_cargar:

        # Identificar tabla
        nombre_tabla = tablas[upper_tablas.index(archivo[:4].upper())]
        print(f'## *Tabla:* {nombre_tabla}')
        print(f'*Archivo:* {archivo}')
        print()
        
        # Cargar dataframe

        if archivo.split('.')[1] == 'xlsx':
            df = pd.read_excel(f'./{DIRECTORIO}/{archivo}')
        else:
            df = pd.read_csv(f'./{DIRECTORIO}/{archivo}', 
                delimiter = config[archivo]['delimiter'], 
                decimal = config[archivo]['decimal'],
                encoding = config[archivo]['encoding'],
                parse_dates = config[archivo]['parse_dates'],
                infer_datetime_format = config[archivo]["infer_datetime_format"],
                )

            if config[archivo]["convert_float"]:
                for col in config[archivo]["convert_float"]:
                    try:
                        df[col] = df[col].apply(lambda x : x.replace(',','.'))
                    except:
                        pass

                    df[col] = pd.to_numeric(df[col],errors='coerce')
                    df[col] = df[col].astype('float')
            
            if config[archivo]["convert_integer"]:
                for col in config[archivo]["convert_integer"]:
                    df[col] = df[col].astype('int64',errors = 'ignore')
        
        print(df.info())
        print()
     
        # Verificar calidad
        calidad = verificar_calidad(df)

        df_calidad = pd.DataFrame(calidad).T
        df_calidad[['Nulos','Outliers','Ok']] = df_calidad[['Nulos','Outliers','Ok']].astype('int')
        print(df_calidad)
        
        bar_calidad(calidad,archivo,DIRECTORIO_IMAGES)

        box_plot_calidad(df,archivo,DIRECTORIO_IMAGES)
        
        del df
        del df_calidad

        print(100*'-')
        print()
        

if __name__ == "__main__":
    main()
