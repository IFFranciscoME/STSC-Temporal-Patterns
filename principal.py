
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

from datos import df_usdmxn, df_ce
import funciones as fn
import time

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

criterios = ['ind_sel+esc', 'ind_sel', 'ind', 'all']
procesos = len(df_ind_3.iloc[:, 1])


def f_busqueda_adelante(param_row, param_ca_data=df_ind_3,
                        param_ce_data=df_ce, param_crit=None):
    """
    Parameters
    ----------
    param_row :
    param_ce_data
    param_ca_data :
    param_crit :

    Returns
    -------

    Debugging
    ---------
    param_row = 0
    param_ca_data = df_anova
    param_ce_data = df_ce
    param_crit = criterios

    """

    if param_crit is None:
        param_crit = criterios

    # renglon con informacion de escenario candidato
    candidate_data = param_ca_data.iloc[param_row, :]
    # primera ocurrencia de escenario candidato
    param_ce_data[(param_ce_data['escenario'] == candidate_data['esc']) &
                  (param_ce_data['name'] == candidate_data['ind'])]

    # localizar punto inicial
    historical_data = param_ce_data[param_ce_data['name'] == candidate_data['ind']]

    if param_crit == 'ind_sel+esc':
        print(1)

    elif param_crit == 'ind_sel':
        print(1)

    elif param_crit == 'ind':
        print(1)

    elif param_crit == 'all':
        print(1)

    return 1
