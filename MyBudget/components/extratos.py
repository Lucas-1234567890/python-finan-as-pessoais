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
                    html.Legend('R$ 400,00', id='valor-despesa-card', style={'font-size': '60px'}),
                    html.H6("Total de Despesas")
                ], style={'textAlign': 'center', 'padding-top': '30px'})
            )
        ], width=3)
    ])
], style={'padding': '1px'})

# =========  Callbacks  =========== #
# Tabela
@app.callback(
    Output('tabela-extrato', 'children'),
    Input('store-despesas', 'data')
)
def imprimir_tabela(data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date
    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False)

    tabela = dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
                                   style_table={'overflowX': 'auto'},
                                   style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
                                   page_size=10)
    return tabela

@app.callback(
    Output('bar-graph', 'figure'),
    Input('store-despesas', 'data')
)
def bar_chart(data):
    df = pd.DataFrame(data)
    # Agrupa por categoria e soma valores
    df_grouped = df.groupby('Categoria', as_index=False)['valor'].sum()
    graph = px.bar(df_grouped, x='Categoria', y='valor', title='Despesas por Categoria')
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return graph

@app.callback(
    Output('valor-despesa-card', 'children'),

    Input('store-despesas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['valor'].sum()
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
