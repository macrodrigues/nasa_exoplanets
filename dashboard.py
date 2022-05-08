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

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
        id='year-picker', 
        options = year_options,
        value = df['disc_year'].max()),
    dcc.Graph(id = 'graph')
])

@app.callback(
    Output('graph', 'figure'),
    [Input('year-picker', 'value')]
)

def update_figure(selected_year):
    filtered_df = df[df['disc_year'] == selected_year]
    traces = []
    for method in filtered_df['discoverymethod'].unique():
        df_by_method = filtered_df[filtered_df['discoverymethod'] == method]
        traces.append(go.Scatter(
                    x=df_by_method['pl_name'],
                    y=df_by_method['sy_dist'],
                    marker=dict(
                        size=df_by_method['pl_bmasse'].apply(lambda x: 0 if math.isnan(x) else x),
                        sizeref = 80),
                    text=df_by_method['pl_bmasse'].apply(lambda x: 0 if math.isnan(x) else x),
                    mode = 'markers',
                    hovertemplate='<br>Planet: %{x}<br>Distance: %{y}<br>Mass: %{text}<br>',
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
                'title': 'Distance (pc)', 
                'showgrid': False,
                'automargin': True,
                'rangemode':'tozero'},
            legend_title_text='Discovery Method')}

if __name__ == '__main__':
    app.run_server()