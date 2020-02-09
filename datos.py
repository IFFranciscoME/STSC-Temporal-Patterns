
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: datos.py - descarga de los datos necesarios para el proyecto                 -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import funciones as fn

# -- -------------------------------------------------------- Descarga de precios masivos -- #

oa_ak = 'd74f029b2fa84337b1c5bc294a4cf0ad-cf53354027ca56ddf09c909a351d18ac'  # token de OANDA
oa_in = "EUR_USD"  # Instrumento
oa_gn = "M1"       # Granularidad de velas
fini = pd.to_datetime("2019-01-01 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-31 00:00:00").tz_localize('GMT')  # Fecha final

df_precios = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn, p3_inst=oa_in,
                                  p4_oatk=oa_ak, p5_ginc=4900)

# -- ----------------------------------------- Descarga de indicadores economicos masivos -- #
