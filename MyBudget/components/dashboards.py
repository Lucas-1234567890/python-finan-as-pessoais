from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from app import app

# Configuração visual dos ícones dos cards
card_icon = {
    "color": 'white',
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto"
}

# =========  Layout  =========== #
layout = dbc.Col([
    # Cards de resumo
    dbc.Row([
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

    # Filtros e gráfico principal
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Filtrar lançamentos', className='card-title'),
                html.Label('Categoria das receitas'),
                dcc.Dropdown(
                    id='dropdown-categorias-receitas',
                    clearable=False,
                    style={'width': '100%'},
                    persistence=True,
                    persistence_type='session',
                    multi=True
                ),
                html.Label('Categoria das despesas', style={'marginTop': '6px'}),
                dcc.Dropdown(
                    id='dropdown-categorias-despesas',
                    clearable=False,
                    style={'width': '100%'},
                    persistence=True,
                    persistence_type='session',
                    multi=True
                ),
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
        dbc.Col([dbc.Card(dcc.Graph(id='graph1'), style={'height': '100%', 'padding': '10px'})], width=8)
    ], style={'margin': '10px'}),

    # Linha de gráficos secundários
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='graph2'), style={'height': '100%', 'padding': '10px'}), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id='graph3'), style={'height': '100%', 'padding': '10px'}), width=3),
        dbc.Col(dbc.Card(dcc.Graph(id='graph4'), style={'height': '100%', 'padding': '10px'}), width=3),
    ])
])

# =========  Callbacks  =========== #

# Preenche dropdown de categorias de receitas e atualiza card de receita
@app.callback(
    [Output('dropdown-categorias-receitas','options'),
     Output('dropdown-categorias-receitas','value'),
     Output('receita-dashboard','children')],
    Input('store-receitas', 'data')
)
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    # Protege contra df vazio ou sem coluna 'Categoria'
    if df.empty or 'Categoria' not in df.columns:
        return [], None, "R$ 0,00"
    valor = df.get('valor', pd.Series([0]*len(df))).sum()
    val = df['Categoria'].unique().tolist()
    options = [{'label': c, 'value': c} for c in val]
    return options, val[0] if val else None, f"R$ {valor:,.2f}"

# Preenche dropdown de categorias de despesas e atualiza card de despesa
@app.callback(
    [Output('dropdown-categorias-despesas','options'),
     Output('dropdown-categorias-despesas','value'),
     Output('despesa-dashboard','children')],
    Input('store-despesas', 'data')
)
def populate_dropdownvalues_despesas(data):
    df = pd.DataFrame(data)
    if df.empty or 'Categoria' not in df.columns:
        return [], None, "R$ 0,00"
    valor = df.get('valor', pd.Series([0]*len(df))).sum()
    val = df['Categoria'].unique().tolist()
    options = [{'label': c, 'value': c} for c in val]
    return options, val[0] if val else None, f"R$ {valor:,.2f}"

# Atualiza card de saldo total
@app.callback(
    Output('saldo-dashboard', 'children'),
    [Input('store-receitas', 'data'),
     Input('store-despesas', 'data')]
)
def update_saldo(receitas, despesas):
    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)
    valor_receitas = df_receitas.get('valor', pd.Series([0]*len(df_receitas))).sum()
    valor_despesas = df_despesas.get('valor', pd.Series([0]*len(df_despesas))).sum()
    saldo = valor_receitas - valor_despesas
    return f"R$ {saldo:,.2f}"

# Gráfico de fluxo de caixa acumulado
@app.callback(
    Output('graph1', 'figure'),
    [Input('store-receitas', 'data'),
     Input('store-despesas', 'data'),
     Input('dropdown-categorias-receitas', 'value'),
     Input('dropdown-categorias-despesas', 'value')]
)
def update_output(data_receita, data_despesa, receita, despesa):
    import plotly.graph_objects as go
    import pandas as pd

    df_receitas = pd.DataFrame(data_receita)
    df_despesas = pd.DataFrame(data_despesa)

    # Padroniza colunas
    df_receitas.columns = [c.lower() for c in df_receitas.columns]
    df_despesas.columns = [c.lower() for c in df_despesas.columns]

    # Trata vazio
    if df_receitas.empty or 'data' not in df_receitas.columns or 'valor' not in df_receitas.columns:
        df_receitas = pd.DataFrame(columns=['data', 'valor', 'categoria'])
    if df_despesas.empty or 'data' not in df_despesas.columns or 'valor' not in df_despesas.columns:
        df_despesas = pd.DataFrame(columns=['data', 'valor', 'categoria'])

    # Filtra categorias
    receita = receita if isinstance(receita, list) else [receita] if receita else []
    despesa = despesa if isinstance(despesa, list) else [despesa] if despesa else []
    if receita:
        df_receitas = df_receitas[df_receitas['categoria'].isin(receita)]
    if despesa:
        df_despesas = df_despesas[df_despesas['categoria'].isin(despesa)]

    # Agrupa
    df_receitas['data'] = pd.to_datetime(df_receitas['data'], errors='coerce')
    df_despesas['data'] = pd.to_datetime(df_despesas['data'], errors='coerce')
    df_rs = df_receitas.groupby('data')['valor'].sum().rename('Receita')
    df_ds = df_despesas.groupby('data')['valor'].sum().rename('Despesa')

    # Junta e preenche datas faltantes
    df_acum = pd.concat([df_rs, df_ds], axis=1).fillna(0)
    df_acum = df_acum.sort_index()
    # Preenche datas faltantes no range
    if not df_acum.empty:
        full_range = pd.date_range(df_acum.index.min(), df_acum.index.max(), freq='D')
        df_acum = df_acum.reindex(full_range, fill_value=0)
    df_acum['Acum'] = df_acum['Receita'] - df_acum['Despesa']
    df_acum['Acum'] = df_acum['Acum'].cumsum()

    # Gráfico
    fig = go.Figure()

    # Linha acumulada
    fig.add_trace(go.Scatter(
        x=df_acum.index,
        y=df_acum['Acum'],
        mode='lines+markers',
        name='Fluxo de Caixa',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=6, color='#FF6B6B'),
        hovertemplate="Data: %{x}<br>Saldo: R$ %{y:,.2f}<extra></extra>"
    ))

    # Área preenchida (dá mais corpo)
    fig.add_trace(go.Scatter(
        x=df_acum.index,
        y=df_acum['Acum'],
        fill='tozeroy',
        mode='none',
        name='Acumulado',
        fillcolor='rgba(46,134,171,0.2)'
    ))

    # Layout mais analista sênior
    fig.update_layout(
        title="📈 Fluxo de Caixa Acumulado",
        xaxis_title="Data",
        yaxis_title="Saldo (R$)",
        template="plotly_white",
        hovermode="x unified",
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor="lightgrey"),
        yaxis=dict(showgrid=True, gridcolor="lightgrey"),
        font=dict(family="Arial", size=12),
        title_font=dict(size=20)
    )

    return fig


# Gráfico de barras de receitas e despesas por período
@app.callback(
    Output('graph2', 'figure'),
    [Input('store-receitas', 'data'),
     Input('store-despesas', 'data'),
     Input('dropdown-categorias-receitas', 'value'),
     Input('dropdown-categorias-despesas', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def graph2_show(data_receita, data_despesa, receita, despesa, start_date, end_date):
    df_receitas = pd.DataFrame(data_receita)
    df_despesas = pd.DataFrame(data_despesa)

    df_despesas['Output'] = "Despesas"
    df_receitas['Output'] = "Receitas"
    df_final = pd.concat([df_receitas, df_despesas], axis=0)

    # Padroniza nome da coluna de data
    if 'Data' in df_final.columns:
        df_final.rename(columns={'Data': 'data'}, inplace=True)
    if 'data' in df_final.columns:
        df_final['data'] = pd.to_datetime(df_final['data'], errors='coerce')

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    if 'data' in df_final.columns:
        df_final = df_final[(df_final['data'] >= start_date) & (df_final['data'] <= end_date)]

    # Garante que receita e despesa sejam listas
    receita = receita if isinstance(receita, list) else [receita] if receita else []
    despesa = despesa if isinstance(despesa, list) else [despesa] if despesa else []

    # Filtra por categoria
    if 'Categoria' in df_final.columns:
        df_final = df_final[(df_final['Categoria'].isin(receita)) | (df_final['Categoria'].isin(despesa))]

    # Se não houver dados, retorna gráfico vazio
    if df_final.empty or 'data' not in df_final.columns or 'valor' not in df_final.columns:
        fig = px.bar(title="Receitas e Despesas por Data")
        fig.update_layout(xaxis_title="Data", yaxis_title="Valor", legend_title="Tipo")
        return fig

    fig = px.bar(df_final, x='data', y='valor', color='Output', barmode='group',
                 title="Receitas e Despesas por Data")
    fig.update_layout(xaxis_title="Data", yaxis_title="Valor", legend_title="Tipo")
    return fig

# Gráfico de rosca (pie) de receitas por categoria
@app.callback(Output('graph3', 'figure'),
                [Input('store-receitas', 'data'),
                 Input('dropdown-categorias-receitas', 'value')]
               )
def Pie_receita(data, categoria):
    df = pd.DataFrame(data)
    # Garante que a coluna 'valor' existe
    if 'valor' not in df.columns:
        df['valor'] = 0
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df['Categoria'] = df.get('Categoria', pd.Series(['Outros']*len(df))).str.strip().str.lower()
    categoria = [c.lower() for c in categoria] if categoria else []

    if categoria:
        df = df[df['Categoria'].isin(categoria)]

    df = df.groupby('Categoria', as_index=False)['valor'].sum()

    if df.empty:
        fig = px.pie(names=[], values=[], title="Receitas por Categoria", hole=0.5)
        fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        return fig

    fig = px.pie(df, names='Categoria', values='valor', title="Receitas por Categoria", hole=0.5)
    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    return fig

# Gráfico de rosca (pie) de despesas por categoria
@app.callback(Output('graph4', 'figure'),
              [Input('store-despesas', 'data'),
               Input('dropdown-categorias-despesas', 'value')]
              )
def Pie_despesa(data, categoria):
    df = pd.DataFrame(data)
    if 'valor' not in df.columns:
        df['valor'] = 0
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df['Categoria'] = df.get('Categoria', pd.Series(['Outros']*len(df))).str.strip().str.lower()
    categoria = [c.lower() for c in categoria] if categoria else []

    if categoria:
        df = df[df['Categoria'].isin(categoria)]

    df = df.groupby('Categoria', as_index=False)['valor'].sum()

    if df.empty:
        fig = px.pie(names=[], values=[], title="Despesas por Categoria", hole=0.5)
        fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        return fig

    fig = px.pie(df, names='Categoria', values='valor', title="Despesas por Categoria", hole=0.5)
    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    return fig
