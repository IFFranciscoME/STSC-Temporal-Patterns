
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

def g_lineas(param_query, param_pattern):
    """
    Parameters
    ----------
    param_query :
    param_pattern :

    Returns
    -------

    Debugging
    ---------
    param_query = serie_q
    param_pattern = serie_p

    """
    serie_x = list(np.arange(len(param_query)))

    # Create traces
    fig = go.Figure()

    fig.update_layout(margin=go.layout.Margin(l=50, r=50, b=20, t=50, pad=0),
                      title=dict(x=0.5, y=1, text='Patron encontrado'),
                      xaxis=dict(title_text='fechas', rangeslider=dict(visible=False)),
                      yaxis=dict(title_text='precios (co)'))

    fig.add_trace(go.Scatter(x=serie_x, y=param_query, mode='lines', name='serie_query'))
    fig.add_trace(go.Scatter(x=serie_x, y=param_pattern, mode='lines', name='serie_pattern'))

    fig.update_layout(legend_orientation="h")

    fig.layout.autosize = False
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
