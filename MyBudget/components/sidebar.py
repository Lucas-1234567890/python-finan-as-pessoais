import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd
from my_globals import *


# ========= Layout ========= #
layout = dbc.Col([
    # ---------- Cabeçalho ----------
    #dcc.Store(id='store-receitas', data=[]),
    html.H1('MyBudget', className='text-primary'),
    html.P('Sistema de controle financeiro pessoal', className='text-info'),
    html.Hr(),

    # ---------- Seção de Perfil ----------
    dbc.Button(
        id='botao-avatar',
        children=[
            html.Img(
                src='/assets/img_hom.png',
                id='avatar_chan',
                alt='Avatar',
                className='perfil_avatar',
                style={'background-color': 'transparent', 'border-color': 'transparent'}
            )
        ]
    ),

    # ---------- Seção NOVO (Receita/Despesa) ----------
    dbc.Row([
        dbc.Col([dbc.Button(color='success', id='open-novo-receita', children=['+ Receita'])], width=6),
        dbc.Col([dbc.Button(color='danger', id='open-novo-despesa', children=['- Despesa'])], width=6),
    ]),

   # ---------- Modal Receita ----------
dbc.Modal([
    dbc.ModalHeader('Adicionar Receita'),
    dbc.ModalBody([
        # Linha 1: Descrição e Valor
        dbc.Row([
            dbc.Col([
                dbc.Label('Descrição'),
                dbc.Input(placeholder='Ex.: salário, venda, reembolso', type='text', id='input-receita-descricao')
            ], width=6),
            dbc.Col([
                dbc.Label('Valor'),
                dbc.Input(placeholder='Ex.: 1000', type='number', id='input-receita-valor')
            ], width=6),
        ]),

        # Linha 2: Data, Extras e Categoria
        dbc.Row([
            dbc.Col([
            dbc.Label("Data:"),
            dcc.DatePickerSingle(
                id='input-receita-data',
                min_date_allowed=date(2023, 1, 1),
                max_date_allowed=date(2030, 12, 31),
                date=date.today(),
                style={'width': '100%'}
            )
            ], width=4),
            dbc.Col([
            dbc.Label("Extras"),
            dbc.Checklist(
                options=[
                {'label': 'Foi recebida', 'value': 1},
                {'label': 'Receita recorrente', 'value': 2}
                ],
                value=[],
                id="switchs-input-receita",
                switch=True
            )
            ], width=4),
            dbc.Col([
            dbc.Label("Categoria de Receitas"),
            dbc.Select(
                id='select-receita-categoria',
                options=[{'label': i['Categoria'], 'value': i['Categoria']} for i in cat_receita],
                value=cat_receita[0]['Categoria'] 
            )
            ], width=4),
        ], style={'margin-top': '25px'}),

        # Linha 3: Accordion para gerenciar categorias
        dbc.Row([
            dbc.Accordion([
                dbc.AccordionItem(
                    children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria", style={'color': 'green'}),
                                dbc.Input(type='text', placeholder='Nova categoria...', id='input-add-receita', value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success', id='add-category-receita', style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(id='category-div-add-receita')
                            ], width=6),
                            dbc.Col([
                                html.Legend("Remover categoria", style={'color': 'red'}),
                                dbc.Checklist(id='checklist-remove-receita', 
                                              options=[{'label': i['Categoria'], 'value': i['Categoria']} for i in cat_receita], 
                                              value=[], 
                                              label_checked_style={'color': 'red'}),
                                dbc.Button('Remover', className='btn btn-danger', id='remove-category-receita', style={'margin-top': '20px'})
                            ], width=6)
                        ])
                    ],
                    title='Gerenciar categorias'
                )
            ], flush=True, start_collapsed=True, id='accordion-receita')
        ]),

        # Botão de salvar receita com Popover
        html.Div([
            dbc.Button('Adicionar Receita', id='save-receita', color='success'),
            dbc.Popover(dbc.PopoverBody("Receita adicionada com sucesso!"), target="save-receita", placement="right", trigger="click", id='popover-receita')
        ], style={'margin-top': '25px'}),

        html.Div(id='teste_receita', style={'padding-top': '20px'})
    ])
], style={'background-color': 'rgba(17, 149, 79, 0.05)'}, id='modal-novo-receita', size='lg', is_open=False, centered=True, backdrop=True),


    # ---------- Modal Despesa ----------
    dbc.Modal([
        dbc.ModalHeader('Adicionar Despesa'),
        dbc.ModalBody([
            # Linha 1: Descrição e Valor
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição'),
                    dbc.Input(placeholder='Ex.: despesa com alimentação', type='text', id='input-despesa-descricao')
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor'),
                    dbc.Input(placeholder='Ex.: 100', type='number', id='input-despesa-valor')
                ], width=6),
            ]),

            # Linha 2: Data, Extras e Categoria
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data:"),
                    dcc.DatePickerSingle(
                        id='input-despesa-data',
                        min_date_allowed=date(2023, 1, 1),
                        max_date_allowed=date(2030, 12, 31),
                        date=date.today(),
                        style={'width': '100%'}
                    )
                ], width=4),
                dbc.Col([
                    dbc.Label("Extras"),
                    dbc.Checklist(
    options=[
        {'label': 'Foi paga', 'value': 1},
        {'label': 'Despesa recorrente', 'value': 2}
    ],
    value=[],
    id="switchs-input-despesa",
    switch=True
)
                ], width=4),
                dbc.Col([
                    dbc.Label("Categoria de Despesas"),
                    dbc.Select(id='select-despesa-categoria', options=[{'label': i['Categoria'], 'value': i['Categoria']} for i in cat_despesa], value=cat_despesa[0]['Categoria'])
                ], width=4),
            ], style={'margin-top': '25px'}),

            # Linha 3: Accordion para gerenciar categorias
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(
                        children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend("Adicionar categoria", style={'color': 'green'}),
                                    dbc.Input(type='text', placeholder='Nova categoria...', id='input-add-despesa', value=''),
                                    html.Br(),
                                    dbc.Button('Adicionar', className='btn btn-success', id='add-category-despesa', style={'margin-top': '20px'}),
                                    html.Br(),
                                    html.Div(id='category-div-add-despesa')
                                ], width=6),
                                dbc.Col([
                                    html.Legend("Remover categoria", style={'color': 'red'}),
                                    dbc.Checklist(id='checklist-remove-despesa',
                                                   options=[{'label': i['Categoria'], 'value': i['Categoria']} for i in cat_despesa],
                                                     value=[],
                                                     label_checked_style={'color': 'red'}),
                                    dbc.Button('Remover', className='btn btn-danger', id='remove-category-despesa', style={'margin-top': '20px'})
                                ], width=6)
                            ])
                        ],
                        title='Gerenciar categorias'
                    )
                ], flush=True, start_collapsed=True, id='accordion-despesa')
            ]),

            # Botão de salvar despesa com Popover
            html.Div([
                dbc.Button('Adicionar Despesa', id='save-despesa', color='red'),
                dbc.Popover(dbc.PopoverBody("Despesa adicionada com sucesso!"), target="save-despesa", placement="right", trigger="click", id='popover-despesa')
            ], style={'margin-top': '25px'}),

            html.Div(id='teste_despesa', style={'padding-top': '20px'})
        ])
    ], style={'background-color': 'rgba(17, 149, 79, 0.05)'}, id='modal-novo-despesa', size='lg', is_open=False, centered=True, backdrop=True),

    html.Br(),

    # ---------- Seção NAV ----------
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
        dbc.NavLink("Extratos", href="/extratos", active="exact")
    ], vertical=True, pills=True, id='nav-buttons', style={'margin-bottom': '50px'})
], id='sidebar-completa')



# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output('modal-novo-receita', 'is_open'),
    Input('open-novo-receita', 'n_clicks'),
    State('modal-novo-receita', 'is_open')
)
def toggle_modal_receita(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output('modal-novo-despesa', 'is_open'),
    Input('open-novo-despesa', 'n_clicks'),
    State('modal-novo-despesa', 'is_open')
)
def toggle_modal_despesa(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output('store-receitas', 'data'),
    Input('save-receita', 'n_clicks'),
    State('input-receita-valor', 'value'),
    State('input-receita-descricao', 'value'),
    State('select-receita-categoria', 'value'),
    State('input-receita-data', 'date'),
    State('switchs-input-receita', 'value'),
    State('store-receitas', 'data'),
    prevent_initial_call=True
)
def save_receita(n, valor, descricao, categoria, date_input, switches, receitas):
    if not n:
        return receitas or []

    # Validação simples
    if not valor:
        return receitas or []

    # Monta nova receita
    nova_receita = {
        'valor': round(float(valor), 2),
        'Efetuado': 1 if switches and 1 in switches else 0,
        'Fixo': 1 if switches and 2 in switches else 0,
        'Data': pd.to_datetime(date_input).date() if date_input else pd.Timestamp.today().date(),
        'Categoria': categoria or '',
        'Descrição': descricao or ''
    }

    # Atualiza lista e salva CSV
    receitas = receitas or []
    receitas.append(nova_receita)
    pd.DataFrame(receitas).to_csv('df_receitas.csv', index=False)
    return receitas
@app.callback(
    Output('store-despesas', 'data'),
    Input('save-despesa', 'n_clicks'),
    State('input-despesa-valor', 'value'),
    State('input-despesa-descricao', 'value'),
    State('select-despesa-categoria', 'value'),
    State('input-despesa-data', 'date'),
    State('switchs-input-despesa', 'value'),
    State('store-despesas', 'data'),
    prevent_initial_call=True
)
def save_despesa(n, valor, descricao, categoria, date_input, switches, despesas):
    # se não clicou ou valor vazio, retorna o store atual
    if not n:
        return despesas or []
    if not valor:
        return despesas or []

    # monta nova despesa (mesma estrutura do CSV que você usa)
    nova_despesa = {
        'valor': round(float(valor), 2),
        'Efetuado': 1 if (switches and 1 in switches) else 0,   # foi paga
        'Fixo': 1 if (switches and 2 in switches) else 0,      # recorrente
        'Data': pd.to_datetime(date_input).date() if date_input else pd.Timestamp.today().date(),
        'Categoria': categoria or '',
        'Descrição': descricao or ''
    }

    despesas = despesas or []
    despesas.append(nova_despesa)

    # salva CSV de despesas
    pd.DataFrame(despesas).to_csv('df_despesas.csv', index=False)

    return despesas



