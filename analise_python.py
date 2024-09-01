
# Importando as bibliotecas necessárias
import basedosdados as bd
import pandas as pd

# Configurando a autenticação no Google Cloud
# O caminho para o arquivo JSON será substituído conforme a necessidade
bd.configure(
    project_id="aerial-optics-433818",
    credentials_path="C:/Users/Softex/Downloads/aerial-optics-433818-g1-41cad062f65c.json"
)

# Função para buscar os dados da tabela de Chamados do 1746
def buscar_chamados():
    query = '''
    SELECT * FROM `basedosdados.br_rj_rio_1746.chamados`
    WHERE data_abertura BETWEEN '2023-04-01' AND '2023-04-01'
    '''
    df_chamados = bd.read_sql(query, billing_project_id="aerial-optics-433818")
    return df_chamados

# Consultas específicas conforme as perguntas
# Exemplo: Quantos chamados foram abertos no dia 01/04/2023?
def chamados_no_dia(df_chamados):
    total_chamados = df_chamados.shape[0]
    return total_chamados

# Exemplo de como utilizar a função
df_chamados = buscar_chamados()
print("Total de chamados em 01/04/2023:", chamados_no_dia(df_chamados))
