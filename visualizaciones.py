
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
