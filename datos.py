
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

oa_ak = '8b50d0cc9f97037e5b6e7b28de8be537-bccc5ff454afcd2ace0f774a57534cad'  # token de OANDA
oa_in = "EUR_USD"  # Instrumento
oa_gn = "M1"       # Granularidad de velas (M1: Minuto, M5: 5 Minutos, M15: 15 Minutos)
fini = pd.to_datetime("2019-01-01 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-31 00:00:00").tz_localize('GMT')  # Fecha final

df_pe_19 = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn, p3_inst=oa_in,
                                p4_oatk=oa_ak, p5_ginc=4900)

# -- ----------------------------------------- Descarga de indicadores economicos masivos -- #

# lista de todos los archivos dentro del directorio files
abspath = path.abspath('datos/files')
files = [f for f in listdir(abspath) if isfile(join(abspath, f))]

# Lista con paises
economias = ['Mexico' if files[i].find('Mexico') != -1 else 'United States'
             for i in range(0, len(files))]

# Lista con nombres
indicadores = [files[i][0:files[i].find(' - ')] for i in range(0, len(files))]

# DataFrame de control general
df_ce_g = pd.DataFrame({'ind': indicadores, 'econ': economias})

# -- Generar criterio de eleccion de indicadores
# base cuantitativa
# con informacion completa
# a la misma hora y el mismo dia, que haya sucedido solo 1 indicador

