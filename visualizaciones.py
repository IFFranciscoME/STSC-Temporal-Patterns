
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: visualizaciones.py - funciones para visualizaciones en el proyecto           -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

import plotly.graph_objs as go                   # objetos de imagenes para funcion principal
import plotly.io as pio                          # renderizador para visualizar imagenes
import numpy as np                               # funciones numericas
pio.renderers.default = "browser"                # render de imagenes para correr en script


# -- --------------------------------------------------- GRÁFICA: lineas series de tiempo -- #
# -- ------------------------------------------------------------------------------------ -- #

def g_lineas(param_query, param_pattern, param_theme, param_dims):
    """
    Parameters
    ----------
    param_query : pd.series / np.array : datos a graficar
    param_pattern : pd.series / np.array : datos a graficar
    param_theme : dict : diccionario con tema de visualizaciones
    param_dims : dict : diccionario con tamanos para visualizaciones

    Returns
    -------
    fig_g_lineas : fig : resultado de visualizacion con plotly

    Debugging
    ---------
    param_pattern = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
    param_pattern = param_pattern['df_serie_p']['close']
    param_query = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
    param_query = param_query['df_serie_q']['close']
    param_theme = tema_base
    param_dims = dimensiones_base

    """

    # eje x en comun
    serie_x = list(np.arange(len(param_pattern)))
    # eje y0 de original
    p1_y0 = param_query
    # eje y1 de patron encontrado
    p1_y1 = param_pattern

    # Determinar los valores y los textos para el eje y0
    y0_ticks_n = 5
    y0_ticks_vals = np.arange(min(p1_y0), max(p1_y0), (max(p1_y0) - min(p1_y0)) / y0_ticks_n)
    y0_ticks_vals = np.append(y0_ticks_vals, max(p1_y0))
    y0_ticks_text = [str("%.4f" % i) for i in y0_ticks_vals]

    # Determinar los valores y los textos para el eje y1
    y1_ticks_n = 5
    y1_ticks_vals = np.arange(min(p1_y1), max(p1_y1), (max(p1_y1) - min(p1_y1)) / y1_ticks_n)
    y1_ticks_vals = np.append(y1_ticks_vals, max(p1_y1))
    y1_ticks_text = [str("%.4f" % i) for i in y1_ticks_vals]

    # Crear objeto figura
    fig_g_lineas = go.Figure()

    # agregar serie 0
    fig_g_lineas.add_trace(
        go.Scatter(y=p1_y0, name="Serie original",
                   line=dict(color=param_theme['color_linea_1'],
                             width=param_theme['tam_linea_2'])))

    # agregar serie 1
    fig_g_lineas.add_trace(
        go.Scatter(y=p1_y1, name="Serie patron encontrado", yaxis="y2",
                   line=dict(color=param_theme['color_linea_2'],
                             width=param_theme['tam_linea_2'], dash='dash')))

    # actualizar layout general
    fig_g_lineas.update_layout(
        xaxis=dict(tickvals=serie_x),
        yaxis=dict(tickvals=y0_ticks_vals, ticktext=y0_ticks_text, zeroline=False,
                   automargin=True,
                   tickfont=dict(color=param_theme['color_linea_1'],
                                 size=param_theme['tam_texto_ejes']),
                   showgrid=True),
        yaxis2=dict(tickvals=y1_ticks_vals, ticktext=y1_ticks_text, zeroline=False,
                    automargin=True,
                    tickfont=dict(color=param_theme['color_linea_2'],
                                  size=param_theme['tam_texto_ejes']),
                    showgrid=True,
                    overlaying="y", side="right"))

    # actualizar layout de leyenda
    fig_g_lineas.update_layout(
        legend=go.layout.Legend(x=.2, y=-.2,
                                font=dict(size=param_theme['tam_texto_leyenda'],
                                          color=param_theme['color_texto_leyenda'])),
        legend_orientation="h")

    # medidas de imagen y margenes
    fig_g_lineas.update_layout(autosize=False, width=1240, height=400, paper_bgcolor="white",
                               margin=go.layout.Margin(l=55, r=65, b=5, t=5, pad=1))

    # Creacion de titulos Y0 y Y1 como anotaciones
    fig_g_lineas.update_layout(annotations=[
        go.layout.Annotation(x=0, y=0.5, text="Serie Original", textangle=-90,
                             xref="paper", yref="paper", showarrow=False,
                             font=dict(size=param_theme['tam_texto_grafica'],
                                       color=param_theme['color_linea_1'])),
        go.layout.Annotation(x=1, y=0.5, text="Serie Patron Encontrado", textangle=-90,
                             xref="paper", yref="paper", showarrow=False,
                             font=dict(size=param_theme['tam_texto_grafica'],
                                       color=param_theme['color_linea_2']))])

    # Formato para titulo
    fig_g_lineas.update_layout(margin=go.layout.Margin(l=50, r=50, b=20, t=50, pad=20),
                               title=dict(x=0.5, text='<b> Serie Original </b> - '
                                                      '<i> Patron Encontrado </i>'),
                               legend=go.layout.Legend(x=.3, y=-.15, orientation='h',
                                                       font=dict(size=15)))
    # Formato de tamanos
    fig_g_lineas.layout.autosize = True
    fig_g_lineas.layout.width = param_dims['figura_1']['width']
    fig_g_lineas.layout.height = param_dims['figura_1']['height']
    fig_g_lineas.show()

    return fig_g_lineas


# -- ------------------------------------------------------- GRÁFICA: velas OHLC Reaccion -- #
# -- ------------------------------------------------------------------------------------ -- #

def g_velas_reac(param_timestamp, param_ohlc, param_serie1, param_serie2, param_serie3,
                 param_theme, param_dims):
    """
    Parameters
    ----------
    param_timestamp : pd.DataFrame : columnas 'timestamp'
    param_ohlc : pd.DataFrame : columnas 'open', 'high', 'low', 'close'
    param_serie1 : pd.Series / np.array : datos a graficar
    param_serie2 : pd.Series / np.array : datos a graficar
    param_serie3 : pd.Series / np.array : datos a graficar
    param_theme : dict : diccionario con tema de visualizaciones
    param_dims : dict : diccionario con tamanos para visualizaciones

    Returns
    -------
    fig_g_velas_reac : plotly : objeto/diccionario tipo plotly para graficar

    Debugging
    ---------
    param_ohlc = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
    param_ohlc = param_ohlc['df_serie_q']
    param_timestamp = param_ohlc['timestamp']
    param_serie1 = param_ohlc['close']
    param_serie2 = param_ohlc['mid_hl']
    param_serie3 = param_ohlc['mid_oc']

    param_theme = tema_base
    param_dims = dimensiones_base

    """

    # parametros para anotacion de texto en grafica
    f_i = param_timestamp[0]
    yini = param_ohlc['high'][0]
    yfin = max(param_ohlc['close'])

    # base de figura
    fig_g_velas_reac = go.Figure()

    # agregar capa de figura de velas japonesas (candlestick)
    fig_g_velas_reac.add_trace(
        go.Candlestick(name='ohlc',
                       x=param_ohlc['timestamp'],
                       open=param_ohlc['open'],
                       high=param_ohlc['high'],
                       low=param_ohlc['low'],
                       close=param_ohlc['close'],
                       opacity=0.4))

    # Agregar capa de linea extra: Close
    fig_g_velas_reac.add_trace(
        go.Scatter(x=param_timestamp, y=param_serie1, name='close',
                   line=dict(color=param_theme['color_linea_1'], width=2, dash='dash')))

    # Agregar capa de linea extra: mid hl
    fig_g_velas_reac.add_trace(
        go.Scatter(x=param_timestamp, y=param_serie2, name='mid hl',
                   line=dict(color=param_theme['color_linea_2'], width=2, dash='dash')))

    # Agregar capa de linea extra: mid oc
    fig_g_velas_reac.add_trace(
        go.Scatter(x=param_timestamp, y=param_serie3, name='mid oc',
                   line=dict(color=param_theme['color_linea_3'], width=2, dash='dash')))

    # linea vertical
    lineas = [dict(x0=f_i, x1=f_i, xref='x', y0=yini, y1=yfin, yref='y', type='line',
                   line=dict(color=param_theme['color_linea_4'], width=1.5, dash='dashdot'))]

    # layout de margen, titulos y ejes
    fig_g_velas_reac.update_layout(
        margin=go.layout.Margin(l=50, r=50, b=20, t=50, pad=20),
        title=dict(x=0.5, text='Reaccion del precio durante <b> Indicador Comunicado </b>'),
        xaxis=dict(title_text='Hora del dia', rangeslider=dict(visible=False)),
        yaxis=dict(title_text='Precio del EurUsd'), shapes=lineas)

    # Color y fuente de texto en ejes
    fig_g_velas_reac.update_layout(
        xaxis=dict(titlefont=dict(color=param_theme['color_titulo_ejes']),
                   tickfont=dict(color=param_theme['color_texto_ejes'],
                                 size=param_theme['tam_texto_ejes'])),
        yaxis=dict(zeroline=False, automargin=True,
                   titlefont=dict(color=param_theme['color_titulo_ejes']),
                   tickfont=dict(color=param_theme['color_texto_ejes'],
                                 size=param_theme['tam_texto_ejes']),
                   showgrid=True))

    # Anotaciones
    fig_g_velas_reac.update_layout(
        annotations=[go.layout.Annotation(x=f_i, y=0.95, xref="x", yref="paper",
                                          showarrow=False, text="Indicador",
                                          font=dict(size=15, color='red')),
                     go.layout.Annotation(x=f_i, y=0.90, xref="x", yref="paper",
                                          showarrow=False, text="Comunicado",
                                          font=dict(size=15, color='red'))])

    # Formato de leyenda
    fig_g_velas_reac.update_layout(
        legend=go.layout.Legend(x=.3, y=-.15, orientation='h',
                                font=dict(size=param_theme['tam_texto_leyenda'],
                                          color=param_theme['color_texto_leyenda'])))

    # Formato de tamanos
    fig_g_velas_reac.layout.autosize = True
    fig_g_velas_reac.layout.width = param_dims['figura_1']['width']
    fig_g_velas_reac.layout.height = param_dims['figura_1']['height']

    fig_g_velas_reac.show()

    return fig_g_velas_reac
