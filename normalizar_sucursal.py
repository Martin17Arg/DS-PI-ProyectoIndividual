import pandas as pd
import os
from auxiliares_batch import crear_dataframe, verificar_calidad
import json

# Constantes
archivo= 'Sucursales.csv'
DIRECTORIO_OUTPUT = 'Output'
ARCHIVO_PROVEEDORES = 'Sucursal.csv'

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

columnas_dropear = ['Provincia']
df = df.drop(columns = columnas_dropear)

print(f'Columnas a dropear: {columnas_dropear}')
print()


print('ACCION: Exportar csv')

try:
    df[df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Sucursal_nulos.csv',index=False)
    print(f'REGISTROS NULOS: Archivo exportado: ./{DIRECTORIO_OUTPUT}/Sucursal_nulos.csv')
except:
    print('ERROR: archivo no exportado.')

try:
    df[~df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Sucursal_ok.csv',index=False)
    print(f'REGISTROS CORRECTOS: Archivo exportado: ./{DIRECTORIO_OUTPUT}/Sucursal_ok.csv')
except:
    print('ERROR: archivo no exportado.')

print()
