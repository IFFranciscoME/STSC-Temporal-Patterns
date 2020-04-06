
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: poster.py - generacion de datos de salida para uso en poster                 -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vs
import entradas as en


# grafica 1 : series de tiempo para busqueda de patrones
pattern = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
pattern = pattern['df_serie_p']['close']
query = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
query = query['df_serie_q']['close']
theme = en.tema_base
dims = en.dimensiones_base

grafica_1 = vs.g_lineas(param_query=query, param_pattern=pattern,
                        param_theme=theme, param_dims=dims)

# grafica 2 : serie origin vs patron encontrado

# grafica 3 : ocurrencia de indicador_esc por tipo de patron

# tabla 1 : Ocurrencia de patrones por indicador_escenario
dc_tablas = fn.f_tablas_ocur(param_carpeta='datos/results_files_r3')
