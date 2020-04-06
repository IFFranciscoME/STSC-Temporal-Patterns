
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: poster.py - generacion de datos de salida para uso en poster                 -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vs
import entradas as en

from datos import df_ce
from entradas import ind_tip

# resultados para tomar ejemplo para las graficas
results = fn.f_leer_resultados(param_carpeta='datos/results_files_r3/',
                               param_archivo='mid_oc_30_1_3000_20')

# tema de colores a utilizar
theme = en.tema_base
# dimensiones a utilizar
dims = en.dimensiones_base
# datos en particulares escogidos para el ejemplo
results_ocur = list(results['ciclo_4'][89]['datos'].keys())
# serie patron arbitraria encontrada para graficar = 7
pattern = results['ciclo_4'][89]['datos'][results_ocur[7]]['df_serie_p']
# serie query arbitraria encontrada para graficar = 7
query = results['ciclo_4'][89]['datos'][results_ocur[7]]['df_serie_q']

# -- -------------------------------------------------------------------------- Grafica 1 -- #
# -- velas con ohlc y series de busqueda de patrones

# series patron y query para graficar
pattern_g2 = pattern.reset_index(inplace=False, drop=True)

# generacion de grafica 1
grafica_1 = vs.g_velas_reac(param_timestamp=pattern_g2['timestamp'], param_ohlc=pattern_g2,
                            param_serie1=pattern_g2['close'],
                            param_serie2=pattern_g2['mid_oc'],
                            param_serie3=pattern_g2['mid_hl'],
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

# -- -------------------------------------------------------------------------- Grafica 3 -- #
# -- Ocurrencia de indicador_esc por tipo de patron

# -- -------------------------------------------------------------------------- Tabla 1 -- #
# -- tabla con informacion general de todos los indicadores

tabla_1 = fn.ce_tabla_general(param_ce=df_ce, param_tip=ind_tip)

# -- -------------------------------------------------------------------------- Tabla 2 -- #
# -- Ocurrencia de patrones por indicador_escenario

tabla_2 = fn.f_tablas_ocur(param_carpeta='datos/results_files_r3')
