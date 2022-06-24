import pandas as pd
import os
from auxiliares_batch import crear_dataframe, verificar_calidad
import json

# Constantes
archivo= 'CanalDeVenta.xlsx'
DIRECTORIO_OUTPUT = 'Output'
#ARCHIVO_PROVINCIA = 'Provincia.csv'
ARCHIVO_CANALDEVENTA = 'CanalDeVenta.csv'

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

canaldeventa = df

try:
    canaldeventa.to_csv(f'./{DIRECTORIO_OUTPUT}/{ARCHIVO_CANALDEVENTA}',index=False)
    print(f'Archivo exportado: ./{DIRECTORIO_OUTPUT}/{ARCHIVO_CANALDEVENTA}')
except:
    print('ERROR: archivo no exportado.')

del canaldeventa
print()