
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# Importar Precios historicos M1 del 2019
# from datos import df_eurusd, df_ce_g
import funciones as fn
from os import path

# -- -------------------------------------------------------------------- Data generation -- #
# Importar Calendario Economico
df_ce_g = fn.f_unir_ind(param_dir=path.abspath('datos/econ_files/'))

# Calcular escenarios para indicadores
df_ce_g = fn.f_escenario(p0_datos=df_ce_g)

# -- ---------------------------------------------------------- Data exploratory analysis -- #

# Statistics of scenario ocurrence

# Scenario statistics visualizations

# -- ------------------------------------------------------ Indicator-Escenario Selection -- #

# Indicator selection as candidate to potential pattern generation

# Calculate 3 different price metrics to search for invariance in price reactions due to
# the release of the economic indicator

# Create 3 randomly selected groups of at least 20 data for each sceario of each indicator

# analysis of unequal sample size condition for ANOVA test for mean invariance between groups

# Test for invariance in 3 price metrics for each indicator, to look for homogeinity in price
# response as a potential condition to a pattern presence due to the release of the economic
# indicator

# subset the EI list with the ones that show invariance in the mean response for the metrics
