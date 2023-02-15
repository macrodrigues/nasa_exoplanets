import pandas as pd
import math
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('planets.csv')

year_options = [] # structure for the dropdown menu
for year in df['disc_year'].sort_values(ascending = True).unique():
    year_options.append({'label':str(year), 'value':year})

yaxis_options = [ # structure for the dropdown menu
    {'label':'Distance (pc)', 'value':df.columns[72]},
    {'label':'Orbital Period', 'value':df.columns[8]},
    {'label':'Orbit Semi-Major Axis', 'value':df.columns[12]},
    {'label':'Planet Radius (Earth Radius)', 'value':df.columns[16]},
    {'label':'Jupyter Radius', 'value':df.columns[20]}]

values = []
keys = []
for item in yaxis_options:
    values.append(item['label'])
    keys.append(item['value'])

dict_yaxis = dict(zip(keys, values))


app = dash.Dash()

app.layout = html.Div([
                html.Div([
                    html.Img(src='https://exoplanetarchive.ipac.caltech.edu/images/nsted_banner.jpg')]),
                html.Div([
                    dcc.Dropdown(
                        id='year-picker', 
                        options = year_options,
                        value = df['disc_year'].max())],
                    style={'width': '48%', 'display':'inline-block'}),
                html.Div([
                    dcc.Dropdown(
                        id='yaxis-picker', 
                        options = yaxis_options,
                        value = df.columns[72])],
                    style={'width': '48%', 'display':'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id = 'graph')],
                    style= {'padding':20})
                    ])

@app.callback( # decorator to define the inputs and outputs
    Output('graph', 'figure'),
    [Input('year-picker', 'value'), 
    Input('yaxis-picker', 'value')]
)

def update_figure(selected_year, selected_yaxis):
    """ This function updates the scatter plot, by taking into account the
    year and the discovery method. """

    filt_df = df[df['disc_year'] == selected_year]
    traces = [] # a list of scatter plot objects
    for method in filt_df['discoverymethod'].unique():
        df_by_method = filt_df[filt_df['discoverymethod'] == method]
        traces.append(go.Scatter(
                    x=df_by_method['pl_name'], # name of the planet
                    y=df_by_method[selected_yaxis], # method range
                    marker=dict(
                        size=df_by_method['pl_bmasse'].\
                            apply(lambda x: 0 if math.isnan(x) else x),
                        sizeref = 80), # define mass as marker
                    text=df_by_method['pl_bmasse'].\
                        apply(lambda x: 0 if math.isnan(x) else x),
                    mode = 'markers',
                    meta = dict_yaxis[selected_yaxis],
                    # hovertemplate shows the legend when hovering with the
                    # variables defined inside go.Scatter()
                    hovertemplate='<br>Planet: %{x}<br>%{meta}: %{y}<br>Mass: %{text}<br>',
                    name = method)) # name is title of the legend when hovering 

    return {
        'data': traces, # these are go.Scatter() objects
        'layout':go.Layout( # plot's layout
            title= f"Exoplanets discovered in {selected_year}",
            xaxis = {
                'showgrid': False,
                'title': dict(text = 'Planets'),
                'title_standoff':40,
                'nticks':30
                },
            yaxis = {
                'title': dict_yaxis[selected_yaxis], 
                'showgrid': False,
                'automargin': True,
                'rangemode':'tozero'},
            legend_title_text='Discovery Method')}

if __name__ == '__main__':
    app.run_server()