
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: funciones.py - funciones de procesamiento para usar en el proyecto           -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd                                       # dataframes y utilidades
import numpy as np                                        # arrays y operaciones numericas
from os import listdir, path
from os.path import isfile, join
from datetime import timedelta                            # diferencia entre datos tipo tiempo
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos

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
    param_dir = path.abspath('datos/files/')

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

    # Elegir columnas para data frame final (no se incluye revised)
    df_ce = df_ce[['DateTime', 'Name', 'Currency', 'Actual', 'Consensus', 'Previous']]

    return df_ce


df_ce_g = f_unir_ind(param_dir=path.abspath('datos/econ_files/'))
