
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


# -- ----------------------------------------------------- Lista de clases de indicadores -- #

ind_tip = {'nombre': ['12-Month Inflation', '1st half-month Inflation',
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
                         'Mercado Laboral', 'Energia', 'Actividad Economica',
                         'Mercado Laboral', 'Mercado Laboral', 'Mercado Laboral', 'Energia',
                         'Mercado Inmobiliario', 'Mercado Inmobiliario', 'Consumo',
                         'Flujos de capital', 'Flujos de capital', 'Flujos de capital',
                         'Consumo', 'Tasas de interes', 'Mercado Laboral',
                         'Actividad Economica', 'Consumo', 'Mercado inmobiliario',
                         'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo',
                         'Consumo', 'Consumo', 'Consumo', 'Mercado Laboral',
                         'Inflacion', 'Consumo', 'Consumo', 'Actividad Economica',
                         'Actividad Economica', 'Actividad Economica', 'Consumo', 'Consumo',
                         'Consumo', 'Energia', 'Energia', 'Mercado Laboral',
                         'Mercado inmobiliario', 'Mercado inmobilirario',
                         'Actividad Economica', 'Actividad Economica', 'Actividad Economica',
                         'Tasas de interes', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Inflacion', 'Mercado inmobilirario',
                         'Mercado inmobilirario', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica', 'Mercado Laboral',
                         'Mercado Laboral', 'Actividad economica', 'Actividad economica',
                         'Actividad economica', 'Actividad economica' 'Actividad economica',
                         'Mercado inmobilirario', 'Actividad economica',
                         'Actividad economica', 'Flujos de capital', 'Mercado inmobiliario',
                         'Mercado inmobilirario', 'Mercado Laboral', 'Mercado Laboral',
                         'Mercado inmobiliario', 'Consumo', 'Consumo' 'Consumo',
                         'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo',
                         'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo', 'Consumo',
                         'Consumo', 'Consumo', 'Mercado Inmobiliario', 'Flujos de capital',
                         'Actividad economica', 'Actividad economica', 'Actividad economica',
                         'Mercado Laboral', 'Mercado Laboral', 'Mercado Laboral',
                         'Mercado Laboral', 'Actividad economica'
                         ]}
