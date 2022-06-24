import pandas as pd
import os
from auxiliares_batch import crear_dataframe, verificar_calidad
import json

# Constantes
archivo= 'Venta_Dic2020.csv'
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

print('ACCION: Exportar csv')

try:
    df[df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Venta_nulos.csv',index=False,mode='a')
    print(f'REGISTROS NULOS: Archivo exportado: ./{DIRECTORIO_OUTPUT}/Venta_nulos.csv')
except:
    print('ERROR: archivo no exportado.')

try:
    df[~df.isna().any(axis=1)].to_csv(f'./{DIRECTORIO_OUTPUT}/Venta_ok.csv',index=False)
    print(f'REGISTROS CORRECTOS: Archivo exportado: ./{DIRECTORIO_OUTPUT}/Venta_ok.csv')
except:
    print('ERROR: archivo no exportado.')

print()
