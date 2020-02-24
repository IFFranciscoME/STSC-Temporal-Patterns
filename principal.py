
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

# Indicator selection as candidate to potential pattern generation
# Calculate 3 different price metrics to search for invariance in price reactions due to
# the release of the economic indicator


# Create 3 randomly selected groups of at least 20 data for each sceario of each indicator

# analysis of unequal sample size condition for ANOVA test for mean invariance between groups

# Test for invariance in 3 price metrics for each indicator, to look for homogeinity in price
# response as a potential condition to a pattern presence due to the release of the economic
# indicator

# subset the EI list with the ones that show invariance in the mean response for the metrics
