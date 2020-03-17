
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: datos.py - descarga de los datos necesarios para el proyecto                 -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import re

# -- In case of running Descarga y Lectura Masiva
# import funciones as fn
# from os import listdir, path
# from os.path import isfile, join

parametros_stsc = {'data_series': ['mid_oc', 'mid_oc', 'mid_oc', 'mid_oc', 'mid_oc',
                                   'mid_hl', 'mid_hl', 'mid_hl', 'mid_hl', 'mid_hl',
                                   'close', 'close', 'close', 'close', 'close'],
                   'data_window': [10, 10, 20, 20, 30, 10, 10, 20, 20, 30, 10, 10, 20, 20, 30],
                   'mass_cores': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   'mass_batch': [1000, 2000, 1000, 2000, 3000, 1000, 2000, 1000, 2000, 3000,
                                  1000, 2000, 1000, 2000, 3000],
                   'mass_matches': [10, 10, 20, 20, 20, 10, 10, 20, 20, 20,
                                    10, 10, 20, 20, 20]}

# dividir en 10 partes
all_years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

# -------------------------------------------------------- GUARDAR SOLO LOS SELECCIONADOS -- #
years = all_years
archivo = 'USD_MXN_M1'

# -- -------------------------------------------------------- Descarga de precios masivos -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Solo correr 1 vez para la descarga masiva de precios
#
# # token de OANDA https://www.oanda.com/demo-account/tpa/personal_token
# oa_ak = '8' + 'b50d0cc9f97037e5b6e7b28de8be537-bccc5ff454afcd2ace0f774a57534ca' + 'd'
# oa_in = "USD_MXN"  # Instrumento
# oa_gn = "M1"       # Granularidad de velas (M1: Minuto, M5: 5 Minutos, M15: 15 Minutos)
# fini = pd.to_datetime("2010-01-01 00:00:00").tz_localize('GMT')  # Fecha inicial
# ffin = pd.to_datetime("2020-01-03 00:00:00").tz_localize('GMT')  # Fecha final
#
# # -- solicitar 1 vez la descarga de precios masivos
# df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn, p3_inst=oa_in,
#                              p4_oatk=oa_ak, p5_ginc=4910)
# # formato a columnas
# columns = list(df_pe.columns)
# columns = [i.lower() for i in columns]
# df_pe.rename(columns=dict(zip(df_pe.columns[0:], columns)), inplace=True)
#
# # escribir cada parte en un archivo para que sea menos pesado cada uno y subir todos a github
# for a in years:
#     lista = [df_pe.loc[i, 'timestamp'].year == a for i in range(0, len(df_pe['timestamp']))]
#     df_escribir = df_pe.iloc[lista, :]
#     nombre_a = archivo + '_' + str(a)
#     df_escribir.to_csv(r'datos/price_files/' + nombre_a + '.csv', index=False)

# -- ---------------------------------------------------------- Lectura masiva de precios -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- leer y concatenar todos los archivos en un DataFrame

archivos = list()
# ciclo para leer los archivos
for a in years:
    nombre_a = 'datos/price_files/' + archivo + '_' + str(a) + '.csv'
    # print(nombre_a)
    archivos.append(pd.read_csv(nombre_a))

# concatenar todos los archivos
df_precios = pd.concat(archivos, sort=True)

# calcular el valor 'mid' como el punto medio entre close y open de cada vela
# como proxy 1 de volatilidad
df_precios['mid_oc'] = 0
df_precios['mid_oc'] = (df_precios['close'] + df_precios['open'])/2

# calcular el valor 'mid_hl' como el punto medio entre high y low de cada vela
# como proxy 2 de volatilidad
df_precios['mid_hl'] = 0
df_precios['mid_hl'] = (df_precios['high'] + df_precios['low'])/2

# modificar el tipo de dato para la columna timestamp
df_precios['timestamp'] = pd.to_datetime(list(df_precios['timestamp']))
df_precios = df_precios.reset_index(inplace=False, drop=True)

# -- ------------------------------------------ Lectura masiva de archivos de indicadores -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Solo correr 1 vez para la lectura masiva de archivos con indicadores

# # lista de todos los archivos dentro del directorio files
# abspath = path.abspath('datos/econ_files')
# files = [f for f in listdir(abspath) if isfile(join(abspath, f))]
#
# # Lista con paises
# economias = ['Mexico' if files[i].find('Mexico') != -1 else 'United States'
#              for i in range(0, len(files))]
#
# # Lista con nombres
# indicadores = [files[i][0:files[i].find(' - ')] for i in range(0, len(files))]
#
# # DataFrame de control general
# df_ce_g = pd.DataFrame({'ind': indicadores, 'econ': economias})
#
# # DataFrame con historicos
# df_ce = fn.f_unir_ind(param_dir=path.abspath('datos/econ_files/'))
#
# # Escribir archivo
# df_ce.to_csv(r'datos/econ_files/' + 'ECON_USD_MXN' + '.csv', index=False)

# -- ------------------------------------------------------- Lectura de archivo unificado -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- leer un csv en y guardar en un DataFrame

df_ce = pd.read_csv('datos/econ_files/' + 'ECON_USD_MXN' + '.csv')

lista = list()
# Convertir a tipo datetime
df_ce['timestamp'] = pd.to_datetime(df_ce['timestamp'])
# Crear columna
df_ce['year'] = [df_ce['timestamp'][i].year for i in range(0, len(df_ce['timestamp']))]
# Seleccionar los deseados
df_ce = df_ce.loc[df_ce['year'].isin(years)]
# Resetear el index
df_ce.reset_index(inplace=True, drop=True)
# Reordenar en ascendente por fechas
df_ce = df_ce.sort_values(by=['timestamp'])

# Eliminar de la busqueda publicaciones que son fuera del mercado
df_ce['weekday'] = [df_ce.loc[i, 'timestamp'].weekday()
                    for i in range(0, len(df_ce['timestamp']))]
df_ce['hour'] = [df_ce.loc[i, 'timestamp'].hour for i in range(0, len(df_ce['timestamp']))]
# extraer los indices
indexNames = df_ce[(df_ce['weekday'] == 5) | (df_ce['weekday'] == 4) & (df_ce['hour'] > 22) |
                   (df_ce['weekday'] == 6) & (df_ce['hour'] < 22)].index
# eliminar renglones
df_ce.drop(indexNames, inplace=True)
# ordenar por nombre alfabeticamente
df_ce.sort_values(by=['name'], ascending=True, inplace=True)
# resetear indice
df_ce = df_ce.reset_index(inplace=False, drop=True)

# quitar todos los valores que no sean economias definidas
currencies = list()
for r in range(0, len(df_ce['currency'])):
    if len(re.findall(r'United States', df_ce['currency'][r])):
        currencies.append('USA')
    elif len(re.findall(r'Mexico', df_ce['currency'][r])):
        currencies.append('MEX')

df_ce['currency'] = currencies

# crear lista de nombres cortos
nombres_cortos = ['ind_' + df_ce['name'][i][:2] + '_' + df_ce['currency'][i] + '_' + str(i)
                  for i in range(0, len(df_ce['name']))]

# crear dataframe con nombres de referencia
df_ce_nombres = df_ce.copy()

# crear ID unico
nombres_or = df_ce['name']
currencies_or = df_ce['currency']
df_ce['id'] = [nombres_or[i].replace(' ', '')[0:6] + nombres_or[i].replace(' ', '')[-6:] +
               '_' + currencies_or[i] for i in range(0, len(nombres_or))]

# -- ----------------------------------------------------- Lista de clases de indicadores -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Una lista para relacionar el indicador con su clase economica.

lista_n = {'nombre': ['12-Month Inflation', '1st half-month Inflation',
                      '3-Month Bill Auction', '3-Year Note Auction',
                      '30-Year Bond Auction', '4-Week Bill Auction',
                      '6-Month Bill Auction', 'ADP Employment Change',
                      'API Weekly Crude Oil Stock', 'Accumulated Current AccountGDP',
                      'Average Hourly Earnings MoM', 'Average Hourly Earnings YoY',
                      'Average Weekly Hours', 'Baker Hughes US Oil Rig Count',
                      'Building Permits Change', 'Building Permits MoM',
                      'Business Inventories', 'CFTC Gold NC Net Positions',
                      'CFTC Oil NC Net Positions', 'CFTC USD NC Net Positions',
                      'Capacity Utilization', 'Central Bank Interest Rate',
                      'Challenger Job Cuts', 'Chicago Fed National Activity Index',
                      "Chicago Purchasing Managers' Index", 'Construction Spending MoM',
                      'Consumer Confidence', 'Consumer Confidence s.a',
                      'Consumer Credit Change', 'Consumer Price Index Core s.a',
                      'Consumer Price Index MoM', 'Consumer Price Index YoY',
                      'Consumer Price Index ex Food  Energy MoM',
                      'Consumer Price Index ex Food  Energy YoY',
                      'Consumer Price Index n.s.a MoM', 'Continuing Jobless Claims',
                      'Core Inflation', 'Core Personal Consumption Expenditure',
                      'Core Personal Consumption Expenditures QoQ', 'Current Account',
                      'Current Account,  QoQ', 'Dallas Fed Manufacturing Business Index',
                      'Durable Goods Orders', 'Durable Goods Orders ex Defense',
                      'Durable Goods Orders ex Transportation', 'EIA Crude Oil Stocks Change',
                      'EIA Natural Gas Storage Change', 'Employment Cost Index',
                      'Existing Home Sales Change MoM', 'Existing Home Sales MoM',
                      'Export Price Index MoM', 'Export Price Index YoY',
                      'Factory Orders MoM', 'Fed Interest Rate Decision',
                      'Fiscal Balance, pesos', 'Goods Trade Balance',
                      'Gross Domestic Product Annualized', 'Gross Domestic Product Price Index',
                      'Gross Domestic Product QoQ', 'Gross Domestic Product YoY',
                      'Headline Inflation', 'Housing Starts Change',
                      'Housing Starts MoM', 'IBDTIPP Economic Optimism MoM',
                      'ISM Manufacturing PMI', 'ISM Manufacturing Prices Paid',
                      'ISM Non-Manufacturing PMI', 'ISM-NY Business Conditions Index',
                      'Import Price Index MoM', 'Industrial Output MoM',
                      'Industrial Output YoY', 'Industrial Production MoM',
                      'Initial Jobless Claims', 'Labor Force Participation Rate',
                      'Markit Manufacturing PMI', 'Markit PMI Composite',
                      'Markit Services PMI', 'Michigan Consumer Sentiment Index',
                      'Monthly Budget Statement', 'NAHB Housing Market Index',
                      'NFIB Business Optimism Index', 'NY Empire State Manufacturing Index',
                      'Net Long-Term TIC Flows', 'New Home Sales Change MoM',
                      'New Home Sales MoM', 'Nonfarm Payrolls',
                      'Nonfarm Productivity', 'Pending Home Sales YoY',
                      'Personal Consumption Expenditures',
                      'Personal Consumption Expenditures Prices QoQ', 'Personal Income MoM',
                      'Personal Spending', 'Philadelphia Fed Manufacturing Survey',
                      'Private Spending QoQ', 'Private Spending YoY',
                      'Producer Price Index MoM', 'Producer Price Index YoY',
                      'Producer Price Index ex Food  Energy MoM',
                      'Producer Price Index ex Food  Energy YoY', 'Redbook Index MoM',
                      'Redbook Index YoY', 'Retail Sales Control Group',
                      'Retail Sales MoM', 'Retail Sales YoY',
                      'Retail Sales ex Autos MoM', 'SPCase-Shiller Home Price Indices YoY',
                      'Total Net TIC Flows', 'Trade Balance',
                      'Trade Balance sa, ', 'Trade Balance, ',
                      'Unemployment Rate', 'Unit Labor Costs',
                      'Wholesale Inventories'],
           'categoria': ['Inflacion', 'Inflacion', 'Subasta de bonos', 'Subasta de bonos',
                         'Subasta de bonos', 'Subasta de bonos', 'Subasta de bonos',
                         'Mercado Laboral', 'Energia', 'Actividad economica',
                         'Mercado Laboral', 'Mercado Laboral', 'Mercado Laboral', 'Energia',
                         'Mercado inmobiliario', 'Mercado inmobiliario', 'Consumo',
                         'Flujos de capital', 'Flujos de capital', 'Flujos de capital',
                         'Consumo', 'Tasas de interes', 'Mercado Laboral',
                         'Actividad economica', 'Consumo', 'Mercado inmobiliario',
                         'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo',
                         'Consumo', 'Consumo', 'Consumo', 'Mercado Laboral',
                         'Inflacion', 'Consumo', 'Consumo', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Consumo', 'Consumo',
                         'Consumo', 'Energia', 'Energia', 'Mercado Laboral',
                         'Mercado inmobiliario', 'Mercado inmobiliario',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Tasas de interes', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Inflacion', 'Mercado inmobiliario',
                         'Mercado inmobiliario', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Mercado Laboral',
                         'Mercado Laboral', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica',
                         'Mercado inmobiliario', 'Actividad economica',
                         'Actividad economica', 'Flujos de capital', 'Mercado inmobiliario',
                         'Mercado inmobiliario', 'Mercado Laboral', 'Mercado Laboral',
                         'Mercado inmobiliario', 'Consumo', 'Consumo',
                         'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo',
                         'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo',
                         'Consumo', 'Consumo', 'Mercado inmobiliario', 'Flujos de capital',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Mercado Laboral', 'Mercado Laboral', 'Mercado Laboral',
                         'Mercado Laboral', 'Actividad economica'
                         ]}

# Tabla completa Indicadores y clasificacion de tipo economico
df_ce_ca = pd.DataFrame(lista_n)
set(df_ce_ca['categoria'])


# tabla = pd.DataFrame({'indicador': ['Trade Balance sa', 'Actividad Economica'
# 'Continuing Jobless Claims', 'Mercado Laboral'
# 'CFTC USD NC Net Positions', 'Flujos de capital'
# 'Consumer Confidence', 'Consumo'
# '3-Year Note Auction', 'Subasta de bonos'
# '12-Month Inflation', 'Inflacion'
# 'API Weekly Crude Oil Stock', 'Energia'
# 'Building Permits Change', 'Mercado inmobiliario'
# 'Central Bank Interest Rate', 'Tasas de interes'
