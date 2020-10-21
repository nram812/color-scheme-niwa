import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask
import dash
import os

import xarray as xr
import pandas as pd
import dash
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

import numpy as np
from pathlib import Path
import xarray as xr
import sys
import seaborn as sn
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
import os
os.chdir(r'C:\Users\rampaln\OneDrive - NIWA\Research Projects\CAOA2101\color-scheme\color-scheme-niwa')

df = xr.open_dataset(r'dataset\TestColorScaleDset.nc')
df_geo = xr.open_dataset(r'dataset\Geopotential.nc')
print(df.data_vars, df_geo.data_vars)
#observations = df['CMG 0.05 Deg Monthly NDVI']

server = flask.Flask(__name__)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, server = server)
#app.config.suppress_callback_exceptions = True
#,
variables = ['Mean_temp','Rad','Rain','SoilM','hgt']

#     html.Div(
#         id='Username',
#         style={'textAlign': 'center',
#                'verticalAlign': 'middle',
#
# Made some minor modificatoins so that the program works




app.layout = html.Div(style={'backgroundColor': colors['background'],'body':0},
    children=[
       html.Div(
                 children=[
                    html.Div(className='six columns',
                             children=[
                                 html.H2('MODIS Enhanced Vegetation Index (EVI) Explorer',style={'color': 'k'}),
                                 dcc.Interval(interval=500),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(
                                             id='datetimemonth-dropdown',
                                             options=[{'label': k, 'value': k} for k in variables],
                                             value=variables[0],
                                             placeholder="Select Variable",
                                             style=dict(width='40%',
                                                 display='inline-block',
                                                 verticalAlign="middle")),
                                        dcc.Interval(interval=500),
                                        dcc.Slider(id ="hue1",min=0, #the first date # time slider
                                                       max=365, #the last date
                                                       value=20,
                                                   tooltip={'always_visible': True}),
                                         dcc.Slider(id="hue2", min=0,  # the first date # zoom slider
                                                    max=365,  # the last date
                                                    value=290,
                                                    tooltip={'always_visible': True}),
                                        dcc.Slider(id="saturation", min=0,  # the first date # zoom slider
                                                    max=365,  # the last date
                                                    value=290,
                                                    tooltip={'always_visible': True}),
                                        dcc.Slider(id="lightness", min=0,  # the first date # zoom slider
                                                    max=365,  # the last date
                                                    value=290,
                                                    tooltip={'always_visible': True}),
                                                    
                                         dcc.Graph(id='funnel-graph'),
                                         dcc.Interval(interval=1000),
                                     ],
                                     style={'color': 'k'})
                                        ]       
                             )],
                 )]
                              )



@app.callback(dash.dependencies.Output('funnel-graph', 'figure'),
              [dash.dependencies.Input('datetimemonth-dropdown', 'value'),
               dash.dependencies.Input("hue1", "value"),
               dash.dependencies.Input("hue2", "value"),
               dash.dependencies.Input("saturation", "value"),
               dash.dependencies.Input("lightness", "value")])
def update_graph(variable, hue1, hue2, saturation, lightness):
    if variable == 'hgt':
        dataset = df_geo
    else:
        dataset = df

    cmap = sn.diverging_palette(hue1, hue2,saturation,lightness, as_cmap=True)
    vals = dataset[variable].isel(time =0).values
    print(vals.shape)
    lats = dataset[variable].lat.values
    lons = dataset[variable].lon.values
    lats, lons = np.meshgrid(lats, lons)
    lats = lats.T
    lons = lons.T
    idx = vals > -100.0
    colors = [[0,f'rgb({hue1},0,0)'], [0,f'rgb({hue2},0,0)'], [0,'rgb(155,0,0)'], [0,'rgb(205,0,0)'], [0,'rgb(25,0,0)']]
    print(colors)
    lats2 = lats[idx].ravel()
    lons2 = lons[idx].ravel()
    vals2 = vals[idx].ravel()
    trace1 = go.Scattermapbox(lat=lats2,
                              lon=lons2,
                              mode='markers+text',
                              marker=dict(size=7, showscale=True, colorscale =colors),
                              textposition='top right',
                              hovertext=[f"{variable} %.2f" % i for i in vals2])
    mapbox = dict(
        center=dict(
            lat=-41,
            lon=175
        ),
        pitch=0,
        zoom=3,
        style= "carto-positron")

    # trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    # trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
    # trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

    return {
        'data': [trace1],
        'layout':
            go.Layout(autosize=True, hovermode='closest',
                      barmode='stack', mapbox=mapbox, height=750, width=800,template= 'seaborn', font=dict(
                family="Courier New, monospace",
                size=10,
            ))
    }

#
# @app.callback(dash.dependencies.Output('funnel-graph', 'children'),
#               [dash.dependencies.Input('funnel-graph', 'clickData')])
# def update_graph2(foo_click_data):
#     print(foo_click_data)
#     return foo_click_data['points'][0]['lat'], foo_click_data['points'][0]['lon']




if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1', port = '8888')


