
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: funciones.py - funciones de procesamiento para usar en el proyecto           -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

from os import listdir, path
from os.path import isfile, join
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos
from datetime import timedelta

import pickle
import json
import numpy as np
import pandas as pd
import warnings
import statsmodels.api as sm                              # modelos estadisticos: anova
from statsmodels.formula.api import ols                   # modelo lineal con ols
import multiprocessing as mp                              # procesamiento en paralelo

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import mass_ts as mass

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso


# -- --------------------------------------------------------- FUNCION: Descargar precios -- #
# -- --------------------------------------------------------------------------------------- #
# -- Descargar precios historicos con OANDA

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Parameters
    ----------
    p0_fini : str : fecha inicial para descargar precios en formato str o pd.to_datetime
    p1_ffin : str : fecha final para descargar precios en formato str o pd.to_datetime
    p2_gran : str : M1, M5, M15, M30, H1, H4, H8, segun formato solicitado por OANDAV20 api
    p3_inst : str : nombre de instrumento, segun formato solicitado por OANDAV20 api
    p4_oatk : str : OANDAV20 API
    p5_ginc : int : cantidad de datos historicos por llamada, obligatorio < 5000

    Returns
    -------
    dc_precios : pd.DataFrame : Data Frame con precios TOHLC

    Debugging
    ---------
    p0_fini = pd.to_datetime("2019-01-01 00:00:00").tz_localize('GMT')
    p1_ffin = pd.to_datetime("2019-12-31 00:00:00").tz_localize('GMT')
    p2_gran = "M1"
    p3_inst = "USD_MXN"
    p4_oatk = '8b50d0cc9f97037e5b6e7b28de8be537-bccc5ff454afcd2ace0f774a57534cad'
    p5_ginc = 4900
    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """
        Parameters
        ----------
        p0_start : str : fecha inicial
        p1_end : str : fecha final
        p2_inc : int : incremento en cantidad de elementos
        p3_delta : str : intervalo para medir elementos ('minutes', 'hours', 'days')

        Returns
        -------
        ls_result : list : lista con fechas intermedias a frequencia solicitada

        Debugging
        ---------
        p0_start = p0_fini
        p1_end = p1_ffin
        p2_inc = p5_ginc
        p3_delta = 'minutes'
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4990:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            # print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final


# -- ---------------------------------------------------------- FUNCION: Unir indicadores -- #
# -- --------------------------------------------------------------------------------------- #
# -- Unir todos los archivos de indicadores descargados

def f_unir_archivos(param_dir):
    """
    Parameters
    ----------
    param_dir : str : direccion de la carpeta que contiene todos los archivos a unir

    Returns
    -------
    salida : pd.DataFrame() : DataFrame con todos los indicadores unidos verticalmente

    Debugging
    ---------
    param_dir = path.abspath('datos/econ_files/')

    """

    # archivos descargados de historicos de cada indicador
    files = [f for f in listdir(param_dir) if isfile(join(param_dir, f))]

    # -- Elegir archivo de indicador de acuerdo a criterio

    # Prueba 1: Tiene, cuando mucho, 2 renglones con "NaNs" en las 3 columnas
    files_p1 = list()
    for j in range(0, len(files)):
        archivo = pd.read_csv(param_dir + '/' + files[j])

        # - prueba de '2 o menos casos con NaNs en todas las columnas'
        elim1 = np.where(np.isnan(archivo['Actual']) & np.isnan(archivo['Consensus']) &
                         np.isnan(archivo['Previous']))[0]

        # - prueba de '2 o menos casos con NaNs en columna Actual'
        elim2 = list(np.where(np.isnan(archivo['Actual']))[0])

        files_p1.append(files[j]) if len(elim1) <= 2 | len(elim2) <= 2 \
            else '2 o menos casos con NaNs'

    # OPCIONAL: Eliminar indicadores que tengan 5 o mas faltantes en consensus

    files_p2 = files_p1
    # files_p2 = list()
    # for k in range(0, len(files_p1)):
    #     archivo = pd.read_csv(param_dir + '/' + files_p1[k])
    #     # - prueba '5 o menos casos sin consensus'
    #     elim2 = np.where(np.isnan(archivo['Consensus']))
    #     files_p2.append(files_p1[k]) if len(elim2[0]) <= 5 else '5 o menos sin consensus'

    # Acomodos de datos
    archivos = list()
    for k in range(0, len(files_p2)):
        archivos.append(pd.read_csv(param_dir + '/' + files_p2[k]))

        # Acomodo 1: Separar nombre de indicador y de currency que afecta
        archivos[k]['Name'] = files_p2[k][0:files_p2[k].find(' - ')]
        archivos[k]['Currency'] = files_p2[k][files_p2[k].find(' - ')+3:]

        # Acomodo 2: Para 'Previous' == NaN, asignar el valor de 'Actual' de t-1
        ind_prev = list(np.where(np.isnan(archivos[k]['Previous']))[0])
        ind_actu = list(np.where(np.isnan(archivos[k]['Previous']))[0] - 1)
        archivos[k]['Previous'][ind_prev] = list(archivos[k]['Actual'][ind_actu])

        # Acomodo 3: Para 'Consensus' == NaN, asignar el valor de 'Previous'
        ind_cons = list(np.where(np.isnan(archivos[k]['Consensus']))[0])
        archivos[k]['Consensus'][ind_cons] = list(archivos[k]['Previous'][ind_cons])

    # Concatenar todos los archivos en un solo DataFrame
    df_ce = pd.concat([archivos[i] for i in range(0, len(files_p2))])

    # Renombrar todas las columnas del dataframe con una lista de nombres
    columns = list(df_ce.columns)
    columns = [i.lower() for i in columns]
    df_ce.rename(columns=dict(zip(df_ce.columns[0:], columns)), inplace=True)

    # Elegir columnas para data frame final (no se incluye revised)
    df_ce = df_ce[['datetime', 'name', 'currency', 'actual', 'consensus', 'previous']]
    df_ce.rename(columns={'datetime': 'timestamp'}, inplace=True)

    # Conversion de tipo de dato timestamp
    df_ce['timestamp'] = pd.to_datetime(list(df_ce['timestamp'])).tz_localize('GMT')
    df_ce.reset_index(inplace=True, drop=True)

    df_ce['timestamp'] = [df_ce['timestamp'][i].floor('min')
                          for i in range(0, len(df_ce['timestamp']))]

    return df_ce


# -- ----------------------------------------------------- FUNCION: Clasificar escenarios -- #
# -- --------------------------------------------------------------------------------------- #
# -- Clasificacion de escenarios

def f_escenario(p0_datos):
    """
    Parameters
    ----------
    p0_datos : pd.DataFrame : con columnas name, actual, consensus, previous

    Returns
    -------
    datos : pd.DataFrame :

    Debugging
    ---------
    p0_datos = df_ce_g

    """

    # Renombrar todas las columnas del dataframe con una lista de nombres
    columns = list(p0_datos.columns)
    columns = [i.lower() for i in columns]
    p0_datos.rename(columns=dict(zip(p0_datos.columns[0:], columns)), inplace=True)

    # inicializar la columna esc, habra los siguientes: A, B, C, D
    p0_datos['esc'] = 'X'

    # -- -- A: actual >= previous & actual >= consensus & consensus >= previous
    p0_datos['esc'][((p0_datos['actual'] >= p0_datos['previous']) &
                          (p0_datos['actual'] >= p0_datos['consensus']))] = 'A'

    # -- -- B: actual >= previous & actual >= consensus & consensus < Precious
    p0_datos['esc'][((p0_datos['actual'] >= p0_datos['previous']) &
                          (p0_datos['actual'] < p0_datos['consensus']))] = 'B'

    # -- -- C: actual >= previous & actual < consensus & consensus >= previous
    p0_datos['esc'][((p0_datos['actual'] < p0_datos['previous']) &
                          (p0_datos['actual'] >= p0_datos['consensus']))] = 'C'

    # -- -- D: actual >= previous & actual < consensus & consensus < previous
    p0_datos['esc'][((p0_datos['actual'] < p0_datos['previous']) &
                          (p0_datos['actual'] < p0_datos['consensus']))] = 'D'

    return p0_datos


# -- ---------------------------------------------------- FUNCION: Parametros de reaccion -- #
# -- --------------------------------------------------------------------------------------- #
# -- Calculo de parametros medidores de "reaccion del mercado"

def f_reaccion(p0_i, p1_ad, p2_ph, p3_ce):
    """
    Parameters
    ----------
    p0_i : int : indexador para iterar en los datos de entrada
    p1_ad : int : cantidad de precios futuros que se considera la ventana (t + p1_ad)
    p2_ph : pd.DataFrame : precios en OHLC con columnas: timestamp, open, high, low, close
    p3_ce : DataFrame : calendario economico con columnas: timestamp, name, actual,
                        consensus, previous

    Returns
    -------
    resultado : dict : diccionario con resultado final con 3 elementos como resultado

    Debugging
    ---------
    p0_i = 0
    p1_ad = 30
    p2_ph = df_precios
    p3_ce = df_ce
    """

    # Debugging y control interno
    # print(p0_i)
    # print(' fecha del ce a buscar es: ' + str(p3_ce['timestamp'][p0_i]))
    mult = 10000

    # Revision si no encuentra timestamp exacto, recorrer 1 hacia atras iterativamente
    # hasta encontrar el mismo
    indice_1 = list(np.where(p2_ph['timestamp'] == p3_ce['timestamp'][p0_i])[0])
    i = 0
    while not indice_1:
        i += 1
        indice_1 = list(np.where(p2_ph['timestamp'] == (p3_ce['timestamp'][p0_i]) -
                                 timedelta(minutes=i))[0])

    # Indices de coincidencias
    indice_1 = indice_1[0]
    indice_2 = indice_1 + p1_ad

    # Calculo de metricas de reaccion
    ho = round((max(p2_ph['high'][indice_1:indice_2]) - p2_ph['open'][indice_1])*mult, 2)
    hl = round((max(p2_ph['high'][indice_1:indice_2]) -
                min(p2_ph['low'][indice_1:indice_2])) * mult, 2)
    ol = round((p2_ph['open'][indice_1] - min(p2_ph['low'][indice_1:indice_2]))*mult, 2)
    co = round((p2_ph['close'][indice_1] - min(p2_ph['open'][indice_1:indice_2]))*mult, 2)

    # Diccionario con resultado final
    resultado = {'ho': ho, 'ol': ol, 'co': co, 'hl': hl, 'data': p2_ph[indice_1:indice_2]}

    return resultado


# -- ------------------------------------------------------ FUNCION: Metricas de reaccion -- #
# -- --------------------------------------------------------------------------------------- #
# -- Calculo de metricas de precios para pruebas ANOVA

def f_metricas(param_ce, param_ph, param_window):
    """
    Parameters
    ----------
    param_ce : pd.DataFrame : Economic calendar with 'timestamp', 'name', 'actual',
                              'consensus', 'previous'
    param_ph : pd.DataFrame : Historical prices 'timestamp', 'open', 'high', 'low', 'close'
    param_window : int : Cantidad de datos hacia el futuro para calculo de metricas

    Returns
    -------
    r_metricas : pd.DataFrame : para_ce + metricas

    Debugging
    ---------
    param_ce = df_ce
    param_ph = df_precios
    param_window = 30
    """

    indices_ce = list(param_ce['timestamp'].index)
    # --------------------------------------------------------- PARALELIZACION DE PROCESO -- #

    # Reaccion del precio para cada escenario (PARALELO)
    # inicializar el pool con el maximo de procesadores disponibles
    pool = mp.Pool(mp.cpu_count())
    d_reaccion = pool.starmap(f_reaccion, [(i, param_window, param_ph, param_ce)
                                           for i in range(0, len(indices_ce))])
    pool.close()

    # --------------------------------------------------------- VERSION SIMPLE DE PROCESO -- #
    # Reaccion del precio para cada escenario (SIMPLE)
    # d_reaccion = [f_reaccion(p0_i=i, p1_ad=psiguiente, p2_ph=param_ph, p3_ce=param_ce)
    #               for i in range(0, len(indices_ce))]

    # Acomodar resultados en columnas
    param_ce['ho'] = [d_reaccion[j]['ho'] for j in range(0, len(param_ce['timestamp']))]
    param_ce['hl'] = [d_reaccion[j]['hl'] for j in range(0, len(param_ce['timestamp']))]
    param_ce['ol'] = [d_reaccion[j]['ol'] for j in range(0, len(param_ce['timestamp']))]
    param_ce['co'] = [d_reaccion[j]['co'] for j in range(0, len(param_ce['timestamp']))]

    return param_ce


# -- ------------------------------------------------------ FUNCION: Tabla de ocurrencias -- #
# -- --------------------------------------------------------------------------------------- #
# -- Tabla de ocurrencias de escenarios para indicadores

def f_tabla_esc(param_ce):
    """
    Parameters
    ----------
    param_ce : pd.DataFrame : name, escenario

    Returns
    -------
    df_ocur : dict : indicador, A, B, C, D, T

    Debugging
    ---------
    Param_ce = df_ce_h

    """

    # resetear index de losd datos
    param_ce.reset_index(inplace=True, drop=True)

    # lista de indicadores
    inds = list(set(param_ce['name']))

    # Ocurrencias de escenario A en cada indicador
    l_a = [sum(list(param_ce['esc'][param_ce['name'] == inds[i]] == 'A'))
           for i in range(0, len(inds))]

    # Ocurrencias de esc B en cada indicador
    l_b = [sum(list(param_ce['esc'][param_ce['name'] == inds[i]] == 'B'))
           for i in range(0, len(inds))]

    # Ocurrencias de esc C en cada indicador
    l_c = [sum(list(param_ce['esc'][param_ce['name'] == inds[i]] == 'C'))
           for i in range(0, len(inds))]

    # Ocurrencias de esc D en cada indicador
    l_d = [sum(list(param_ce['esc'][param_ce['name'] == inds[i]] == 'D'))
           for i in range(0, len(inds))]

    # Ocurrencias total de cada indicador
    l_t = [len(param_ce['esc'][param_ce['name'] == inds[i]]) for i in range(0, len(inds))]

    # DataFrame con los datos finales
    df_ocur = pd.DataFrame({'indicador': inds, 'A': l_a, 'B': l_b, 'C': l_c, 'D': l_d,
                            'T': l_t})
    return df_ocur


# -- ----------------------------------------------------- FUNCION: Seleccion Indicadores -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Seleccion de indicadores

def f_seleccion_ind(param_ce, param_c1, param_c2):
    """
    Parameters
    ----------
    param_ce : DataFrame : Calendario Economico
    param_c1 : int : Cantidad de observaciones totales de indicador
    param_c2 : int : Cantidad de ocurrencias de escenarios por indicador

    Returns
    -------
    param_ce : DataFrame : DataFrame con indicadores seleccionados

    Debugging
    ---------
    param_ce = df_indes
    param_c1 = 40
    param_c2 = 12

    """

    # indicadores con mas de 40 observaciones.
    indes_out_1 = param_ce[param_ce['T'] < param_c1].index
    param_ce.drop(indes_out_1, inplace=True)
    param_ce.reset_index(inplace=True, drop=True)

    # escenarios de cada indicador con mas de 12 observaciones
    indes_out_2 = param_ce[(param_ce['A'] < param_c2) & (param_ce['B'] < param_c2) &
                           (param_ce['C'] < param_c2) & (param_ce['D'] < param_c2)].index
    param_ce.drop(indes_out_2, inplace=True)
    param_ce.reset_index(inplace=True, drop=True)

    return param_ce


# -- ------------------------------------------------------- FUNCION: Tabla Pruebas ANOVA -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- construir la tabla ANOVA

def f_anova(param_data1, param_data2):
    """
    Parameters
    ----------
    param_data1 : df_indes
    param_data2 : df_ce

    Returns
    -------

    """
    # -- construir tabla de indicador_escenario con los candidatos
    # param_tab = param_data1
    indicadores = list(set(param_data1['indicador']))

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
    # tab_anova1 = []
    # tab_anova2 = []
    # tab_anova3 = []
    # tab_anova4 = []

    for ind in indicadores:
        data = param_data1[param_data1['indicador'] == ind]
        esc = list()
        n_esc = list()
        p_esc = list()

        # -- -- encontrar el escenario donde hay mas de 30 observaciones
        if list(data['A'])[0] >= 30:
            esc.append('A')
            n_esc.append(list(data['A'])[0])
            p_esc.append(int(list(data['A'])[0] / 3))
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
            tab_ind.extend([ind] * len(esc))
            tab_esc.extend(esc)
            tab_obs.extend(n_esc)
            tab_grp.extend(p_esc)

    # formar DataFrame con listas previamente construidas
    df_anova = pd.DataFrame({'name': tab_ind, 'esc': tab_esc, 'obs': tab_obs, 'grp': tab_grp,
                             'anova_hl': [0] * len(tab_ind),
                             'anova_ol': [0] * len(tab_ind),
                             'anova_ho': [0] * len(tab_ind),
                             'anova_co': [0] * len(tab_ind)})

    # -- eligir aleatoriamente la misma cantidad de observaciones para 3 grupos distintos
    # elegir N observaciones, aleatoriamente con dist uniforme sin reemplazo, del total
    # de observaciones del indicador IM.

    for i in range(0, len(df_anova['name'])):

        n_ale_1 = df_anova.iloc[i, 3]
        n_ale_2 = n_ale_1
        n_ale_3 = df_anova.iloc[i, 2] - n_ale_1 - n_ale_2

        im = df_anova['name'][i]
        obs = list(param_data2[param_data2['name'] == im].index)
        muestra_1 = list(np.random.choice(obs, n_ale_1, replace=False))
        muestra_2 = list(np.random.choice(obs, n_ale_2, replace=False))
        muestra_3 = list(np.random.choice(obs, n_ale_3, replace=False))

        # datos de metricas para anova
        df_anova_test = pd.DataFrame({'muestras':
                                      [(df_anova['esc'][i] + '_' + str(1))]*len(muestra_1) + \
                                      [(df_anova['esc'][i] + '_' + str(2))]*len(muestra_2) + \
                                      [(df_anova['esc'][i] + '_' + str(3))]*len(muestra_3),
                                      'ho': list(param_data2['ho'][muestra_1]) + \
                                            list(param_data2['ho'][muestra_2]) + \
                                            list(param_data2['ho'][muestra_3]),
                                      'hl': list(param_data2['hl'][muestra_1]) + \
                                            list(param_data2['hl'][muestra_2]) + \
                                            list(param_data2['hl'][muestra_3]),
                                      'ol': list(param_data2['ol'][muestra_1]) + \
                                            list(param_data2['ol'][muestra_2]) + \
                                            list(param_data2['ol'][muestra_3]),
                                      'co': list(param_data2['co'][muestra_1]) + \
                                            list(param_data2['co'][muestra_2]) + \
                                            list(param_data2['co'][muestra_3])
                                      })

        # p > 0.05 --> se acepta la H0: NO hay diferencia significativa entre las medias
        # p < 0.05 --> se rechaza la H0: SI hay diferencia significativa entre las medias

        # ANOVA para metrica 1: High - Open
        model_ho = ols('ho ~ C(muestras)', data=df_anova_test).fit()
        anova_table_ho = sm.stats.anova_lm(model_ho, typ=2)
        df_anova['anova_ho'][i] = 1 if anova_table_ho['PR(>F)'][0] > 0.05 else 0

        # ANOVA para metrica 2: High - Low
        model_hl = ols('hl ~ C(muestras)', data=df_anova_test).fit()
        anova_table_hl = sm.stats.anova_lm(model_hl, typ=2)
        df_anova['anova_hl'][i] = 1 if anova_table_hl['PR(>F)'][0] > 0.05 else 0

        # ANOVA para metrica 3: Open - Low
        model_ol = ols('ol ~ C(muestras)', data=df_anova_test).fit()
        anova_table_ol = sm.stats.anova_lm(model_ol, typ=2)
        df_anova['anova_ol'][i] = 1 if anova_table_ol['PR(>F)'][0] > 0.05 else 0

        # ANOVA para metrica 4: Close - Open
        model_co = ols('co ~ C(muestras)', data=df_anova_test).fit()
        anova_table_co = sm.stats.anova_lm(model_co, typ=2)
        df_anova['anova_co'][i] = 1 if anova_table_co['PR(>F)'][0] > 0.05 else 0

    # Si pasa 4 anovas = Fuerte, 3 o 2 anovas = Util, 1 anova = Poco util,
    # 0 anovas = se descarta.

    return df_anova


# -- -------------------------------------------------- FUNCION: clustering subsecuencial -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- construir la tabla ANOVA

def f_ts_clustering(param_pe, param_row, param_ca_data, param_ce_data, param_tipo,
                    param_p_ventana, param_cores, param_batch, param_matches):
    """
    Parameters
    ----------
    param_pe : pd.DataFrame : dataframe con precios
    param_row :
    param_ce_data :
    param_ca_data :
    param_p_ventana :
    param_cores :
    param_tipo :
    param_batch :
    param_matches :

    Returns
    -------
    df_tabla_busqueda :

    Debugging
    ---------
    param_pe = df_precios # precios historicos para minar
    param_row = 4 # renglon de iteracion de candidatos
    param_ca_data = df_ind_3 # dataframe con candidatos a iterar
    param_ce_data = df_ce # dataframe con calendario completo
    param_tipo = 'mid'
    param_p_ventana = 30 # tamano de ventana para buscar serie de tiempo
    param_cores = 4 # nucleos con los cuales utilizar algoritmo
    param_batch = 300
    param_matches = 10
    """
    # almacenar resultados
    # dict_res = {'name': [], 'esc': [], 'timestamp': [],
    #             'tipo_1': [], 'tipo_2': [], 'tipo_3': [], 'tipo_4': []}

    # renglon con informacion de evento disparador candidato
    candidate_data = param_ca_data.iloc[param_row, :]
    # print('Ind disparador: ' + str(candidate_data['name']) + ' - ' + candidate_data['esc'])

    # datos completos de todas las ocurrencias del evento disparador candidato
    df_ancla = param_ce_data[(param_ce_data['esc'] == candidate_data['esc']) &
                             (param_ce_data['name'] == candidate_data['name'])]

    # todos los timestamps del calendario economico completo
    ts_serie_ce = list(param_ce_data['timestamp'])

    # inicializar contadores de ocurrencias por escenario ancla
    p1, p2, p3, p4 = 0, 0, 0, 0

    # Para guardar resultados parciales
    dict_res = {'ancla': df_ancla['id'].iloc[0], 'metricas': {}, 'datos': {}}

    # -- ------------------------------------------------------ OCURRENCIA POR OCURRENCIA -- #
    for ancla in range(0, len(df_ancla['timestamp'])):
        # ancla = 31
        # print(ancla)
        # datos de ancla para buscar hacia el futuro
        ancla_ocurr = df_ancla.iloc[ancla, ]
        # print('ind: ' + ancla_ocurr['name'] + ' ' + ancla_ocurr['esc'] + ' ' +
        #       str(ancla_ocurr['timestamp']))
        # fecha de ancla
        fecha_ini = ancla_ocurr['timestamp']

        # .. buscar recurrentemente la fecha mas cercana para construir serie y serie_p
        while len(param_pe[param_pe['timestamp'] == fecha_ini].index) == 0:
            fecha_ini = fecha_ini - timedelta(minutes=1)

        # se toma el timestamp de precios igual a timestamp del primer escenario del indicador
        ind_ini = param_pe[param_pe['timestamp'] == fecha_ini].index
        # fecha final es la fecha inicial mas un tamano de ventana arbitrario
        ind_fin = ind_ini + param_p_ventana

        # se construye la serie query
        df_serie_q = param_pe.copy().loc[ind_ini[0]:ind_fin[0], :]
        df_serie_q = df_serie_q.reset_index(drop=True)

        # se toma el mid como valor para construir series temporales
        serie_q = np.array(df_serie_q[param_tipo])

        # se construye la serie completa para busqueda (un array de numpy de 1 dimension)
        df_serie = param_pe.copy().loc[ind_ini[0]:, :]
        df_serie = df_serie.reset_index(drop=True)

        # se toma el mid como valor para construir series temporales
        serie = np.array(df_serie[param_tipo])

        try:
            # correr algoritmo y regresar los indices de coincidencias y las distancias
            mass_indices, mass_dists = mass.mass2_batch(ts=serie, query=serie_q,
                                                        batch_size=param_batch,
                                                        n_jobs=param_cores,
                                                        top_matches=param_matches)

            # Borrar inidice 0 de resultados por ser el mismo que la serie query
            origen = np.where(mass_indices == 0)[0][0]
            mass_indices = np.delete(mass_indices, origen)
            # mass_dists = np.delete(mass_dists, origen)
            # print('indices encontrados' + ' ' + str(mass_indices))

            # Indice de referencia de n-esima serie similar encontrada
            for indice in mass_indices:
                # indice = mass_indices[0]
                # print(indice)
                # DataFrame de n-esima serie patron similar encontrada
                df_serie_p = df_serie.copy().loc[indice:(indice + param_p_ventana), :]
                # print(df_serie_p.head())
                # print('Verificando patron con f_ini: ' +
                #       str(list(df_serie_p['timestamp'])[0]) + ' f_fin: ' +
                #       str(list(df_serie_p['timestamp'])[-1]))

                # Extraer el timestamp inicial para verificar si coincide con indicador
                ts_serie_p = list(df_serie_p['timestamp'])[0]

                # Busqueda si el timestamp inicial de cada uno de los patrones
                # encontrados es igual a alguna fecha de comunicacion de toda
                # la lista de indicadores que se tiene
                if ts_serie_p in ts_serie_ce:

                    # ID del evento ancla que genero patron hacia adelante
                    id_ocurrencia = ancla_ocurr['id'] + '_' + ancla_ocurr['esc'] +\
                                    '_' + str(ancla_ocurr['timestamp'])[:-6].replace(' ', '_')

                    match = np.where(param_ce_data['timestamp'] == ts_serie_p)[0]
                    encontrados = param_ce_data.loc[match, :]

                    # print(' ------------------ Coincidencia encontrada ------------------')
                    # print('buscando en: ' + id_ocurrencia)
                    # print(' ----------- Se encontro el patron que empieza en: -----------')
                    # print(ts_serie_p)
                    # print('en los siguientes casos: ')
                    # print(encontrados)

                    # -- contar y sacar los datos segun tipo
                    # Paso 1: tener un diccionario con la llave id_ocurrencia con la encontrada
                    # Paso 2: dentro de la llave id_ocurrencia tener la llave datos
                    dict_res['datos'].update({id_ocurrencia: {'ocurrencias': {},
                                                              'df_serie_q': df_serie_q,
                                                              'df_serie_p': df_serie_p}})

                    # Paso 3: hacer las llaves id_sub_ocurrencia para cada sub de ocurrencia
                    llaves = [encontrados['id'].iloc[j] + '_' + encontrados['esc'].iloc[j] +
                              '_' +
                              str(encontrados['timestamp'].iloc[j])[:-6].replace(' ', '_')
                              for j in range(0, len(encontrados['id']))]
                    dict_res['datos'][id_ocurrencia]['ocurrencias'] = llaves

                    enc = (encontrados['name'] == ancla_ocurr['name']) & \
                          (encontrados['esc'] == ancla_ocurr['esc'])

                    # TIPO 1: name == name & esc == esc
                    p1 = p1 + len(encontrados.loc[enc, 'name'])
                    # print('tipo_1 = ' + str(p1))

                    # TIPO 2: name == name
                    p2 = p2 + len(encontrados.loc[encontrados['name'] == ancla_ocurr['name'],
                                                  'name'])
                    # print('tipo_2 = ' + str(p2))

                    # TIPO 3: cualquiera en calendario
                    p3 = p3 + len(encontrados.loc[encontrados['name'] != ancla_ocurr['name'],
                                                  'name'])
                    # print('tipo_3 = ' + str(p3))

                    # TIPO 4: fuera de calendario
                    p4 = p4 + 0
                    # print('tipo_4 = ' + str(p4))

                else:
                    # TIPO 4: fuera de calendario
                    p4 += len(mass_indices)
                    # print('p4 = ' + str(p4))

        # tipo_4 = Cualquier otro punto en el tiempo
        except ValueError:
            # print('ValueError: problemas de indices en MASS-TS')
            p4 += 0
        except IndexError:
            # print('IndexError: problemas de indices en MASS-TS')
            p4 += 0

        # agregar al diccionario de resultados los casos encontrados
        dict_res.update({'metricas': {
            # Mismo Indicador + Mismo Escenario que la ancla
            'tipo_1': p1,
            # Mismo Indicador + Cualquier Escenario
            'tipo_2': p2,
            # Otro Indicador en la lista
            'tipo_3': p3,
            # Ninguna de las anteriores
            'tipo_4': p4}
        })

    return dict_res


# -- ------------------------------------------------- FUNCION: leer resultados de pickle -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Leer del archivo tipo pickle los resultados de la busqueda

def f_leer_resultados(param_carpeta, param_archivo):
    """
    Parameters
    ----------
    param_carpeta : str : direccion de la carpeta donde esta el archivo a leer
    param_archivo : str : nombre del archivo .p a leer

    Returns
    -------
    p_results : varios : el contenido del archivo

    Debugging
    ---------
    param_carpeta = 'datos/results_files_r2/'
    param_archivo = 'mid_oc_20_1_2000_20_r2'

    """

    # -- Re-abrir archivo pickle
    with open(param_carpeta + param_archivo, 'rb') as file:
        p_results = pickle.load(file)

    return p_results


# -- --------------------------------------------------------------- Tablas de ocurrencia -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- tablas de ocurrencia por indicador, tipo de indicador, escenario. para cada ciclo

def f_tablas_ocur(param_carpeta):
    """
    Parameters
    ----------
    param_carpeta : str : direccion de carpetas para leer archivo

    Returns
    -------
    dc_ocurrencias : dict : diccionario con dataframes de resultados de ocurrencias

    Debugging
    ---------
    param_carpeta = 'datos/results_files_r3'

    """

    # lista de nombres de archivos en la carpeta
    abspath = path.abspath(param_carpeta)
    files = [f for f in listdir(abspath) if isfile(join(abspath, f))]
    dc_ocurrencias = dict()

    # ciclo para hacer proceso de unir informacion de todos los archivos
    for j in range(0, len(files)):

        # abrir el archivo
        with open(abspath + '/' + files[j], 'rb') as file:
            resultados = pickle.load(file)

        # dejar como llave el nombre del dataframe
        llave = list(resultados.keys())[0]
        len_res = len(resultados[llave])

        # listas para guardar resultados
        l_ocur_titulo = list()
        l_ocur_tipo1 = list()
        l_ocur_tipo2 = list()
        l_ocur_tipo3 = list()

        # verificar cantidad de ocurrencias
        for i in range(0, len_res):
            tipo_1 = resultados[llave][i]['metricas']['tipo_1']
            tipo_2 = resultados[llave][i]['metricas']['tipo_2']
            tipo_3 = resultados[llave][i]['metricas']['tipo_3']

        # guardar resultados
            if (tipo_1 + tipo_2 + tipo_3) > 0:
                l_ocur_titulo.append(list(resultados[llave][i]['datos'].keys())[0][:-20])
                l_ocur_tipo1.append(tipo_1)
                l_ocur_tipo2.append(tipo_2)
                l_ocur_tipo3.append(tipo_3)

        # importar data frame de calendario economico original
        from datos import df_ce
        df_ce_ocur = f_escenario(p0_datos=df_ce)
        df_ce_ocur['ind_esc'] = [df_ce_ocur['id'][i] + '_' + df_ce_ocur['esc'][i]
                                 for i in range(0, len(df_ce_ocur['id']))]
        df_ind_esc = pd.DataFrame(df_ce_ocur.groupby('ind_esc')['esc'].count())
        df_ind_esc.reset_index(inplace=True, drop=False)

        # ocurrencias totales de indicador_escenario
        l_ocur_ind_esc = [int(df_ind_esc.loc[df_ind_esc['ind_esc'] == i, 'esc'])
                          for i in l_ocur_titulo]

        # ocurrencias totales de indicador
        df_esc_totales = pd.DataFrame(df_ce_ocur.groupby('id')['esc'].count())
        df_esc_totales.reset_index(inplace=True, drop=False)
        l_ocur_ind = [df_esc_totales['esc'].loc[
                          np.where(df_esc_totales['id'] == l_ocur_titulo[i][:-2])[0][0]]
                      for i in range(0, len(l_ocur_titulo))]

        # actualizar diccionario con dataframes de informacion
        dc_ocurrencias['df_' +
                       files[j]] = pd.DataFrame({'id_esc': l_ocur_titulo,
                                                 'tipo_1': l_ocur_tipo1,
                                                 'tipo_2': l_ocur_tipo2,
                                                 'tipo_3': l_ocur_tipo3,
                                                 'total_ind_esc': l_ocur_ind_esc,
                                                 'total_ind': l_ocur_ind})

    return dc_ocurrencias


# -- ----------------------------------------------- Tabla general de info de indicadores -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Una tabla con todos los indicadores e informacion general para cada uno


def ce_tabla_general(param_ce, param_tip):
    """
    Parameters
    ----------
    param_ce : pd.DataFrame : con datos de calendario economico
    param_tip : pd.DataFrame : con clasificacion manual de indicadores por tipo

    Returns
    -------
    df_tb : pd.DataFrame : tabla general de indicadores

    Debugging
    ---------
    param_ce = df_ce
    param_tip = ind_tip

    """

    # datos para calculos
    df_tip = pd.DataFrame(param_tip)
    df_datos = param_ce.copy()

    # creacion de data frame final
    df_tb = pd.DataFrame({'id': list(set(df_datos['id']))})

    # columna de nombre
    df_tb['nombre'] = [df_datos['name'][np.where(df_datos['id'] ==
                                                 df_tb['id'].loc[i])[0][0]]
                       for i in range(0, len(df_tb['id']))]

    # columna de tipo
    df_tb['categoria'] = [df_tip['categoria'][np.where(df_tip['nombre'] ==
                                                       df_tb['nombre'].loc[i])[0][0]]
                          for i in range(0, len(df_tb['nombre']))]

    # columna de pais o economia de la que es el indicador
    df_tb['pais'] = [df_datos['currency'][np.where(df_datos['id'] == df_tb['id'].loc[i])[0][0]]
                     for i in range(0, len(df_tb['id']))]

    # columna de ocurrencias totales de cada indicador
    df_tb.sort_values('nombre', ascending=True, inplace=True)
    df_tb['ocurrencias'] = list(df_datos.groupby('id').count()['name'])

    # categorizacion empirica de indicador segun cantidad de observaciones
    l_categ = list()
    for r in range(0, len(df_tb['id'])):
        if 0 < df_tb['ocurrencias'].iloc[r] <= 60:
            l_categ.append('trimestral')
        elif 60 < df_tb['ocurrencias'].iloc[r] <= 125:
            l_categ.append('mensual')
        elif 125 < df_tb['ocurrencias'].iloc[r] <= 920:
            l_categ.append('semanal')

    # asignar categoria
    df_tb['frecuencia'] = l_categ

    return df_tb


# -- ------------------------------------------------------------- Tabla general compacta -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- tabla general version comparta

def f_tabla_general(param_tabla_1):
    """
    Parameters
    ----------
    param_tabla_1: pd.DataFrame : tabla de entrada

    Returns
    -------
    tabla_4: pd.DataFrame : tabla de salida

    Debugging
    ---------
    param_tabla_1 = tabla_1


    """
    tabla_4 = pd.DataFrame({
        'USA': param_tabla_1[param_tabla_1['pais'] ==
                             'USA'].groupby('categoria')['id'].count(),
        'MEX': param_tabla_1[param_tabla_1['pais'] ==
                             'MEX'].groupby('categoria')['id'].count()})

    tabla_4['USA'][np.isnan(tabla_4['USA'])] = 0
    tabla_4['MEX'][np.isnan(tabla_4['MEX'])] = 0

    tabla_4.reset_index(inplace=True, drop=False)
    tabla_4 = tabla_4.rename(columns={"index": "categoria indicador"})

    return tabla_4


# -- --------------------------------------------------------- Tabla para grafica aluvial -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- tabla para grafica aluvial

def f_tabla_aluvial(param_tabla_1, param_tabla_2):
    """
    Parameters
    ----------
    param_tabla_1 : pd.DataFrame : tabla 1 anteriormente calculada
    param_tabla_2 : pd.DataFrame : tabla 2 anteriormente calculada

    Returns
    -------
    df_aluvial : pd.DataFrame : tabla 3 para visualizaciones

    Debugging
    ---------
    param_tabla_1 = tabla_1
    param_tabla_2 = tabla_2

    """
    frames = [param_tabla_1, param_tabla_2]
    prueba = pd.concat(frames)

    # reordenar tablas de acuerdo a los valores de id y id_esc
    param_tabla_1.sort_values('id', ascending=True, inplace=True)
    param_tabla_2.sort_values('id_esc', ascending=True, inplace=True)

    # agregar columna de id para mayor facilidad de calculos posteriores a tabla 2
    param_tabla_2['id'] = [param_tabla_2['id_esc'].iloc[i][0:-2]
                           for i in range(0, len(param_tabla_2['id_esc']))]

    # tuvieron por lo menos 1 ocurrencia de patron encontrado tipo 1
    tipo_1 = list(param_tabla_2[param_tabla_2['tipo_1'] != 0].groupby('id').count().index)

    # tuvieron por lo menos 1 ocurrencia de patron encontrado tipo 2
    tipo_2 = list(param_tabla_2[param_tabla_2['tipo_2'] != 0].groupby('id').count().index)

    # tuvieron por lo menos 1 ocurrencia de patron encontrado tipo 3
    tipo_3 = list(param_tabla_2[param_tabla_2['tipo_3'] != 0].groupby('id').count().index)

    # listas de control
    l_tipo_1 = list()
    l_tipo_2 = list()
    l_tipo_3 = list()

    # ciclo para llenar listas de control
    for i in range(0, len(param_tabla_2['id'])):
        if param_tabla_2['id'].iloc[i] in tipo_1:
            l_tipo_1.append(1)
        else:
            l_tipo_1.append(0)

    for i in range(0, len(param_tabla_2['id'])):
        if param_tabla_2['id'].iloc[i] in tipo_2:
            l_tipo_2.append(1)
        else:
            l_tipo_2.append(0)

    for i in range(0, len(param_tabla_2['id'])):
        if param_tabla_2['id'].iloc[i] in tipo_3:
            l_tipo_3.append(1)
        else:
            l_tipo_3.append(0)

    # conjunto de indicadores que tuvieron al menos alguno de los 3 tipos
    tipos = set(tipo_1 + tipo_2 + tipo_3)

    # dataframe de salida con solo los indicadores que tuvieron al menos 1 tipo
    df_aluvial = param_tabla_1.loc[param_tabla_1['id'].isin(tipos)]
    df_aluvial.reset_index(inplace=True, drop=True)

    # creacion de nuevas columnas para indicar con 1 si hubo ese tipo y 0 si no lo hubo

    # al menos 1 de los escenarios del indicador tuvo patron del tipo 1
    df_aluvial['tipo_1'] = [1 if df_aluvial['id'].iloc[i] in tipo_1 else 0
                               for i in range(0, len(df_aluvial['id']))]

    # al menos 1 de los escenarios del indicador tuvo patron del tipo 2
    df_aluvial['tipo_2'] = [1 if df_aluvial['id'].iloc[i] in tipo_2 else 0
                               for i in range(0, len(df_aluvial['id']))]

    # al menos 1 de los escenarios del indicador tuvo patron del tipo 3
    df_aluvial['tipo_3'] = [1 if df_aluvial['id'].iloc[i] in tipo_3 else 0
                               for i in range(0, len(df_aluvial['id']))]

    # por la forma que se buscan, todos tuvieron patrones del tipo 4
    df_aluvial['tipo_4'] = [1]*len(df_aluvial['id'])

    # reordenar por id
    df_aluvial.sort_values('id', inplace=True)

    # agregar renglones de indicadores que no tuvieron patrones encontrados
    si_hay = list(df_aluvial['id'])
    todos = list(param_tabla_1['id'])
    no_hay = np.setdiff1d(todos, si_hay).tolist()

    df_nohay = param_tabla_1.iloc[[int(np.where(param_tabla_1['id'] == i)[0])
                                    for i in no_hay]]

    frames = [df_aluvial, df_nohay]
    df_aluvial = pd.concat(frames, axis=0, sort=True)
    df_aluvial['tipo_1'][np.isnan(df_aluvial['tipo_1'])] = 0
    df_aluvial['tipo_2'][np.isnan(df_aluvial['tipo_2'])] = 0
    df_aluvial['tipo_3'][np.isnan(df_aluvial['tipo_3'])] = 0
    df_aluvial['tipo_4'][np.isnan(df_aluvial['tipo_4'])] = 0

    return df_aluvial


# -- -------------------------------------------------------- Serializacion de resultados -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- serializar resultados para exportarse como JSON

def f_serial_result(param_objeto, param_nombre):
    """
    Parameters
    ----------
    param_objeto : dict : objeto cargado tipo dict
    param_nombre : str : nombre del archivo serializado json a escribir

    Returns
    -------

    Debugging
    ---------
    param_objeto = results
    param_nombre = 'ejemplo.json'

    """

    dato = json.dumps(param_objeto, default=pd.DataFrame.to_json)

    with open(param_nombre, 'w') as json_file:
        json.dump(dato, json_file)
