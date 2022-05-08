import pandas as pd
import math
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('planets.csv')

year_options = []
for year in df['disc_year'].sort_values(ascending = True).unique():
    year_options.append({'label':str(year), 'value':year})

yaxis_options = [
    {'label':'Distance (pc)', 'value':df.columns[72]},
    {'label':'Orbital Period', 'value':df.columns[8]},
    {'label':'Orbit Semi-Major Axis', 'value':df.columns[12]},
    {'label':'Planet Radius (Earth Radius)', 'value':df.columns[16]},
    {'label':'Jupyter Radius (Earth Radius)', 'value':df.columns[20]}]

values = []
keys = []
for item in yaxis_options:
    values.append(item['label'])
    keys.append(item['value'])

dict_yaxis = dict(zip(keys, values))


app = dash.Dash()

app.layout = html.Div([
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

@app.callback(
    Output('graph', 'figure'),
    [Input('year-picker', 'value'), 
    Input('yaxis-picker', 'value')]
)

def update_figure(selected_year, selected_yaxis):
    filt_df = df[df['disc_year'] == selected_year]
    header = dict_yaxis[selected_yaxis]
    traces = []
    for method in filt_df['discoverymethod'].unique():
        df_by_method = filt_df[filt_df['discoverymethod'] == method]
        traces.append(go.Scatter(
                    x=df_by_method['pl_name'],
                    y=df_by_method[selected_yaxis],
                    marker=dict(
                        size=df_by_method['pl_bmasse'].apply(lambda x: 0 if math.isnan(x) else x),
                        sizeref = 80),
                    text=df_by_method['pl_bmasse'].apply(lambda x: 0 if math.isnan(x) else x),
                    mode = 'markers',
                    meta = header,
                    hovertemplate='<br>Planet: %{x}<br>%{meta}: %{y}<br>Mass: %{text}<br>',
                    name = method))

    return {
        'data': traces, 
        'layout':go.Layout(
            title= f"Exoplanets discovered in {selected_year}",
            xaxis = {
                'showgrid': False,
                'title': dict(text = 'Planets'),
                'title_standoff':40,
                'nticks':30
                },
            yaxis = {
                'title': header, 
                'showgrid': False,
                'automargin': True,
                'rangemode':'tozero'},
            legend_title_text='Discovery Method')}

if __name__ == '__main__':
    app.run_server()