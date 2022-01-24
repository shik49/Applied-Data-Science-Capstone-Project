"""
Building a Dashboard Application with Plotly Dash
We will be building a Plotly Dash application for users to perform interactive visual analytics on SpaceX launch data in real-time.

TASK 1: Add a Launch Site Drop-down Input Component
TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
TASK 3: Add a Range Slider to Select Payload
TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
"""

# importing required libraries
from multiprocessing.sharedctypes import Value
from tkinter.font import names
import pandas as pd
import dash
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np

app = dash.Dash(__name__)

spacex_df = pd.read_csv('spacex_launch_dash.csv')
sites = spacex_df['Launch Site'].unique()
sites = np.insert(sites, 0, 'All Sites')
print(sites)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard', 
                                        style={'text-align':'center', 'color':'#503D36', 'font-size': 40}),
                      dcc.Dropdown(id='site-dropdown', 
                                   options=[
                                           {'label': site, 'value': site} for site in sites
                                           ],
                                   value='All Sites',
                                   placeholder="Select a launch site",
                                   searchable=True,
                                   style={'padding':'3px', 'font-size':'20px',
                                          'text-align-last': 'center'}),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload Range (Kg)"),
                                html.Div(dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                        marks={0: '0', 2500: '2500', 7500:'7500', 10000:'10000'},
                                                        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
                                                        )),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))         
                        ]
                     )

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))

def success_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    filtered_df = filtered_df.groupby(['class'])['Launch Site'].count().reset_index()
    if entered_site == 'All Sites':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Success Rates of Launch Sites')
    else:
        fig = px.pie(filtered_df, values='Launch Site', names='class', title=f'Success Rates of Launch Site {entered_site}')
    return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                 [Input(component_id='site-dropdown', component_property='value'), 
                 Input(component_id='payload-slider', component_property='value')])

def success_payload_scatter(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site)
                     & (spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1], inclusive=True))]
    filter_all = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1], inclusive=True)]
    # filtered_df = filtered_df.groupby(['class'])['Launch Site'].count().reset_index()
    if entered_site == 'All Sites':
        fig = px.scatter(filter_all, x='Payload Mass (kg)', y='class', color='Booster Version Category')

    else:
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')

    return fig

if __name__ == '__main__':
    app.run_server()


