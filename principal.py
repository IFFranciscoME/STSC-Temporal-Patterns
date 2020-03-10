
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# Importar Precios historicos M1 del 2019
from datos import df_usdmxn, df_ce
import funciones as fn
import time

# -- -------------------------------------------------------------------- Data generation -- #

s_f1 = time.time()
# Calcular escenarios para indicadores
df_ce = fn.f_escenario(p0_datos=df_ce)
e_f1 = time.time()

time_f1 = round(e_f1 - s_f1, 4)
print('f1 se tardo: ' + str(time_f1))

# -- ------------------------------------------------------ Indicator-Scenario Selection -- #

# -- ----------------------------------------------------------------------- FUNCTION : 2 -- #
# -- Calcular las metricas para reacciones del precio
# -- para medir el cambio en la varianza
s_f2 = time.time()
df_ce = fn.f_metricas(param_ce=df_ce, param_ph=df_usdmxn)
e_f2 = time.time()

time_f2 = round(e_f2 - s_f2, 4)
print('f2 se tardo: ' + str(time_f2))

# -- ---------------------------------------------------------- Data exploratory analysis -- #

# -- Statistics of scenario ocurrence

# -- Scenario statistics visualizations

# -- Boxplot for each indicator_scenario metrics values, for all the 4 metrics

# -- ----------------------------------------------------------------------- FUNCTION : 3 -- #
# -- Tabla de ocurrencias de escenario para cada indicador
s_f3 = time.time()
df_indes = fn.f_tabla_ind(param_ce=df_ce)
e_f3 = time.time()

time_f3 = round(e_f3 - s_f3, 2)
print('f3 se tardo: ' + str(time_f3))

# -- ----------------------------------------------------------------------- FUNCTION : 4 -- #
# -- Seleccionar indicadores y escenarios para pruebas ANOVA
s_f4 = time.time()

# indicadores con mas de 40 observaciones.
indes_out_1 = df_indes[df_indes['T'] < 40].index
df_indes.drop(indes_out_1, inplace=True)
df_indes.reset_index(inplace=True, drop=True)

# escenarios de cada indicador con mas de 12 observaciones
indes_out_2 = df_indes[(df_indes['A'] < 12) & (df_indes['B'] < 12) &
                       (df_indes['C'] < 12) & (df_indes['D'] < 12)].index
df_indes.drop(indes_out_2, inplace=True)
df_indes.reset_index(inplace=True, drop=True)

e_f4 = time.time()

time_f4 = round(e_f4 - s_f4, 2)
print('f4 se tardo: ' + str(time_f4))

# -- ----------------------------------------------------------------------- FUNCTION : 5 -- #
# tabla de anova
s_f5 = time.time()
df_anova = fn.f_anova(param_data1=df_indes, param_data2=df_ce)

e_f5 = time.time()

time_f5 = round(e_f5 - s_f5, 2)
print('f5 se tardo: ' + str(time_f3))
