from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from components import sidebar, dashboards, extratos
from my_globals import df_receitas, df_despesas, cat_receita, cat_despesa

# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    # Stores
    dcc.Store(id='store-receitas', data=df_receitas.to_dict('records')),
    dcc.Store(id='store-despesas', data=df_despesas.to_dict('records')),
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


if __name__ == '__main__':
    app.run(port=8051, debug=True)
