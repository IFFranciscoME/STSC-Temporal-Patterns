
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

from datos import df_precios, df_ce
import multiprocessing as mp
import funciones as fn
import pandas as pd
import time
import json
from multiprocessing import cpu_count

import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    print('Inicio de ejecucion')

    # -- ------------------------------------------------------------------- FUNCTION : 1 -- #
    # -- Calcular escenarios para indicadores
    s_f1 = time.time()
    df_ce = fn.f_escenario(p0_datos=df_ce)
    e_f1 = time.time()
    time_f1 = round(e_f1 - s_f1, 4)
    # print('f_escenario se tardo: ' + str(time_f1))

    # -- ------------------------------------------------------------------- FUNCTION : 2 -- #
    # -- Calcular las metricas para reacciones del precio
    s_f2 = time.time()
    df_ce = fn.f_metricas(param_ce=df_ce, param_ph=df_precios)
    e_f2 = time.time()
    time_f2 = round(e_f2 - s_f2, 4)
    # print('f_metricas se tardo: ' + str(time_f2))

    # -- ------------------------------------------------------ Data exploratory analysis -- #

    # -- Statistics of scenario ocurrence

    # -- Scenario statistics visualizations

    # -- Boxplot for each indicator_scenario metrics values, for all the 4 metrics

    # -- ------------------------------------------------------------------- FUNCTION : 3 -- #
    # -- Tabla de ocurrencias de escenario para cada indicador
    s_f3 = time.time()
    df_ind_1 = fn.f_tabla_ind(param_ce=df_ce)
    e_f3 = time.time()
    time_f3 = round(e_f3 - s_f3, 2)
    # print('f_tabla_ind se tardo: ' + str(time_f3))

    # -- ------------------------------------------------------------------- FUNCTION : 4 -- #
    # -- Seleccionar indicadores y escenarios con observaciones suficientes
    s_f4 = time.time()
    df_ind_2 = fn.f_seleccion_ind(param_ce=df_ind_1, param_c1=18, param_c2=10)
    e_f4 = time.time()
    time_f4 = round(e_f4 - s_f4, 2)
    # print('f_seleccion_ind se tardo: ' + str(time_f4))

    # -- ------------------------------------------------------------------- FUNCTION : 5 -- #
    # -- Construir tabla de anova para seleccionar escenarios candidatos
    s_f5 = time.time()
    df_ind_3 = fn.f_anova(param_data1=df_ind_2, param_data2=df_ce)
    e_f5 = time.time()
    time_f5 = round(e_f5 - s_f5, 2)
    # print('f_anova se tardo: ' + str(time_f3))

    # -- ------------------------------------------------------------------- FUNCTION : 6 -- #
    # -- Busqueda hacia adelante de patrones en serie de tiempo

    parametros_stsc = {'data_series': ['mid', 'mid', 'mid', 'close', 'close', 'close'],
                       'data_window': [10, 20, 10, 10, 10, 10],
                       'mass_cores': [1, 1, 1, 1, 1, 1],
                       'mass_batch': [1000, 2000, 1000, 1000, 1000, 1000],
                       'mass_matches': [20, 20, 20, 20, 20, 20]}

    # ciclo para buscar varias combinaciones de casos

    for ciclo in range(0, 2):

        s_f6_2 = time.time()
        pool = mp.Pool(cpu_count()-1)
        df_stsc_2 = pd.DataFrame([pool.apply(fn.f_ts_clustering,
                                             args=(df_precios, indexador_data, df_ind_3, df_ce,
                                                   parametros_stsc['data_series'][ciclo],
                                                   parametros_stsc['data_window'][ciclo],
                                                   parametros_stsc['mass_cores'][ciclo],
                                                   parametros_stsc['mass_batch'][ciclo],
                                                   parametros_stsc['mass_matches'][ciclo]))
                                  for indexador_data in range(0, len(df_ind_3))])

        pool.close()
        e_f6_2 = time.time()
        time_f6_2 = round(e_f6_2 - s_f6_2, 2)

        archivo = str(parametros_stsc['data_series'][ciclo]) + '_' + \
                  str(parametros_stsc['data_window'][ciclo]) + '_' + \
                  str(parametros_stsc['mass_cores'][ciclo]) + '_' + \
                  str(parametros_stsc['mass_batch'][ciclo]) + '_' + \
                  str(parametros_stsc['mass_matches'][ciclo])

        df_stsc_2.to_csv(r'datos/results_files/' + archivo + '.csv', index=False)

        print('fin')
