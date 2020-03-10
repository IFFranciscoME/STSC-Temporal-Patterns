
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

def g_lineas(p_datos1, p_datos2):
    """
    :param p_datos1
    :param p_datos2

    :return:
    """

    n = len(p_datos1)
    random_x = list(np.arange(n))
    random_y0 = p_datos1
    random_y1 = p_datos2

    # Create traces
    fig = go.Figure()

    fig.update_layout(margin=go.layout.Margin(l=50, r=50, b=20, t=50, pad=0),
                      title=dict(x=0.5, y=1, text='Patron encontrado'),
                      xaxis=dict(title_text='fechas', rangeslider=dict(visible=False)),
                      yaxis=dict(title_text='precios (co)'))

    fig.add_trace(go.Scatter(x=random_x, y=random_y0, mode='lines', name='serie_query'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y1, mode='lines', name='serie'))

    fig.update_layout(legend_orientation="h")

    fig.layout.autosize = False
    fig.layout.width = 840
    fig.layout.height = 520

    return fig
