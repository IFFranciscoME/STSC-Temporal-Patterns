
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# Importar Precios historicos M1 del 2019
from datos import df_usdmxn, df_ce
import funciones as fn
import numpy as np
import pandas as pd

# -- -------------------------------------------------------------------- Data generation -- #
# Importar Calendario Economico

# Calcular escenarios para indicadores
df_ce = fn.f_escenario(p0_datos=df_ce)

# -- ------------------------------------------------------ Indicator-Scenario Selection -- #

# -- Calcular las metricas para reacciones del precio, para medir el cambio en la varianza
df_ce = fn.f_metricas(param_ce=df_ce, param_ph=df_usdmxn)

# -- ---------------------------------------------------------- Data exploratory analysis -- #

# -- Statistics of scenario ocurrence

# -- Scenario statistics visualizations

# -- Boxplot for each indicator_scenario metrics values, for all the 4 metrics

# -- Tabla de ocurrencias de escenario para cada indicador
df_indes = fn.f_tabla_ind(param_ce=df_ce)

# -- Seleccionar indicadores y escenarios para pruebas ANOVA
# indicadores con mas de 40 observaciones.
indes_out_1 = df_indes[df_indes['T'] < 40].index
df_indes.drop(indes_out_1, inplace=True)
df_indes.reset_index(inplace=True, drop=True)

# escenarios de cada indicador con mas de 12 observaciones
indes_out_2 = df_indes[(df_indes['A'] < 12) & (df_indes['B'] < 12) &
                       (df_indes['C'] < 12) & (df_indes['D'] < 12)].index
df_indes.drop(indes_out_2, inplace=True)
df_indes.reset_index(inplace=True, drop=True)

# -- ------------------------------------------------------- FUNCION: Tabla Pruebas ANOVA -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- construir la tabla ANOVA

# -- construir tabla de indicador_escenario con los candidatos
param_tab = df_indes
indicadores = list(set(df_indes['indicador']))

# -- escenarios diferentes de 0 para el indicador

# nombre de indicador
tab_ind = []
# nombre de escenario
tab_esc = []
# observaciones totales
tab_obs = []
# cantidad de observaciones por grupo
tab_grp = []
# 1: no hay variabilidad (se utiliza indicador-escenario)
# 0: hay variabilidad (se descarta indicador-escenario)
tab_anova1 = []
tab_anova2 = []
tab_anova3 = []
tab_anova4 = []

for ind in indicadores:
    data = df_indes[df_indes['indicador'] == ind]
    esc = list()
    n_esc = list()
    p_esc = list()

    # -- -- encontrar el escenario donde hay mas de 30 observaciones
    if list(data['A'])[0] >= 30:
        esc.append('A')
        n_esc.append(list(data['A'])[0])
        p_esc.append(int(list(data['A'])[0]/3))
    if list(data['B'])[0] >= 30:
        esc.append('B')
        n_esc.append(list(data['B'])[0])
        p_esc.append(int(list(data['B'])[0] / 3))
    if list(data['C'])[0] >= 30:
        esc.append('C')
        n_esc.append(list(data['C'])[0])
        p_esc.append(int(list(data['C'])[0] / 3))
    if list(data['D'])[0] >= 30:
        esc.append('D')
        n_esc.append(list(data['D'])[0])
        p_esc.append(int(list(data['D'])[0] / 3))

    # crear listas de valores encontrados
    if len(esc) != 0:
        tab_ind.extend([ind]*len(esc))
        tab_esc.extend(esc)
        tab_obs.extend(n_esc)
        tab_grp.extend(p_esc)

# formar DataFrame con listas previamente construidas
df_anova = pd.DataFrame({'ind': tab_ind, 'esc': tab_esc, 'obs': tab_obs, 'grp': tab_grp,
                         'anova_hl': [0]*len(tab_ind),
                         'anova_ol': [0]*len(tab_ind),
                         'anova_ho': [0]*len(tab_ind),
                         'anova_co': [0]*len(tab_ind)})

# -- eligir aleatoriamente la misma cantidad de observaciones para 3 grupos distintos
df_grp_anova = []

# elegir N observaciones, aleatoriamente con dist uniforme sin reemplazo, del total
# de observaciones del indicador IM.

i = 0
n_ale_1 = df_anova.iloc[i, 3]
n_ale_2 = df_anova.iloc[i, 3]
n_ale_3 = df_anova.iloc[i, 2] - n_ale_1 - n_ale_2

im = df_anova.iloc[0, 0]
obs = list(df_ce[df_ce['name'] == im].index)
muestra_1 = np.random.choice(obs, n_ale_1, replace=False)
muestra_2 = np.random.choice(obs, n_ale_2, replace=False)
muestra_3 = np.random.choice(obs, n_ale_3, replace=False)

# -- Hacer prueba ANOVA a cada indicador_escenario con sus 3 grupos
