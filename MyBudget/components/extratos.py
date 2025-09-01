import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend('Tabela de Despesas'),
        html.Div(id='tabela-extrato', className='dbc')
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph', style={'margin-right': '20px'})
        ], width=9),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Despesas"),
                    html.Legend('R$ 400,00', id='valor-depesa-card', style={'font-size': '60px'}),
                    html.H6("Total de Despesas")
                ], style={'textAlign': 'center', 'padding-top': '30px'})
            )
        ], width=3)
    ])
], style={'padding': '1px'})

# =========  Callbacks  =========== #
# Tabela
