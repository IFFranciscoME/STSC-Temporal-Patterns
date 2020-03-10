
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: datos.py - descarga de los datos necesarios para el proyecto                 -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import funciones as fn

from os import listdir, path
from os.path import isfile, join

# dividir en 11 partes
all_years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

# -------------------------------------------------------- GUARDAR SOLO LOS SELECCIONADOS -- #
years = all_years[0:4]
archivo = 'USD_MXN_M1'

# -- -------------------------------------------------------- Descarga de precios masivos -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Solo correr 1 vez para la descarga masiva de precios
#
# # token de OANDA https://www.oanda.com/demo-account/tpa/personal_token
# oa_ak = '8' + 'b50d0cc9f97037e5b6e7b28de8be537-bccc5ff454afcd2ace0f774a57534ca' + 'd'
# oa_in = "USD_MXN"  # Instrumento
# oa_gn = "M1"       # Granularidad de velas (M1: Minuto, M5: 5 Minutos, M15: 15 Minutos)
# fini = pd.to_datetime("2010-01-01 00:00:00").tz_localize('GMT')  # Fecha inicial
# ffin = pd.to_datetime("2020-01-03 00:00:00").tz_localize('GMT')  # Fecha final
#
# # -- solicitar 1 vez la descarga de precios masivos
# df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn, p3_inst=oa_in,
#                              p4_oatk=oa_ak, p5_ginc=4910)
# # formato a columnas
# columns = list(df_pe.columns)
# columns = [i.lower() for i in columns]
# df_pe.rename(columns=dict(zip(df_pe.columns[0:], columns)), inplace=True)
#
# # escribir cada parte en un archivo para que sea menos pesado cada uno y subir todos a github
# for a in years:
#     lista = [df_pe.loc[i, 'timestamp'].year == a for i in range(0, len(df_pe['timestamp']))]
#     df_escribir = df_pe.iloc[lista, :]
#     nombre_a = archivo + '_' + str(a)
#     df_escribir.to_csv(r'datos/price_files/' + nombre_a + '.csv', index=False)

# -- ---------------------------------------------------------- Lectura masiva de precios -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- leer y concatenar todos los archivos en un DataFrame

archivos = list()
# ciclo para leer los archivos
for a in years:
    nombre_a = 'datos/price_files/' + archivo + '_' + str(a) + '.csv'
    # print(nombre_a)
    archivos.append(pd.read_csv(nombre_a))

# concatenar todos los archivos
df_usdmxn = pd.concat(archivos, sort=False)

# modificar el tipo de dato para la columna timestamp
df_usdmxn['timestamp'] = pd.to_datetime(list(df_usdmxn['timestamp']))
df_usdmxn.reset_index(inplace=True, drop=True)

# -- ------------------------------------------ Lectura masiva de archivos de indicadores -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Solo correr 1 vez para la lectura masiva de archivos con indicadores

# # lista de todos los archivos dentro del directorio files
# abspath = path.abspath('datos/econ_files')
# files = [f for f in listdir(abspath) if isfile(join(abspath, f))]
#
# # Lista con paises
# economias = ['Mexico' if files[i].find('Mexico') != -1 else 'United States'
#              for i in range(0, len(files))]
#
# # Lista con nombres
# indicadores = [files[i][0:files[i].find(' - ')] for i in range(0, len(files))]
#
# # DataFrame de control general
# df_ce_g = pd.DataFrame({'ind': indicadores, 'econ': economias})
#
# # DataFrame con historicos
# df_ce = fn.f_unir_ind(param_dir=path.abspath('datos/econ_files/'))
#
# # Escribir archivo
# df_ce.to_csv(r'datos/econ_files/' + 'ECON_USD_MXN' + '.csv', index=False)

# -- ------------------------------------------------------- Lectura de archivo unificado -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- leer un csv en y guardar en un DataFrame

df_ce = pd.read_csv('datos/econ_files/' + 'ECON_USD_MXN' + '.csv')

lista = list()
# Convertir a tipo datetime
df_ce['timestamp'] = pd.to_datetime(df_ce['timestamp'])
# Crear columna
df_ce['year'] = [df_ce['timestamp'][i].year for i in range(0, len(df_ce['timestamp']))]
# Seleccionar los deseados
df_ce = df_ce.loc[df_ce['year'].isin(years)]
# Resetear el index
df_ce.reset_index(inplace=True, drop=True)
