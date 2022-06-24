import pandas as pd
import os
from auxiliares_batch import crear_dataframe, verificar_calidad, coordenadas_localidad, localidad_mas_cercana
import json

# Constantes
archivo= 'Clientes_cliente2020.csv'
DIRECTORIO_OUTPUT = 'Output'

# NORMALIZACION

df = crear_dataframe(archivo)

calidad = verificar_calidad(df)
df_calidad = pd.DataFrame(calidad).T
df_calidad[['Nulos','Outliers','Ok']] = df_calidad[['Nulos','Outliers','Ok']].astype('int')

print()
print('Reporte de calidad:')
print(100*'-')
print(df_calidad)
print()


print('ACCION: Dropear columnas que no aportan información')
print()

columnas_dropear = ['Provincia','col10']

print(f'Columnas a dropear: {columnas_dropear}')
print()

df = df.drop(columns = columnas_dropear)

print('ACCION: Corregir coordenadas')
print()

mask = ((df.X+35)**2 < 10**2) & ((df.Y+58)**2 < 10**2)

print(f'1) Latitud y longitud invertidas: {df[mask].shape[0]} registro(s)')

try:
    df.loc[mask,'X'], df.loc[mask,'Y'] = df[mask].Y, df[mask].X

    mask_corregidos = ((df.X+35)**2 < 10**2) & ((df.Y+58)**2 < 10**2)
    print(f'Latitud y longitud invertidas (después de procesar): {df[mask_corregidos].shape[0]} registro(s)')

except:
    print('ERROR: no se invirtieron coordenadas')

print()
print('2) Problemas de signos')

try:
    mask_2_x = (df.X > 0)
    a_corregir = df[mask_2_x].shape[0]
    print(f'Registros con longitudes positivas: {a_corregir}')
    df.loc[mask_2_x,'X'] = df.X*(-1)
    mask_2_x = (df.X > 0)
    print(f'Corregidos: {a_corregir - df[mask_2_x].shape[0]} registros')
except:
    print('ERROR: no corregidos')

print()

try:
    mask_2_y = (df.Y > 0)
    a_corregir = df[mask_2_y].shape[0]
    print(f'Registros con longitudes positivas: {a_corregir}')
    df.loc[mask_2_y,'Y'] = df.Y*(-1)
    mask_2_y = (df.Y > 0)
    print(f'Corregidos: {a_corregir - df[mask_2_y].shape[0]} registros')
except:
    print('ERROR: no corregidos')

print()

print('ACCION: Corregir valores faltantes de localidad a través de coordenadas')

# Buscar localidad
local_null_mask = ((df.Localidad.isnull()) & ((df.X.notnull()) | (df.Y.notnull())))

try:
    a_corregir = df[local_null_mask].shape[0]
    print(f'Registros con Localidad nula: {a_corregir} registro(s)')
    
    df.loc[local_null_mask,'Localidad'] = df.apply(lambda x: localidad_mas_cercana(df.X, df.Y), axis = 1)
    
    local_null_mask = ((df.Localidad.isnull()) & ((df.X.notnull()) | (df.Y.notnull())))
    
    print(f'Corregidos: {a_corregir-df[local_null_mask].shape[0]} registro(s)')

except:
    print('ERROR: no corregidos')


print('ACCION: Corregir valores faltantes de coordenadas a través de localidad (Algoritmo de Levenshtein)')
print()

mask = mask = (df.X.isna()) | (df.Y.isna())
a_corregir = df[mask].shape[0]
print(f'Registros con Localidad nula: {a_corregir} registro(s)')

localidades_buscadas = df.loc[mask,['Localidad','X','Y']].to_dict()

for index in localidades_buscadas['Localidad'].keys():
    (localidades_buscadas['X'][index],localidades_buscadas['Y'][index])  = coordenadas_localidad(localidades_buscadas['Localidad'][index])

df_coordenadas_corregidas = pd.DataFrame(localidades_buscadas)

df.loc[mask,['X','Y']] = df_coordenadas_corregidas[['X','Y']]

print(f'Registros corregidos: {a_corregir - df[(df.X.isna()) | (df.Y.isna())].shape[0]} registro(s)')

calidad = verificar_calidad(df)
df_calidad = pd.DataFrame(calidad).T
df_calidad[['Nulos','Outliers','Ok']] = df_calidad[['Nulos','Outliers','Ok']].astype('int')

print()
print('Reporte de calidad:')
print(100*'-')
print(df_calidad)
print()

print('ACCION: Exportar todos los csv')

try:
    df[df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Cliente_nulos.csv',index=False,mode='a')
    df[~df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Cliente_Dic2020_nulos.csv',index=False)
    print(f'REGISTROS NULOS: Archivo exportado: ./{DIRECTORIO_OUTPUT}/Cliente_nulos.csv')
except:
    print('ERROR: archivo no exportado.')
  

try:
    df[~df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Cliente_ok.csv',index=False, mode='a')
    df[~df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Cliente_Dic2020_ok.csv',index=False)
    print(f'REGISTROS CORRECTOS: Archivo exportado: ./{DIRECTORIO_OUTPUT}/Cliente_ok.csv')
except:
    print('ERROR: archivo no exportado.')


print()