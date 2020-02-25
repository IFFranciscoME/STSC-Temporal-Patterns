
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

# -- -------------------------------------------------------- Descarga de precios masivos -- #
#
# oa_ak = '8b50d0cc9f97037e5b6e7b28de8be537-bccc5ff454afcd2ace0f774a57534cad'  # token de OANDA
# oa_in = "USD_MXN"  # Instrumento
# oa_gn = "M1"       # Granularidad de velas (M1: Minuto, M5: 5 Minutos, M15: 15 Minutos)
# fini = pd.to_datetime("2018-01-01 00:00:00").tz_localize('GMT')  # Fecha inicial
# ffin = pd.to_datetime("2020-01-03 23:59:00").tz_localize('GMT')  # Fecha final
#
# # -- solicitar 1 vez la descarga de precios masivos
# df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn, p3_inst=oa_in,
#                              p4_oatk=oa_ak, p5_ginc=4920)
#
# columns = list(df_pe.columns)
# columns = [i.lower() for i in columns]
# df_pe.rename(columns=dict(zip(df_pe.columns[0:], columns)), inplace=True)
# df_pe.to_csv(r"datos/price_files/USD_MXN_M1.csv", index=False)

df_usdmxn = pd.read_csv('datos/price_files/USD_MXN_M1.csv')
df_usdmxn['timestamp'] = pd.to_datetime(list(df_usdmxn['timestamp']))

# -- ----------------------------------------- Descarga de indicadores economicos masivos -- #

# lista de todos los archivos dentro del directorio files
abspath = path.abspath('datos/econ_files')
files = [f for f in listdir(abspath) if isfile(join(abspath, f))]

# Lista con paises
economias = ['Mexico' if files[i].find('Mexico') != -1 else 'United States'
             for i in range(0, len(files))]

# Lista con nombres
indicadores = [files[i][0:files[i].find(' - ')] for i in range(0, len(files))]

# DataFrame de control general
df_ce_g = pd.DataFrame({'ind': indicadores, 'econ': economias})

# DataFrame con historicos
df_ce_h = fn.f_unir_ind(param_dir=path.abspath('datos/econ_files/'))

# para pruebas con 2019
df_ce = df_ce_h[list([(df_ce_h['timestamp'][i].year == 2018) |
                      (df_ce_h['timestamp'][i].year == 2019)
                      for i in range(0, len(df_ce_h['timestamp']))])]

# -- Generar criterio de eleccion de indicadores
# base cuantitativa
# con informacion completa
# a la misma hora y el mismo dia, que haya sucedido solo 1 indicador

