
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

from datos import df_precios, df_ce, parametros_stsc
from multiprocessing import cpu_count
import multiprocessing as mp
import funciones as fn
import pickle
import time
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    print('                                                            ')
    print(' -- ---------------- ------------------- ---------------- --')
    print(' -- ---------------- Inicio de ejecucion ---------------- --')
    print(' -- ---------------- ------------------- ---------------- --')

    # contabilizar el tiempo completo con todas las combinaciones
    e_i7 = time.time()

    for ciclo in range(0, len(parametros_stsc['data_series'])):
        if ciclo < 10:
            str_ciclo = '0' + str(ciclo)
        else:
            str_ciclo = str(ciclo)

        print('                                                            ')
        print(' ***********************************************************')
        print(' ************************ CICLO: ' + str_ciclo + ' ************************')
        print(' ***********************************************************')

        # -- --------------------------------------------------------------- FUNCTION : 1 -- #
        # -- Calcular escenarios para indicadores
        s_f1 = time.time()
        df_ce = fn.f_escenario(p0_datos=df_ce)
        e_f1 = time.time()
        time_f1 = round(e_f1 - s_f1, 4)
        print('f_escenario se tardo: ' + str(time_f1))

        # -- --------------------------------------------------------------- FUNCTION : 2 -- #
        # -- Calcular las metricas para reacciones del precio
        s_f2 = time.time()
        df_ce = fn.f_metricas(param_ce=df_ce, param_ph=df_precios,
                              param_window=parametros_stsc['data_window'][ciclo])
        e_f2 = time.time()
        time_f2 = round(e_f2 - s_f2, 4)
        print('f_metricas se tardo: ' + str(time_f2))

        # -- -------------------------------------------------- Data exploratory analysis -- #

        # -- Statistics of scenario ocurrence

        # -- Scenario statistics visualizations

        # -- Boxplot for each indicator_scenario metrics values, for all the 4 metrics

        # -- --------------------------------------------------------------- FUNCTION : 3 -- #
        # -- Tabla de ocurrencias de escenario para cada indicador
        s_f3 = time.time()
        df_ind_1 = fn.f_tabla_ind(param_ce=df_ce)
        e_f3 = time.time()
        time_f3 = round(e_f3 - s_f3, 2)
        print('f_tabla_ind se tardo: ' + str(time_f3))

        # -- --------------------------------------------------------------- FUNCTION : 4 -- #
        # -- Seleccionar indicadores y escenarios con observaciones suficientes
        s_f4 = time.time()
        df_ind_2 = fn.f_seleccion_ind(param_ce=df_ind_1, param_c1=24, param_c2=12)
        e_f4 = time.time()
        time_f4 = round(e_f4 - s_f4, 2)
        print('f_seleccion_ind se tardo: ' + str(time_f4))

        # -- --------------------------------------------------------------- FUNCTION : 5 -- #
        # -- Construir tabla de anova para seleccionar escenarios candidatos
        s_f5 = time.time()
        df_ind_3 = fn.f_anova(param_data1=df_ind_2, param_data2=df_ce)
        e_f5 = time.time()
        time_f5 = round(e_f5 - s_f5, 2)
        print('f_anova se tardo: ' + str(time_f3))

        # -- --------------------------------------------------------------- FUNCTION : 6 -- #
        # -- Busqueda hacia adelante de patrones en serie de tiempo

        e_i6 = time.time()

        print('                                                            ')
        print(' ***********************************************************')
        print(' ***************** PARALELIZACION DE STSC ******************')
        print(' ***********************************************************')

        pool = mp.Pool(cpu_count())
        stsc = {'ciclo_' +
                ciclo: pool.starmap(fn.f_ts_clustering,
                                    [(df_precios, indexador_data, df_ind_3, df_ce,
                                      parametros_stsc['data_series'][ciclo],
                                      parametros_stsc['data_window'][ciclo],
                                      parametros_stsc['mass_cores'][ciclo],
                                      parametros_stsc['mass_batch'][ciclo],
                                      parametros_stsc['mass_matches'][ciclo])
                                     for indexador_data in range(0, len(df_ind_3))])}

        pool.close()

        # crear nombre de archivo
        archivo = str(parametros_stsc['data_series'][ciclo]) + '_' + \
                  str(parametros_stsc['data_window'][ciclo]) + '_' + \
                  str(parametros_stsc['mass_cores'][ciclo]) + '_' + \
                  str(parametros_stsc['mass_batch'][ciclo]) + '_' + \
                  str(parametros_stsc['mass_matches'][ciclo])

        # Guardar resultados de la combinacion iterada
        with open(archivo, 'wb') as file:
            pickle.dump(stsc, file)

        e_f6 = time.time()
        time_f6 = round(e_f6 - e_i6, 2)
        print('f_ts_clustering paralelizado se tardo: ' + str(time_f6))

    e_f7 = time.time()

    print('                                                            ')
    print(' -- ---------------- ------------------- ---------------- --')
    print(' -- ---------------- Fin de la ejecucion ---------------- --')
    print(' -- ---------------- ------------------- ---------------- --')

    time_f7 = round(e_f7 - e_i7, 2)
    print('ciclo de ' + str(len(parametros_stsc['data_series'])) +
          ' iteraciones se tardo: ' + str(time_f7))
    print(' -- Finalizado sin errores de ejecucion -- ')

# -- Prueba para re-abrir archivo pickle
# with open('mid_oc_10_1_1000_10', 'rb') as file:
#     results_dictionary = pickle.load(file)
#     print(results_dictionary)
