import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from datetime import datetime, date
import pandas as pd
from my_globals import *

# ========= Layout ========= #
layout = dbc.Col([
    # Cabeçalho do sistema
    html.H1('MyBudget', className='text-primary'),
    html.P('Sistema de controle financeiro pessoal', className='text-info'),
    html.Hr(),

    # Avatar do usuário
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

    # Botões para adicionar receita/despesa
    dbc.Row([
        dbc.Col([dbc.Button(color='success', id='open-novo-receita', children=['+ Receita'])], width=6),
        dbc.Col([dbc.Button(color='danger', id='open-novo-despesa', children=['- Despesa'])], width=6),
    ]),

    # Modal de Receita
    dbc.Modal([
        dbc.ModalHeader('Adicionar Receita'),
        dbc.ModalBody([
            # Descrição e valor
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
            # Data, extras e categoria
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
                        value=cat_receita[0]['Categoria'] if cat_receita else None
                    )
                ], width=4),
            ], style={'margin-top': '25px'}),
            # Gerenciamento de categorias
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
                                    dbc.Checklist(
                                        id='checklist-remove-receita',
                                        options=[{'label': i['Categoria'], 'value': i['Categoria']} for i in cat_receita],
                                        value=[],
                                        label_checked_style={'color': 'red'}
                                    ),
                                    dbc.Button('Remover', className='btn btn-danger', id='remove-category-receita', style={'margin-top': '20px'})
                                ], width=6)
                            ])
                        ],
                        title='Gerenciar categorias'
                    )
                ], flush=True, start_collapsed=True, id='accordion-receita')
            ]),
            # Botão de salvar receita
            html.Div([
                dbc.Button('Adicionar Receita', id='save-receita', color='success'),
                dbc.Popover(
                    dbc.PopoverBody("Receita adicionada com sucesso!"),
                    target="save-receita", placement="right", trigger="click", id='popover-receita'
                )
            ], style={'margin-top': '25px'}),
            html.Div(id='teste_receita', style={'padding-top': '20px'})
        ])
    ], style={'background-color': 'rgba(17, 149, 79, 0.05)'}, id='modal-novo-receita', size='lg', is_open=False, centered=True, backdrop=True),

    # Modal de Despesa
    dbc.Modal([
        dbc.ModalHeader('Adicionar Despesa'),
        dbc.ModalBody([
            # Descrição e valor
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
            # Data, extras e categoria
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
                    dbc.Select(
                        id='select-despesa-categoria',
                        options=[{'label': i['Categoria'], 'value': i['Categoria']} for i in cat_despesa],
                        value=cat_despesa[0]['Categoria'] if cat_despesa else None
                    )
                ], width=4),
            ], style={'margin-top': '25px'}),
            # Gerenciamento de categorias
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
                                    dbc.Checklist(
                                        id='checklist-remove-despesa',
                                        options=[{'label': i['Categoria'], 'value': i['Categoria']} for i in cat_despesa],
                                        value=[],
                                        label_checked_style={'color': 'red'}
                                    ),
                                    dbc.Button('Remover', className='btn btn-danger', id='remove-category-despesa', style={'margin-top': '20px'})
                                ], width=6)
                            ])
                        ],
                        title='Gerenciar categorias'
                    )
                ], flush=True, start_collapsed=True, id='accordion-despesa')
            ]),
            # Botão de salvar despesa
            html.Div([
                dbc.Button('Adicionar Despesa', id='save-despesa', color='red'),
                dbc.Popover(
                    dbc.PopoverBody("Despesa adicionada com sucesso!"),
                    target="save-despesa", placement="right", trigger="click", id='popover-despesa'
                )
            ], style={'margin-top': '25px'}),
            html.Div(id='teste_despesa', style={'padding-top': '20px'})
        ])
    ], style={'background-color': 'rgba(17, 149, 79, 0.05)'}, id='modal-novo-despesa', size='lg', is_open=False, centered=True, backdrop=True),

    html.Br(),

    # Navegação lateral
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
        dbc.NavLink("Extratos", href="/extratos", active="exact")
    ], vertical=True, pills=True, id='nav-buttons', style={'margin-bottom': '50px'})
], id='sidebar-completa')

# ========= Callbacks ========= #

# Modal de receita - abre/fecha
@app.callback(
    Output('modal-novo-receita', 'is_open'),
    Input('open-novo-receita', 'n_clicks'),
    State('modal-novo-receita', 'is_open')
)
def toggle_modal_receita(n_clicks, is_open):
    # Toggle modal ao clicar
    if n_clicks:
        return not is_open
    return is_open

# Modal de despesa - abre/fecha
@app.callback(
    Output('modal-novo-despesa', 'is_open'),
    Input('open-novo-despesa', 'n_clicks'),
    State('modal-novo-despesa', 'is_open')
)
def toggle_modal_despesa(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Salva receita no store e CSV
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
    # Validação básica
    if not n or not valor:
        return receitas or []

    # Monta registro de receita
    nova_receita = {
        'valor': round(float(valor), 2),
        'Efetuado': 1 if switches and 1 in switches else 0,
        'Fixo': 1 if switches and 2 in switches else 0,
        'Data': pd.to_datetime(date_input).date() if date_input else pd.Timestamp.today().date(),
        'Categoria': categoria or '',
        'Descrição': descricao or ''
    }

    receitas = receitas or []
    receitas.append(nova_receita)
    pd.DataFrame(receitas).to_csv('df_receitas.csv', index=False)
    return receitas

# Salva despesa no store e CSV
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
    if not n or not valor:
        return despesas or []

    nova_despesa = {
        'valor': round(float(valor), 2),
        'Efetuado': 1 if switches and 1 in switches else 0,
        'Fixo': 1 if switches and 2 in switches else 0,
        'Data': pd.to_datetime(date_input).date() if date_input else pd.Timestamp.today().date(),
        'Categoria': categoria or '',
        'Descrição': descricao or ''
    }

    despesas = despesas or []
    despesas.append(nova_despesa)
    pd.DataFrame(despesas).to_csv('df_despesas.csv', index=False)
    return despesas

# Gerenciamento de categorias de despesa
@app.callback(
    [Output('select-despesa-categoria', 'options'),
     Output('checklist-remove-despesa', 'options'),
     Output('checklist-remove-despesa', 'value')],
    [Input('add-category-despesa', 'n_clicks'),
     Input('remove-category-despesa', 'n_clicks')],
    [
        State('input-add-despesa', 'value'),
        State('checklist-remove-despesa', 'value'),
    ]
)
def add_category(n_add, n_remove, txt, check_delete):
    # Carrega categorias do CSV
    try:
        df_cat_despesa = pd.read_csv('df_cat_despesas.csv')
        cat_despesa = df_cat_despesa['Categoria'].tolist()
    except Exception:
        cat_despesa = []

    # Adiciona nova categoria
    if n_add and txt and txt.strip() != "" and txt not in cat_despesa:
        cat_despesa.append(txt.strip())

    # Remove categorias selecionadas
    if n_remove and check_delete:
        cat_despesa = [cat for cat in cat_despesa if cat not in check_delete]

    # Salva categorias atualizadas
    pd.DataFrame(cat_despesa, columns=['Categoria']).to_csv('df_cat_despesas.csv', index=False)

    opt_despesa = [{'label': cat, 'value': cat} for cat in cat_despesa]
    return [opt_despesa, opt_despesa, []]

# Gerenciamento de categorias de receita
@app.callback(
    [Output('select-receita-categoria', 'options'),
     Output('checklist-remove-receita', 'options'),
     Output('checklist-remove-receita', 'value')],
    [Input('add-category-receita', 'n_clicks'),
     Input('remove-category-receita', 'n_clicks')],
    [
        State('input-add-receita', 'value'),
        State('checklist-remove-receita', 'value'),
    ]
)
def add_category_receita(n_add, n_remove, txt, check_delete):
    # Carrega categorias do CSV
    try:
        df_cat_receita = pd.read_csv('df_cat_receitas.csv')
        cat_receita = df_cat_receita['Categoria'].tolist()
    except Exception:
        cat_receita = []

    # Adiciona nova categoria
    if n_add and txt and txt.strip() != "" and txt not in cat_receita:
        cat_receita.append(txt.strip())

    # Remove categorias selecionadas
    if n_remove and check_delete:
        cat_receita = [cat for cat in cat_receita if cat not in check_delete]

    # Salva categorias atualizadas
    pd.DataFrame(cat_receita, columns=['Categoria']).to_csv('df_cat_receitas.csv', index=False)

    opt_receita = [{'label': cat, 'value': cat} for cat in cat_receita]
    return [opt_receita, opt_receita, []]
