
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: poster.py - generacion de datos de salida para uso en poster                 -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vs
import entradas as en

# -- -------------------------------------------------------------------------- Grafica 1 -- #
# -- velas con ohlc y series de busqueda de patrones

# -- -------------------------------------------------------------------------- Grafica 2 -- #
# -- Series original vs patron encontrado

results = fn.f_leer_resultados(param_carpeta='datos/results_files_r3/',
                               param_archivo='mid_oc_30_1_3000_20')

# serie patron arbitraria encontrada para graficar = 7
results_ocur = list(results['ciclo_4'][89]['datos'].keys())
pattern = results['ciclo_4'][89]['datos'][results_ocur[7]]['df_serie_p']['mid_oc']

# serie query arbitraria encontrada para graficar = 7
query = results['ciclo_4'][89]['datos'][results_ocur[7]]['df_serie_q']['mid_oc']

# tema de colores a utilizar
theme = en.tema_base

# dimensiones a utilizar
dims = en.dimensiones_base

# generar grafica
grafica_1 = vs.g_lineas(param_query=query, param_pattern=pattern,
                        param_theme=theme, param_dims=dims)
grafica_1.show()

# -- -------------------------------------------------------------------------- Grafica 3 -- #
# -- Ocurrencia de indicador_esc por tipo de patron

# -- -------------------------------------------------------------------------- Tabla 1 -- #
# -- Ocurrencia de patrones por indicador_escenario

dc_tablas = fn.f_tablas_ocur(param_carpeta='datos/results_files_r3')
