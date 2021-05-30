
# -- ------------------------------------------------------------------------------------ -- #
# -- 
# -- 
# -- 
# -- 
# -- ------------------------------------------------------------------------------------ -- #

# Remover todos los objetos del "Environment"
rm(list = ls())

suppressMessages(library(knitr))  # Opciones de documentacion + codigo
suppressMessages(library(ggplot2))           # Leer archivos XLSx
suppressMessages(library(kableExtra))         # Tablas en HTML
options("scipen"=100, "digits"=4)

# tema_base = ('tam_titulo_ejes': 15, 'tam_titulo_prin': 15, 'tam_texto_ejes': 14,
#   'tam_linea_grafica': 1.5, 'tam_texto_grafica': 12, 'tam_texto_general': 14,
#   'color_titulo_principal': 'blue', 'color_titulo_ejes': 'blue',
#   'color_texto_ejes': 'blue', 'color_background_grafica': 'white',
#   'color_texto_general': 'grey', 'color_texto_tabla': 'grey',
#   'color_linea_1': 'red', 'color_linea_2': 'red', 'color_linea_3': 'red',
#   'color_linea_4': 'red', 'color_linea_5': 'red', 'color_linea_6': 'red')

# dimensiones_base = {'figura_1': {'width': 480, 'height': 480},
#   'figura_2': {'width': 480, 'height': 480},
#   'figura_3': {'width': 480, 'height': 480}}

# -- ----------------------------------------------------- GRAFICA 1: Serie OHLC + Lineas -- #
# -- --------------------------------------------------------------------------------------- #
# -- --

vs_ohlc_series <- function(param_ts, param_ohlc, param_s1, param_s2, param_s3, 
                           param_theme, param_dim) {

  return (1)
}

# -- -------------------------------------------------- GRAFICA 2: Serie original + Motif -- #
# -- --------------------------------------------------------------------------------------- #
# -- --

vs_serie_motif <- function(param_q, param_p, param_theme, param_dim){
  
  
  
  return (1)
}



# -- --------------------------------------------------- GRAFICA 3: Barras de ocurrencias -- #
# -- --------------------------------------------------------------------------------------- #
# -- --

vs_barras_ocurr <- function(param_theme, param_dim){
  
  
  
  return (1)
}
