# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# Importar Precios historicos M1 del 2019
from datos import df_eurusd, df_ce_2019
import funciones as fn

# -- -------------------------------------------------------------------- Data generation -- #
# Importar Calendario Economico

# Calcular escenarios para indicadores
df_ce_h = fn.f_escenario(p0_datos=df_ce_2019)

# -- ---------------------------------------------------------- Data exploratory analysis -- #

# Statistics of scenario ocurrence

# Scenario statistics visualizations

# -- ------------------------------------------------------ Indicator-Scenario Selection -- #

# Calcular 4 metricas para reacciones del precio
df_ce_h = fn.f_metricas(param_ce=df_ce_h, param_ph=df_eurusd)

# -- tabla de escenarios y ocurrencias por cada indicador
# lista de indicadores
inds = list(set(df_ce_h['name']))
# indicador a elegir
ind = 4
# escenarios observados de indicador elegido
esc_obs = sorted(list(df_ce_h['escenario'][df_ce_h['name'] == inds[ind]]))
# escenarios posibles a existir
esc_exi = ['A', 'B', 'C', 'D']
# lista de escenarios faltantes
falta = list(np.where([esc_exi[i] not in list(set(esc_obs)) for i in range(0, 4)])[0])
esc_fal = [esc_exi[falta[i]] for i in range(0, len(falta))]
esc_fal

from itertools import groupby

conteo = [len(list(group)) for key, group in groupby(esc_obs)]
df_ind = pd.DataFrame({'esc': list(set(esc_obs)), 'con': conteo})

# si existe 1 o mas escenarios faltantes, agregar renglon con un 0
if falta:
    df_ind = df_ind.append(pd.DataFrame({'esc': esc_fal, 'con': [0]*len(esc_fal)}))

# Seleccionar indicadores y escenarios para pruebas ANOVA
# -- indicadores con mas de 40 observaciones.
# -- escenarios de cada indicador con mas de 30 observaciones.
# -- eligir aleatoriamente la misma cantidad de observaciones para 3 grupos distintos
# -- DataFrame con indicador, escenario, metrica que pasa prueba de invariabilidad.
