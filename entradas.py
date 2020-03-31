
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: entrada.py - diccionarios con informacion de entrada                         -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# parametros generales
parametros_stsc = {'data_series': ['mid_oc', 'mid_oc', 'mid_oc', 'mid_oc', 'mid_oc',
                                   'mid_hl', 'mid_hl', 'mid_hl', 'mid_hl', 'mid_hl',
                                   'close', 'close', 'close', 'close', 'close'],
                   'data_window': [10, 10, 20, 20, 30, 10, 10, 20, 20, 30, 10, 10, 20, 20, 30],
                   'mass_cores': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   'mass_batch': [1000, 2000, 1000, 2000, 3000, 1000, 2000, 1000, 2000, 3000,
                                  1000, 2000, 1000, 2000, 3000],
                   'mass_matches': [10, 10, 20, 20, 20, 10, 10, 20, 20, 20,
                                    10, 10, 20, 20, 20]}

# periodos disponibles para hacer busqueda
all_years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

# periodos elegidos para hacer la busqueda
years = all_years

# archivo con precios historicos a utilizar
archivo = 'USD_MXN_M1'

# tema para visualizacion de graficas
tema_base = {'tam_titulo_ejes': 15, 'tam_titulo_prin': 15, 'tam_texto_ejes': 14,
             'tam_linea_grafica': 1.5, 'tam_texto_grafica': 12, 'tam_texto_general': 14,
             'tam_texto_leyenda': 16,
             'color_titulo_principal': 'blue', 'color_titulo_ejes': 'dark grey',
             'color_texto_ejes': 'dark grey', 'color_background_grafica': 'white',
             'color_texto_general': 'dark grey', 'color_texto_tabla': 'dark grey',
             'color_texto_leyenda': 'dark grey',
             'color_linea_1': 'blue', 'color_linea_2': 'red', 'color_linea_3': 'red',
             'color_linea_4': 'red', 'color_linea_5': 'red', 'color_linea_6': 'red',
             'tam_linea_1': 1, 'tam_linea_2': 2, 'tam_linea_3': 3}

# dimensiones para graficas
dimensiones_base = {'figura_1': {'width': 840, 'height': 520},
                    'figura_2': {'width': 480, 'height': 480},
                    'figura_3': {'width': 480, 'height': 480}}
