
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

from datos import df_usdmxn, df_ce
from datetime import timedelta
import funciones as fn
import time
import numpy as np
import mass_ts as mass

# -- ----------------------------------------------------------------------- FUNCTION : 1 -- #
# -- Calcular escenarios para indicadores
s_f1 = time.time()
df_ce = fn.f_escenario(p0_datos=df_ce)
e_f1 = time.time()
time_f1 = round(e_f1 - s_f1, 4)
print('f_escenario se tardo: ' + str(time_f1))

# -- ----------------------------------------------------------------------- FUNCTION : 2 -- #
# -- Calcular las metricas para reacciones del precio
s_f2 = time.time()
df_ce = fn.f_metricas(param_ce=df_ce, param_ph=df_usdmxn)
e_f2 = time.time()
time_f2 = round(e_f2 - s_f2, 4)
print('f_metricas se tardo: ' + str(time_f2))

# -- ---------------------------------------------------------- Data exploratory analysis -- #

# -- Statistics of scenario ocurrence

# -- Scenario statistics visualizations

# -- Boxplot for each indicator_scenario metrics values, for all the 4 metrics

# -- ----------------------------------------------------------------------- FUNCTION : 3 -- #
# -- Tabla de ocurrencias de escenario para cada indicador
s_f3 = time.time()
df_ind_1 = fn.f_tabla_ind(param_ce=df_ce)
e_f3 = time.time()
time_f3 = round(e_f3 - s_f3, 2)
print('f_tabla_ind se tardo: ' + str(time_f3))

# -- ----------------------------------------------------------------------- FUNCTION : 4 -- #
# -- Seleccionar indicadores y escenarios con observaciones suficientes
s_f4 = time.time()
df_ind_2 = fn.f_seleccion_ind(param_ce=df_ind_1, param_c1=60, param_c2=25)
e_f4 = time.time()
time_f4 = round(e_f4 - s_f4, 2)
print('f_seleccion_ind se tardo: ' + str(time_f4))

# -- ----------------------------------------------------------------------- FUNCTION : 5 -- #
# -- Construir tabla de anova para seleccionar escenarios candidatos
s_f5 = time.time()
df_ind_3 = fn.f_anova(param_data1=df_ind_2, param_data2=df_ce)
e_f5 = time.time()
time_f5 = round(e_f5 - s_f5, 2)
print('f_anova se tardo: ' + str(time_f3))

# -- ----------------------------------------------------------------------- FUNCTION : 6 -- #
# -- Busqueda hacia adelante de patrones

# Para cada indicador, para cada escenario, empezar desde la 1era ocurrencia y buscar
# hacia adelante:
# -- En los mismos indicadores y mismos escenarios
# -- En los mismos indicadores en diferentes escenarios
# -- En otros indicadores
# -- En todas las demas ventanas de precios


def f_busqueda_adelante(param_row, param_ca_data, param_ce_data, param_p_ventana, param_cores):
    """
    Parameters
    ----------
    param_row :
    param_ce_data :
    param_ca_data :
    param_p_ventana :
    param_cores :

    Returns
    -------
    df_tabla_busqueda

    Debugging
    ---------
    param_row = 0 # renglon de iteracion de candidatos
    param_ca_data = df_ind_3 # dataframe con candidatos a iterar
    param_ce_data = df_ce # dataframe con calendario completo
    param_p_ventana = 30 # tamano de ventana para buscar serie de tiempo
    param_cores = 4 # nucleos con los cuales utilizar algoritmo

    """
    # almacenar resultados
    resultado = list()

    # renglon con informacion de evento disparador candidato
    candidate_data = param_ca_data.iloc[param_row, :]
    print('Ind disparador: ' + str(candidate_data['name']) + ' - ' + candidate_data['esc'])

    # datos completos de todas las ocurrencias del evento disparador candidato
    df_ancla = param_ce_data[(param_ce_data['esc'] == candidate_data['esc']) &
                             (param_ce_data['name'] == candidate_data['name'])]

    # todos los timestamps del calendario economico completo
    ts_serie_ce = list(param_ce_data['timestamp'])

    # -- ------------------------------------------------------ OCURRENCIA POR OCURRENCIA -- #
    for ancla in range(0, len(df_ancla['timestamp'])-1):
        print(ancla)
        # datos de ancla para buscar hacia el futuro
        ancla_ocurr = df_ancla.iloc[ancla, ]
        print('ind: ' + ancla_ocurr['name'] + ' ' + str(ancla_ocurr['timestamp']))
        # fecha de ancla
        fecha_ini = ancla_ocurr['timestamp']
        # se toma el timestamp de precios igual a timestamp del primer escenario del indicador
        ind_ini = df_usdmxn[df_usdmxn['timestamp'] == fecha_ini].index
        # fecha final es la fecha inicial mas un tamaño de ventana arbitrario
        ind_fin = ind_ini + param_p_ventana
        # se construye la serie query
        serie_q = df_usdmxn.iloc[ind_ini[0]:ind_fin[0], :]
        # se toma el close
        serie_q = np.array(serie_q['close'])
        # se construye la serie completa para busqueda (un array de numpy de 1 dimension)
        serie = np.array(df_usdmxn.loc[ind_fin[0]:, 'close'])

        print('serie BIEN')

        # tamaño de ventana para iterar la busqueda = tamaño de query
        batch = param_p_ventana * 10
        # la cantidad de casos que regresa como "mas parecidos"
        matches = 10
        # correr algoritmo y regresar los indices de coincidencias y las distancias
        mass_indices, mass_dists = mass.mass2_batch(ts=serie, query=serie_q,
                                                    batch_size=batch,
                                                    top_matches=matches,
                                                    n_jobs=param_cores)

        # Indice de referencia de n-esima serie similar encontrada
        for indice in mass_indices:
            # DataFrame de n-esima serie patron similar encontrada
            df_serie_p = df_usdmxn[indice:indice + param_p_ventana]
            print('Verificando patron con f_ini: ' +
                  str(list(df_serie_p['timestamp'])[0]) + ' f_fin: ' +
                  str(list(df_serie_p['timestamp'])[-1]))

            # Extraer solo los timestamp de la serie patron para busqueda.
            ts_serie_p = list(df_serie_p['timestamp'])

            # Busqueda si el timestamp inicial de cada uno de los patrones
            # encontrados es igual a alguna fecha de comunicacion de toda
            # la lista de indicadores que se tiene

            if ts_serie_p[0] in ts_serie_ce:
                # print(param_ce_data.loc[np.where(ts_serie_ce == ts_serie_p[0])[0], 'name'])
                print('Coincidencia encontrada')
                resultado.append(param_ce_data.loc[np.where(ts_serie_ce == ts_serie_p[0])[0],
                                                   'name'])

                # Tipo1 = Mismo Indicador + Mismo Escenario que la ancla

                # Tipo2 = Mismo Indicador + Cualquier Escenario

                # Tipo3 = Otro Indicador en la lista
            else:
                print('No coincide con comunicado de indicadores')

                # Tipo0 = Cualquier otro punto en el tiempo fuera
                # de ocurrencia de indicadores

    return resultado


stsc = f_busqueda_adelante(param_row=0, param_ca_data=df_ind_3, param_ce_data=df_ce,
                           param_p_ventana=30, param_cores=4)
