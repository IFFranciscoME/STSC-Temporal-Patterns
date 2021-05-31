
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Subsequential Time Series Clustering: Evidence of Temporal Patterns in UsdMxn Exchange Rate         -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Description: Code repositories (Python, R and LaTeX for research poster                             -- #
# -- Script: visualizations.py : python script with data visualization functions                         -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- Repository: https://github.com/IFFranciscoME/STSC-Temporal-Patterns                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #

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
    param_pattern = pattern_g2
    param_query = results['ciclo_3'][0]['datos']['ConsumrgyMoM_USA_A_2015-12-15_13:30:00']
    param_query = query_g2
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
    y0_ticks_text = [str("%.2f" % i) for i in y0_ticks_vals]

    # Determinar los valores y los textos para el eje y1
    y1_ticks_n = 5
    y1_ticks_vals = np.arange(min(p1_y1), max(p1_y1), (max(p1_y1) - min(p1_y1)) / y1_ticks_n)
    y1_ticks_vals = np.append(y1_ticks_vals, max(p1_y1))
    y1_ticks_text = [str("%.2f" % i) for i in y1_ticks_vals]

    # Crear objeto figura
    fig_g_lineas = go.Figure()

    # agregar serie 0
    fig_g_lineas.add_trace(
        go.Scatter(y=p1_y0, name="original",
                   line=dict(color=param_theme['color_linea_1'],
                             width=param_theme['tam_linea_2'])))

    # agregar serie 1
    fig_g_lineas.add_trace(
        go.Scatter(y=p1_y1, name="patron", yaxis="y2",
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

    # Anotaciones en la grafica (una para cada serie)
    # fig_g_lineas.update_layout(annotations=[
    #     go.layout.Annotation(x=0, y=0.35, text="Serie Original", textangle=-90,
    #                          xref="paper", yref="paper", showarrow=False,
    #                          font=dict(size=param_theme['tam_texto_grafica'],
    #                                    color=param_theme['color_linea_1'])),
    #     go.layout.Annotation(x=1, y=0.35, text="Serie Patron Encontrado", textangle=-90,
    #                          xref="paper", yref="paper", showarrow=False,
    #                          font=dict(size=param_theme['tam_texto_grafica'],
    #                                    color=param_theme['color_linea_2']))])

    # Formato para titulo
    fig_g_lineas.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=0),
                               title=None,
                               legend=go.layout.Legend(x=.8, y=.17, orientation='h',
                                                       bordercolor=param_theme['color_texto_leyenda'],
                                                       borderwidth=1,
                                                       font=dict(size=12)))

    # Formato de tamanos
    fig_g_lineas.layout.autosize = True
    fig_g_lineas.layout.width = param_dims['figura_1']['width']
    fig_g_lineas.layout.height = param_dims['figura_1']['height']

    return fig_g_lineas


# -- ------------------------------------------------------- GRÁFICA: velas OHLC Reaccion -- #
# -- ------------------------------------------------------------------------------------ -- #

def g_velas_reac(param_timestamp, param_ohlc, param_serie1, param_serie2, param_theme, param_dims):
    """
    Parameters
    ----------
    param_timestamp : pd.DataFrame : columnas 'timestamp'
    param_ohlc : pd.DataFrame : columnas 'open', 'high', 'low', 'close'
    param_serie1 : pd.Series / np.array : datos a graficar
    param_serie2 : pd.Series / np.array : datos a graficar
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
    param_serie1 = param_ohlc['mid_hl']
    param_serie2 = param_ohlc['mid_oc']

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
            go.Candlestick(name='OHLC',
                           x=param_ohlc['timestamp'],
                           open=round(param_ohlc['open'], 4),
                           high=round(param_ohlc['high'], 4),
                           low=round(param_ohlc['low'], 4),
                           close=round(param_ohlc['close'], 4),
                           increasing_line_color='gray', decreasing_line_color='gray',
                           opacity=0.4))

    # Agregar capa de linea extra: mid hl
    fig_g_velas_reac.add_trace(
        go.Scatter(x=param_timestamp, y=param_serie1, name='CO',
                   line=dict(color=param_theme['color_linea_1'], width=2, dash='dash')))

    # Agregar capa de linea extra: mid oc
    fig_g_velas_reac.add_trace(
        go.Scatter(x=param_timestamp, y=param_serie2, name='HL',
                   line=dict(color=param_theme['color_linea_3'], width=2, dash='dash')))

    # linea vertical
    lineas = [dict(x0=f_i, x1=f_i, xref='x', y0=yini, y1=yfin, yref='y', type='line',
                   line=dict(color=param_theme['color_linea_4'], width=1.5, dash='dashdot'))]

    # layout de margen, titulos y ejes
    fig_g_velas_reac.update_layout(
        margin=go.layout.Margin(l=1, r=1, b=1, t=0, pad=0),
        title=None,
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
                                          showarrow=False, text="Indicador Comunicado",
                                          font=dict(size=15, color='red'))])

    # Formato de leyenda
    fig_g_velas_reac.update_layout(
        legend=go.layout.Legend(x=.76, y=.17, orientation='h',
                                bordercolor=param_theme['color_texto_leyenda'], borderwidth=1,
                                font=dict(size=param_theme['tam_texto_leyenda'],
                                          color=param_theme['color_texto_leyenda'])))

    # Formato de tamanos
    fig_g_velas_reac.layout.autosize = True
    fig_g_velas_reac.layout.width = param_dims['figura_2']['width']
    fig_g_velas_reac.layout.height = param_dims['figura_2']['height']

    return fig_g_velas_reac


# -- -------------------------------------------------------- GRÁFICA: aluvial categorica -- #
# -- ------------------------------------------------------------------------------------ -- #

def g_aluvial_cat(param_data, param_theme, param_dims):
    """
    Parameters
    ----------
    param_data : pd.DataFrame : data frame con tabla a graficar (tabla 3)
    param_theme : dict : diccionario con tema de visualizaciones
    param_dims : dict : diccionario con tamanos para visualizaciones

    Returns
    -------
    fig_g_aluvial_cat : plotly : objeto/diccionario tipo plotly para graficar

    Debugging
    ---------
    param_data = tabla_3
    param_theme = tema_base
    param_dims = dimensiones_base

    """

    # generacion de dimension: categoria
    categoria_dim = go.parcats.Dimension(
        values=param_data['categoria'],
        label='categoria')

    # generacion de dimension: pais
    pais_dim = go.parcats.Dimension(
        values=param_data['pais'],
        label='pais')

    # generacion de dimension: frecuencia de ocurrencia
    frecuencia_dim = go.parcats.Dimension(
        values=param_data['frecuencia'],
        label='frecuencia')

    # generacion de dimension: presencia de patrones tipo 1
    tipo_1_dim = go.parcats.Dimension(
        values=param_data['tipo_1'],
        label="tipo_1",
        categoryarray=[0, 1],
        ticktext=['sin patron', 'con patron'])

    # generacion de dimension: presencia de patrones tipo 2
    tipo_2_dim = go.parcats.Dimension(
        values=param_data['tipo_2'],
        label="tipo_2",
        categoryarray=[0, 1],
        ticktext=['sin patron', 'con patron'])

    # generacion de dimension: presencia de patrones tipo 3
    tipo_3_dim = go.parcats.Dimension(
        values=param_data['tipo_3'],
        label="tipo_3",
        categoryarray=[0, 1],
        ticktext=['sin patron', 'con patron'])

    # vector de colores para todas las lineas
    colores = [param_theme['color_linea_9'], param_theme['color_linea_2'],
               param_theme['color_linea_3'], param_theme['color_linea_4'],
               param_theme['color_linea_5'], param_theme['color_linea_6'],
               param_theme['color_linea_7'], param_theme['color_linea_8'],
               param_theme['color_linea_1']]

    # crear columna de color en los datos de entrada
    param_data['color'] = ['#ABABAB']*len(param_data['id'])

    for i in range(0, len(param_data['categoria'])):
        if param_data['categoria'].iloc[i] == 'Tasas de interes':
            param_data['color'].iloc[i] = colores[0]
        elif param_data['categoria'].iloc[i] == 'actividad economica':
            param_data['color'].iloc[i] = colores[3]
        elif param_data['categoria'].iloc[i] == 'consumo':
            param_data['color'].iloc[i] = colores[8]
        elif param_data['categoria'].iloc[i] == 'energia':
            param_data['color'].iloc[i] = colores[6]
        elif param_data['categoria'].iloc[i] == 'flujos de capital':
            param_data['color'].iloc[i] = colores[4]
        elif param_data['categoria'].iloc[i] == 'inflacion':
            param_data['color'].iloc[i] = colores[5]
        elif param_data['categoria'].iloc[i] == 'mercado inmobiliario':
            param_data['color'].iloc[i] = colores[1]
        elif param_data['categoria'].iloc[i] == 'mercado laboral':
            param_data['color'].iloc[i] = colores[7]
        elif param_data['categoria'].iloc[i] == 'subasta de bonos':
            param_data['color'].iloc[i] = colores[2]

    color = param_data['color'].tolist()

    # generacion del objeto figura
    fig_g_aluvial_cat = go.Figure()

    # agregar trazo de grafica tipo aluvial (parallel categories)
    fig_g_aluvial_cat.add_trace(go.Parcats(
        dimensions=[categoria_dim, frecuencia_dim, pais_dim,
                    tipo_1_dim, tipo_2_dim, tipo_3_dim],
        line={'color': color},
        hoveron='color', hoverinfo='count+probability',
        labelfont={'size': 14, 'family': 'Times',
                   'color': param_theme['color_texto_ejes']},
        tickfont={'size': 14, 'family': 'Times',
                  'color': param_theme['color_texto_ejes']},
        arrangement='perpendicular'))

    # layout de margen, titulos y ejes
    fig_g_aluvial_cat.update_layout(
        margin=go.layout.Margin(l=100, r=25, b=5, t=25, pad=10),
        title=None)

    # Formato de tamanos
    fig_g_aluvial_cat.layout.autosize = True
    fig_g_aluvial_cat.layout.width = param_dims['figura_3']['width']
    fig_g_aluvial_cat.layout.height = param_dims['figura_3']['height']

    return fig_g_aluvial_cat
