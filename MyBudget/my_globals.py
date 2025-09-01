import pandas as pd
import os

# ---------- Carrega ou cria os CSVs de lançamentos ----------
if 'df_despesas.csv' in os.listdir() and 'df_receitas.csv' in os.listdir():
    df_despesas = pd.read_csv('df_despesas.csv', index_col=0, parse_dates=True)
    df_receitas = pd.read_csv('df_receitas.csv', index_col=0, parse_dates=True)
    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'], errors='coerce')
    df_receitas['Data'] = df_receitas['Data'].apply(lambda x: x.date())
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'], errors='coerce')
    df_despesas['Data'] = df_despesas['Data'].apply(lambda x: x.date())


else:
    data_structure = {'valor': [],
                      'Efetuado': [],
                      'Fixo': [],
                      'Data': [],
                      'Categoria': [],
                      'Descrição': []
                     }
    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure)
    df_receitas.to_csv('df_receitas.csv', index=False)
    df_despesas.to_csv('df_despesas.csv', index=False)

# ---------- Carrega ou cria os CSVs de categorias ----------
if 'df_cat_despesas.csv' in os.listdir() and 'df_cat_receitas.csv' in os.listdir():
    df_cat_despesas = pd.read_csv('df_cat_despesas.csv')  # <--- sem index_col
    df_cat_receitas = pd.read_csv('df_cat_receitas.csv')  # <--- sem index_col
else:
    cat_receita_dict = {'Categoria': ['Salário', 'Investimentos', 'Comissão']}
    cat_despesa_dict = {'Categoria': ['Alimentação', 'Transporte', 'Moradia', 'Saúde', 'Educação',
                                      'Lazer', 'Compras', 'Impostos', 'Serviços', 'Outros']}
    df_cat_receitas = pd.DataFrame(cat_receita_dict)
    df_cat_despesas = pd.DataFrame(cat_despesa_dict)
    df_cat_receitas.to_csv('df_cat_receitas.csv', index=False)
    df_cat_despesas.to_csv('df_cat_despesas.csv', index=False)

# ---------- Converte categorias para lista de dicionários ----------
cat_receita = df_cat_receitas.to_dict('records')
cat_despesa = df_cat_despesas.to_dict('records')

