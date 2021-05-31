
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Subsequential Time Series Clustering: Evidence of Temporal Patterns in UsdMxn Exchange Rate         -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Description: Code repositories (Python, R and LaTeX for research poster                             -- #
# -- Script: poster.py : python script with functions to produce results and write files for poster      -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- Repository: https://github.com/IFFranciscoME/STSC-Temporal-Patterns                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import functions as fn
import visualizations as vs
import execution as ex

from data import df_ce
from execution import ind_tip

# resultados para tomar ejemplo para las graficas
results = fn.f_leer_resultados(param_carpeta='datos/results_files_r3/',
                               param_archivo='mid_oc_30_1_3000_20')

# tema de colores a utilizar
theme = ex.tema_base
# dimensiones a utilizar
dims = ex.dimensiones_base

# -------------------------------------------------------------------- datos para ejemplo -- #
results_ocur = list(results['ciclo_4'][89]['datos'].keys())
# serie patron arbitraria encontrada para graficar = 6
pattern = results['ciclo_4'][89]['datos'][results_ocur[3]]['df_serie_p']
# serie query arbitraria encontrada para graficar = 7
query = results['ciclo_4'][89]['datos'][results_ocur[7]]['df_serie_q']

# -- -------------------------------------------------------------------------- Grafica 1 -- #
# -- velas con ohlc y series de busqueda de patrones

# series patron y query para graficar
pattern_g2 = pattern.reset_index(inplace=False, drop=True)

# generacion de grafica 1
grafica_1 = vs.g_velas_reac(param_timestamp=pattern_g2['timestamp'],
                            param_ohlc=pattern_g2,
                            param_serie1=pattern_g2['mid_oc'],
                            param_serie2=pattern_g2['mid_hl'],
                            param_theme=theme, param_dims=dims)

# mostrar grafica 1
grafica_1.show()

# -- -------------------------------------------------------------------------- Grafica 2 -- #
# -- Series original vs patron encontrado

# series patron y query para graficar
pattern_g2 = pattern['mid_oc']
query_g2 = query['mid_oc']

# generar grafica 2
grafica_2 = vs.g_lineas(param_query=query_g2, param_pattern=pattern_g2,
                        param_theme=theme, param_dims=dims)

# mostrar grafica 2
grafica_2.show()

# -- ---------------------------------------------------------------------------- Tabla 1 -- #
# -- tabla con informacion general de todos los indicadores

tabla_1 = fn.ce_tabla_general(param_ce=df_ce, param_tip=ind_tip)
tabla_1.to_csv(r'poster/tablas/t_tabla_1.csv')

# -- ---------------------------------------------------------------------------- Tabla 2 -- #
# -- Ocurrencia de patrones por indicador_escenario

tabla_2 = fn.f_tablas_ocur(param_carpeta='datos/results_files_r3')
tabla_2 = tabla_2['df_mid_hl_30_1_3000_20']
tabla_2.to_csv(r'poster/tablas/t_tabla_2.csv')

# -- ---------------------------------------------------------------------------- Tabla 3 -- #
# -- para grafica tipo aluvial
tabla_3 = fn.f_tabla_aluvial(param_tabla_1=tabla_1, param_tabla_2=tabla_2)
tabla_3.to_csv(r'poster/tablas/t_tabla_3.csv')

# -- -------------------------------------------------------------------------- Grafica 3 -- #
# -- Ocurrencia de indicador_esc por tipo de patron

grafica_3 = vs.g_aluvial_cat(param_data=tabla_3, param_theme=theme, param_dims=dims)

# mostrar grafica 3
grafica_3.show()

# -- ---------------------------------------------------------------------------- Tabla 4 -- #
# -- Tablas auxiliares generales

tabla_4 = fn.f_tabla_general(param_tabla_1=tabla_1)
tabla_4.to_csv(r'poster/tablas/t_tabla_4.csv')

# -- ------------------------------------------------------- Escribir archivo JSON para R -- #
# -- Escribir un archivo tipo JSON serializando los datos

# resultados para tomar ejemplo para las graficas
# res_pickle = fn.f_leer_resultados(param_carpeta='datos/results_files_r3/',
#                                   param_archivo='mid_oc_30_1_3000_20')

# funcion que serializa y escribe JSON
# fn.f_serial_result(param_objeto=res_pickle,
#                    param_nombre='poster/datos/mid_oc_30_1_3000_20.json')
