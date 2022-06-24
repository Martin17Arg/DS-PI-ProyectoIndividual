def verificar_calidad(df):
    '''
    Devuelve un diccionario con calidad del dato en cada columna.
    '''
    calidad = dict()
    columnas = df.columns

    for col in columnas:

        calidad[col] = dict()
        
        # Nulos
        calidad[col]['Nulos'] = int(df[col].isna().sum())

        # Outliers
        if df[col].dtype == 'float64':
            
            lim_inf = df[col].mean() - 3*df[col].std()
            lim_sup = df[col].mean() + 3*df[col].std()
            
            # Mask
            outliers = (df[col] < lim_inf) | (df[col] > lim_sup)
            
            if len(outliers.unique()) == 2:
                calidad[col]['Outliers'] = int(outliers.value_counts()[True])
            else: 
                calidad[col]['Outliers'] = 0
                
        else:
            calidad[col]['Outliers'] = 0

        # Datos ok    
        calidad[col]['Ok'] = int(df[col].notnull().sum() - calidad[col]['Outliers'])
        
        # Porcentajes
        calidad[col]['Nulos_perc'] = calidad[col]['Nulos']/(calidad[col]['Nulos']+calidad[col]['Outliers']+calidad[col]['Ok'])
        calidad[col]['Outliers_perc'] = calidad[col]['Outliers']/(calidad[col]['Nulos']+calidad[col]['Outliers']+calidad[col]['Ok'])
        calidad[col]['Ok_perc'] = calidad[col]['Ok']/(calidad[col]['Nulos']+calidad[col]['Outliers']+calidad[col]['Ok'])
        
    return calidad  

def crear_dataframe(archivo):

    import pandas as pd
    import os
    import json
    
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

    DIRECTORIO = 'Input'
    upper_tablas = [x[:4].upper() for x in tablas] # Lista para matchear tablas y archivos

    # Cargar configuración para read_csv
    with open(f'./{DIRECTORIO}/config.json') as config_file: # Cargar configuraciones particulares para cada CSV
        config = json.load(config_file)

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

    return df

def localidad_mas_cercana(longitud,latitud):

    import pandas as pd

    localidad = pd.read_csv('./Output/Localidad.csv')
    
    localidad['Distancia_cuadratica'] = (localidad['centroide_lat']-latitud)**2+(localidad['centroide_lon']-longitud)**2

    localidad_mas_cercana = str(localidad.nombre[localidad['Distancia_cuadratica'].idxmin()])

    return localidad_mas_cercana


def coordenadas_localidad(localidad_buscada):

    import pandas as pd
    from Levenshtein import distance
    
    localidad = pd.read_csv('./Output/Localidad.csv', 
                    usecols = ['nombre','centroide_lat','centroide_lon'])
        
    localidad['Distancias'] = localidad['nombre'].apply(lambda x: distance(x,localidad_buscada))

    latitud = localidad['centroide_lat'].iloc[localidad['Distancias'].idxmin()]
    longitud = localidad['centroide_lon'].iloc[localidad['Distancias'].idxmin()]

    coordenadas = (longitud,latitud)
        
    return coordenadas

def bar_calidad(calidad,archivo,path):

    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    
    columnas = []
    nulos = []
    outliers = []

    for i in calidad.keys():
        columnas.append(i)
        nulos.append(calidad[i]['Nulos_perc']*100)
        outliers.append(calidad[i]['Outliers_perc']*100)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.barh(columnas, nulos)
    ax.barh(columnas, outliers)

    ax.legend(['Nulos','Outliers'],loc='lower right')
    ax.set_title(str(archivo))

    fig = ax.get_figure()
    fig.savefig(f'./{path}/bar-{str(archivo).split(".")[0]}.jpg',bbox_inches='tight',dpi=100)

def box_plot_calidad(df,archivo,path):

    import matplotlib.pyplot as plt

    for col in df.columns:
        if ((df[col].dtype == 'float64') | (df[col].dtype == 'int64')):
            fig,ax = plt.subplots(tight_layout=True, figsize = (8,3))
            plt.boxplot(df[col][df[col].notnull()],vert=False)
            ax.set_title(col)
            fig.savefig(f'./{path}/box-{str(archivo).split(".")[0]}-{col}.jpg')    