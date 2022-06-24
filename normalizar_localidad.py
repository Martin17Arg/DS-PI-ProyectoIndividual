import pandas as pd
import os
from auxiliares_batch import crear_dataframe, verificar_calidad
import json

# Constantes
archivo= 'Localidades.csv'
DIRECTORIO_OUTPUT = 'Output'
ARCHIVO_PROVINCIA = 'Provincia.csv'
ARCHIVO_LOCALIDADES = 'Localidad.csv'

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

columnas_dropear = ['departamento_id','departamento_nombre','municipio_id','municipio_nombre','categoria','fuente','localidad_censal_nombre','localidad_censal_id']

print(f'Columnas a dropear: {columnas_dropear}')
print()

df = df.drop(columns = columnas_dropear)

print('ACCION: Ordenar columnas')
print()

columnas_ordenadas = ['id','nombre','provincia_id','provincia_nombre','centroide_lat','centroide_lon']
df = df[columnas_ordenadas]

print(f'Orden de columnas: {columnas_ordenadas}')
print()

print('ACCION: Crear otro dataframe con tabla de provincias')
print()

provincias = df[['provincia_id','provincia_nombre']].drop_duplicates()

print('ACCION: Exportar csv de provincias')

try:
    provincias.to_csv(f'./{DIRECTORIO_OUTPUT}/{ARCHIVO_PROVINCIA}',index=False)
    print(F'Archivo exportado: ./{DIRECTORIO_OUTPUT}/{ARCHIVO_PROVINCIA}')
except:
    print('ERROR: archivo no exportado.')

del provincias
print()

print('ACCION: Exportar csv de localidades')

localidades = df.drop(columns = ['provincia_nombre'])

try:
    localidades.to_csv(f'./{DIRECTORIO_OUTPUT}/{ARCHIVO_LOCALIDADES}',index=False)
    print(f'Archivo exportado: ./{DIRECTORIO_OUTPUT}/{ARCHIVO_LOCALIDADES}')
except:
    print('ERROR: archivo no exportado.')

del localidades
print()