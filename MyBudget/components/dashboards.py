from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
#from globals import *
from app import app

card_icon = {
    "color": 'white',
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto"
}


# =========  Layout  =========== #
layout = dbc.Col([

    # ---------- Linha de Cards de Resumo (Saldo, Receita, Despesa) ----------
    dbc.Row([

        # Saldo Total
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo'),
                    html.H5('R$ 1.000,00', id='saldo-dashboard',
                            style={'padding-left': '20px', 'padding-top': '10px'})
                ]),
                dbc.Card([html.Div(className='fa fa-university', style=card_icon)],
                         color='warning', style={'maxWidth': 75, 'height': 100, 'marginLeft': '-10px'})
            ])
        ], width=4),

        # Receita
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Receita'),
                    html.H5('R$ 1.000,00', id='receita-dashboard',
                            style={'padding-left': '20px', 'padding-top': '10px'})
                ]),
                dbc.Card([html.Div(className='fa fa-smile-o', style=card_icon)],
                         color='success', style={'maxWidth': 75, 'height': 100, 'marginLeft': '-10px'})
            ])
        ], width=4),

        # Despesa
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Despesa'),
                    html.H5('R$ 1.000,00', id='despesa-dashboard',
                            style={'padding-left': '20px', 'padding-top': '10px'})
                ]),
                dbc.Card([html.Div(className='fa fa-meh-o', style=card_icon)],
                         color='danger', style={'maxWidth': 75, 'height': 100, 'marginLeft': '-10px'})
            ])
        ], width=4)
    ], style={'margin': '10px'}),

    # ---------- Filtros ----------
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Filtrar lançamentos', className='card-title'),

                # Filtro de Categorias de Receitas
                html.Label('Categoria das receitas'),
                dcc.Dropdown(
                    id='dropdown-categorias-receitas',
                    clearable=False,
                    style={'width': '100%'},
                    persistence=True,
                    persistence_type='session',
                    multi=True
                ),

                # Filtro de Categorias de Despesas
                html.Label('Categoria das despesas', style={'marginTop': '6px'}),
                dcc.Dropdown(
                    id='dropdown-categorias-despesas',
                    clearable=False,
                    style={'width': '100%'},
                    persistence=True,
                    persistence_type='session',
                    multi=True
                ),

                # Filtro de Período
                html.Legend('Período de Análise', style={'marginTop': '10px'}),
                dcc.DatePickerRange(
                    month_format='Do MMM, YY',
                    end_date_placeholder_text='Data...',
                    start_date=datetime(2022, 4, 1).date(),
                    end_date=(datetime.today() + timedelta(days=31)).date(),
                    updatemode='singledate',
                    id='date-picker-range',
                    style={'zIndex': '100'}
                )
            ], style={'height': '100%', 'padding': '10px'})
        ], width=4),

        # Gráfico principal
        dbc.Col([dbc.Card(dcc.Graph(id='graph1'), style={'height': '100%', 'padding': '10px'})], width=8)

    ], style={'margin': '10px'}),

    # ---------- Linha de Gráficos Secundários ----------
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='graph2'), style={'height': '100%', 'padding': '10px'}), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id='graph3'), style={'height': '100%', 'padding': '10px'}), width=3),
        dbc.Col(dbc.Card(dcc.Graph(id='graph4'), style={'height': '100%', 'padding': '10px'}), width=3),
    ])

])




# =========  Callbacks  =========== #
