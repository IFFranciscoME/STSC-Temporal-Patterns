
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: funciones.py - funciones de procesamiento para usar en el proyecto           -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

from os import listdir
from os.path import isfile, join
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos
from datetime import timedelta

import numpy as np
import pandas as pd
import statsmodels.api as sm  # modelos estadisticos: anova
from statsmodels.formula.api import ols  # modelo lineal con ols

import multiprocessing as mp                              # procesamiento en paralelo

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
            print(f1 + ' y ' + f2)
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

def f_unir_ind(param_dir):
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

    # inicializar la columna escenario, habra los siguientes: A, B, C, D
    p0_datos['escenario'] = 'X'

    # -- -- A: actual >= previous & actual >= consensus & consensus >= previous
    p0_datos['escenario'][((p0_datos['actual'] >= p0_datos['previous']) &
                          (p0_datos['actual'] >= p0_datos['consensus']))] = 'A'

    # -- -- B: actual >= previous & actual >= consensus & consensus < Precious
    p0_datos['escenario'][((p0_datos['actual'] >= p0_datos['previous']) &
                          (p0_datos['actual'] < p0_datos['consensus']))] = 'B'

    # -- -- C: actual >= previous & actual < consensus & consensus >= previous
    p0_datos['escenario'][((p0_datos['actual'] < p0_datos['previous']) &
                          (p0_datos['actual'] >= p0_datos['consensus']))] = 'C'

    # -- -- D: actual >= previous & actual < consensus & consensus < previous
    p0_datos['escenario'][((p0_datos['actual'] < p0_datos['previous']) &
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
    p2_ph = df_usdmxn
    p3_ce = df_ce
    """

    # Debugging y control interno
    # print(p0_i)
    # print(' fecha del ce a buscar es: ' + str(p3_ce['timestamp'][p0_i]))
    mult = 10000

    # Revisión si no encuentra timestamp exacto, recorrer 1 hacia atras iterativamente
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

def f_metricas(param_ce, param_ph):
    """
    Parameters
    ----------
    param_ce : pd.DataFrame : Economic calendar with 'timestamp', 'name', 'actual',
                              'consensus', 'previous'
    param_ph : pd.DataFrame : Historical prices 'timestamp', 'open', 'high', 'low', 'close'

    Returns
    -------
    r_metricas : pd.DataFrame : para_ce + metricas

    Debugging
    ---------
    param_ce = df_ce
    param_ph = df_usdmxn
    """

    # Cantidad de precios a futuro a considerar
    psiguiente = 30
    indices_ce = list(param_ce['timestamp'].index)
    # --------------------------------------------------------- PARALELIZACION DE PROCESO -- #

    # Reaccion del precio para cada escenario (PARALELO)
    # inicializar el pool con el maximo de procesadores disponibles
    pool = mp.Pool(mp.cpu_count())
    d_reaccion = pool.starmap(f_reaccion, [(i, psiguiente, param_ph, param_ce)
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

def f_tabla_ind(param_ce):
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
    l_a = [sum(list(param_ce['escenario'][param_ce['name'] == inds[i]] == 'A'))
           for i in range(0, len(inds))]

    # Ocurrencias de escenario B en cada indicador
    l_b = [sum(list(param_ce['escenario'][param_ce['name'] == inds[i]] == 'B'))
           for i in range(0, len(inds))]

    # Ocurrencias de escenario C en cada indicador
    l_c = [sum(list(param_ce['escenario'][param_ce['name'] == inds[i]] == 'C'))
           for i in range(0, len(inds))]

    # Ocurrencias de escenario D en cada indicador
    l_d = [sum(list(param_ce['escenario'][param_ce['name'] == inds[i]] == 'D'))
           for i in range(0, len(inds))]

    # Ocurrencias total de cada indicador
    l_t = [len(param_ce['escenario'][param_ce['name'] == inds[i]]) for i in range(0, len(inds))]

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
    df_anova = pd.DataFrame({'ind': tab_ind, 'esc': tab_esc, 'obs': tab_obs, 'grp': tab_grp,
                             'anova_hl': [0] * len(tab_ind),
                             'anova_ol': [0] * len(tab_ind),
                             'anova_ho': [0] * len(tab_ind),
                             'anova_co': [0] * len(tab_ind)})

    # -- eligir aleatoriamente la misma cantidad de observaciones para 3 grupos distintos
    # elegir N observaciones, aleatoriamente con dist uniforme sin reemplazo, del total
    # de observaciones del indicador IM.

    for i in range(0, len(df_anova['ind'])):

        n_ale_1 = df_anova.iloc[i, 3]
        n_ale_2 = n_ale_1
        n_ale_3 = df_anova.iloc[i, 2] - n_ale_1 - n_ale_2

        im = df_anova['ind'][i]
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
