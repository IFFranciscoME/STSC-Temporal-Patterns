
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

def g_lineas(param_query, param_pattern, param_theme, param_dim):
    """
    Parameters
    ----------
    param_query :
    param_pattern :
    param_theme :
    param_dim :

    Returns
    -------
    fig :

    Debugging
    ---------
    param_pattern = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
    param_pattern = param_pattern['df_serie_p']
    param_query = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
    param_query = param_query['df_serie_q']

    param_theme = tema_base
    param_dim = dimensiones_base

    """

    pt_temp = dict(eje_x_tick_col='blue', eje_x_tick_tam=12,
                   eje_x_titulo_col='blue', eje_x_titulo_tam=12,

                   eje_y0_tick_col='red', eje_y0_tick_tam=12,
                   eje_y0_titulo_col='red', eje_y0_titulo_tam=12,

                   eje_y1_tick_col='blue', eje_y1_tick_tam=12,
                   eje_y1_titulo_col='blue', eje_y1_titulo_tam=12,

                   legend_col='grey', legend_tam=16)

    serie_x = list(np.arange(len(param_pattern['close'])))
    p1_y1 = param_pattern['close']
    p2_y2 = param_query['close']

    # Determinar los valores y los textos para el eje y1
    y1_ticks_n = 5
    y1_ticks_vals = np.arange(min(p1_y1), max(p1_y1), (max(p1_y1) - min(p1_y1)) / y1_ticks_n)
    y1_ticks_vals = np.append(y1_ticks_vals, max(p1_y1))
    y1_ticks_text = [str("%.4f" % i) for i in y1_ticks_vals]

    # Determinar los valores y los textos para el eje y2
    y2_ticks_n = 5
    y2_ticks_vals = np.arange(min(p2_y2), max(p2_y2), (max(p2_y2) - min(p2_y2)) / y2_ticks_n)
    y2_ticks_vals = np.append(y2_ticks_vals, max(p2_y2))
    y2_ticks_text = [str("%.4f" % i) for i in y2_ticks_vals]

    # serie_p = param_pattern['close']/max(param_pattern['close'])
    # serie_q = param_query['close']/max(param_query['close'])

    # Crear objeto figura
    fig = go.Figure()

    # agregar serie 1
    fig.add_trace(
        go.Scatter(y=p1_y1, name="Serie patron encontrado"))

    # agregar serie 2
    fig.add_trace(
        go.Scatter(y=p2_y2, name="Serie original", yaxis="y2"))

    # actualizar layout general
    fig.update_layout(
        xaxis=dict(tickvals=serie_x),
        yaxis=dict(tickvals=y1_ticks_vals, ticktext=y1_ticks_text, zeroline=False,
                   automargin=True,
                   tickfont=dict(color=pt_temp['eje_y0_tick_col'],
                                 size=pt_temp['eje_y0_tick_tam']),
                   showgrid=True),
        yaxis2=dict(tickvals=y2_ticks_vals, ticktext=y2_ticks_text, zeroline=False,
                    automargin=True,
                    tickfont=dict(color=pt_temp['eje_y1_tick_col'],
                                  size=pt_temp['eje_y1_tick_tam']),
                    showgrid=True,
                    overlaying="y", side="right"))

    # actualizar layout de leyenda
    fig.update_layout(
        legend=go.layout.Legend(x=.2, y=-.2, font=dict(size=pt_temp['legend_tam'],
                                                       color=pt_temp['legend_col'])),
        legend_orientation="h")

    # medidas de imagen y margenes
    fig.update_layout(autosize=False, width=1240, height=400, paper_bgcolor="white",
                      margin=go.layout.Margin(l=55, r=65, b=5, t=5, pad=1))

    # Creacion de titulos Y0 y Y1 como anotaciones
    fig.update_layout(annotations=[
        go.layout.Annotation(x=0, y=0.25, text="Serie Original", textangle=-90,
                             xref="paper", yref="paper", showarrow=False,
                             font=dict(size=pt_temp['eje_y0_titulo_tam'],
                                       color=pt_temp['eje_y0_titulo_col'])),
        go.layout.Annotation(x=1, y=0.25, text="Serie Patron Encontrado", textangle=-90,
                             xref="paper", yref="paper", showarrow=False,
                             font=dict(size=pt_temp['eje_y1_titulo_tam'],
                                       color=pt_temp['eje_y1_titulo_col']))])

    fig.update_layout(margin=go.layout.Margin(l=50, r=50, b=20, t=50, pad=20),
                      title=dict(x=0.5, text='Serie Original - <b> Patron Encontrado </b>'),
                      legend=go.layout.Legend(x=.3, y=-.15, orientation='h',
                                              font=dict(size=15)))
    fig.layout.autosize = True
    fig.layout.width = 840
    fig.layout.height = 520
    fig.show()

    return fig


# -- ------------------------------------------------------- GRÁFICA: velas OHLC Reaccion -- #
# -- ------------------------------------------------------------------------------------ -- #

def g_velas_reaccion(param_timestamp, param_ohlc, param_serie1, param_serie2, param_serie3):
    """
    Parameters
    ----------
    param_timestamp
    param_ohlc
    param_serie1
    param_serie2
    param_serie3

    Returns
    -------

    Debugging
    ---------
    param_ohlc = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
    param_ohlc = param_ohlc['df_serie_q']
    param_timestamp = param_ohlc['timestamp']
    param_serie1 = param_ohlc['close']
    param_serie2 = param_ohlc['mid_hl']
    param_serie3 = param_ohlc['mid_oc']
    """

    f_i = param_timestamp[0]
    yini = param_ohlc['high'][0]
    yfin = max(param_ohlc['close'])
    fig = go.Figure(data=[go.Candlestick(name='ohlc', x=param_ohlc['timestamp'],
                                         open=param_ohlc['open'], high=param_ohlc['high'],
                                         low=param_ohlc['low'], close=param_ohlc['close'],
                                         opacity=0.4)])

    fig.add_trace(go.Scatter(x=param_timestamp, y=param_serie1, name='close',
                             line=dict(color='blue', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=param_timestamp, y=param_serie2, name='mid hl',
                             line=dict(color='red', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=param_timestamp, y=param_serie3, name='mid oc',
                             line=dict(color='green', width=2, dash='dash')))

    lineas = [dict(x0=f_i, x1=f_i, xref='x', y0=yini, y1=yfin, yref='y', type='line',
                   line=dict(color='red', width=1.5, dash='dashdot'))]

    fig.update_layout(margin=go.layout.Margin(l=50, r=50, b=20, t=50, pad=20),
                      title=dict(x=0.5, text='Reaccion del precio durante '
                                             'comunicado de <b> indicador </b>'),
                      xaxis=dict(title_text='Hora del dia', rangeslider=dict(visible=False)),
                      yaxis=dict(title_text='Precio del EurUsd'), shapes=lineas,
                      annotations=[go.layout.Annotation(x=f_i, y=0.95, xref="x", yref="paper",
                                                        showarrow=False, text="Indicador",
                                                        font=dict(size=15)),
                                   go.layout.Annotation(x=f_i, y=0.90, xref="x", yref="paper",
                                                        showarrow=False, text="Comunicado",
                                                        font=dict(size=15))])

    # fig.update_layout(legend_orientation="h")
    fig.update_layout(legend=go.layout.Legend(x=.3, y=-.15, orientation='h',
                                              font=dict(size=15)))
    fig.layout.autosize = False
    fig.layout.width = 840
    fig.layout.height = 520
    fig.show()

    return fig
