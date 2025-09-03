from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from app import app
from components import sidebar, dashboards, extratos
from my_globals import df_receitas, df_despesas, cat_receita, cat_despesa

def load_csv_or_empty(path, cols):
    try:
        df = pd.read_csv(path)
        # Padroniza colunas
        for col in cols:
            if col not in df.columns:
                df[col] = ''
        return df[cols].to_dict('records')
    except Exception:
        return []

# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    # Stores
    dcc.Store(id='store-receitas', data=load_csv_or_empty('df_receitas.csv', ['valor', 'Efetuado', 'Fixo', 'Data', 'Categoria', 'Descrição'])),
    dcc.Store(id='store-despesas', data=load_csv_or_empty('df_despesas.csv', ['valor', 'Efetuado', 'Fixo', 'Data', 'Categoria', 'Descrição'])),
    dcc.Store(id='store-cat-receitas', data=cat_receita),
    dcc.Store(id='store-cat-despesas', data=cat_despesa),

    # URL
    dcc.Location(id="url"),
    
    # Layout principal
    dbc.Row([
        dbc.Col([sidebar.layout], md=2),
        dbc.Col([content], md=10)
    ])
], fluid=True)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def render_page(pathname):
    if pathname in ['/', '/dashboard']:
        return dashboards.layout
    if pathname == '/extratos':
        return extratos.layout
    # fallback: rota desconhecida
    return dashboards.layout


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)




