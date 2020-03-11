
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
df_ind_2 = fn.f_seleccion_ind(param_ce=df_ind_1, param_c1=60, param_c2=40)
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
# -- Busqueda hacia adelante de patrones en serie de tiempo
s_f6 = time.time()
stsc = [fn.f_ts_clustering(param_pe=df_usdmxn, param_row=s, param_ca_data=df_ind_3,
                           param_ce_data=df_ce, param_p_ventana=30, param_cores=4)
        for s in range(0, 1)]
e_f6 = time.time()
time_f6 = round(e_f6 - s_f6, 2)
print('f_ts_clustering se tardo: ' + str(time_f6))
