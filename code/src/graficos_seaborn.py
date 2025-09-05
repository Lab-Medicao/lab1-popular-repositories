import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os

def salvar_grafico(nome_arquivo):
    pasta = './docs/charts'
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f'{nome_arquivo}.png')
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print(f'Gráfico salvo em: {caminho}')

# RQ 01: Sistemas populares são maduros/antigos?
# Métrica: Idade do repositório 
# Gráfico: Violino (violin plot)
def grafico_idade_repos(df):
    df['Created At'] = pd.to_datetime(df['Created At'], utc=True)
    now = datetime.now(timezone.utc)
    df['Idade (anos)'] = (now - df['Created At']).dt.days / 365
    plt.figure(figsize=(10,6))
    sns.violinplot(y=df['Idade (anos)'])
    plt.title('Distribuição da idade dos repositórios populares (anos)')
    plt.ylabel('Idade (anos)')
    salvar_grafico('RQ01.idade_repositorios')

# RQ 02: Sistemas populares recebem muita contribuição externa?
# Métrica: Total de pull requests aceitas 
# Gráfico: Dispersão (scatter plot)
def grafico_pull_requests(df):
    plt.figure(figsize=(10,6))
    plt.scatter(df['Stars'], df['Merged Pull Requests'])
    plt.xlabel('Estrelas (Popularidade)')
    plt.ylabel('Pull Requests Aceitas (Contribuição Externa)')
    plt.title('Popularidade vs Contribuição Externa nos Repositórios')
    salvar_grafico('RQ02.pull_requests_aceitas')

# RQ 03: Sistemas populares lançam releases com frequência?
# Métrica: Total de releases 
# Gráfico: Dispersão (scatter plot)
def grafico_releases(df):
    plt.figure(figsize=(12,6))
    plt.scatter(df['Stars'], df['Releases'])
    plt.xlabel('Estrelas (Popularidade)')
    plt.ylabel('Total de Releases')
    plt.title('Releases vs Popularidade')
    salvar_grafico('RQ03.total_releases')

# RQ 04: Sistemas populares são atualizados com frequência?
# Métrica: Tempo até a última atualização 
# Gráfico: Histograma (histplot)
def grafico_tempo_ultima_atualizacao(df):
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], utc=True)
    now = datetime.now(timezone.utc)
    df['Dias desde última atualização'] = (now - df['Last Updated']).dt.days
    plt.figure(figsize=(10,6))
    sns.histplot(df['Dias desde última atualização'], bins=20, kde=True)
    plt.title('Distribuição do tempo desde a última atualização dos repositórios (dias)')
    plt.xlabel('Dias desde última atualização')
    plt.ylabel('Quantidade de repositórios')
    salvar_grafico('RQ04.tempo_ultima_atualizacao')

# RQ 05: Sistemas populares são escritos nas linguagens mais populares?
# Métrica: Linguagem primária dos repositórios populares 
# Gráfico: Swarmplot
def grafico_linguagem_primaria(df):
    plt.figure(figsize=(12,10))
    sns.swarmplot(y='Primary Language', data=df, size=3)
    plt.title('Distribuição das linguagens primárias dos repositórios populares')
    plt.ylabel('Linguagem')
    salvar_grafico('RQ05.linguagem_primaria')

# RQ 06: Sistemas populares possuem um alto percentual de issues fechadas?
# Métrica: Percentual de issues fechadas 
# Gráfico: Violino (violin plot)
def grafico_percentual_issues_fechadas(df):
    plt.figure(figsize=(12,6))
    sns.violinplot(y=df['Closed Issues Ratio'])
    plt.title('Distribuição do percentual de issues fechadas')
    plt.ylabel('Razão de Issues Fechadas')
    salvar_grafico('RQ06.percentual_issues_fechadas')

# RQ 07 - Extra: Sistemas escritos em linguagens mais populares recebem mais 
# contribuição externa, lançam mais releases e são atualizados com mais frequência?
# Comparação entre os resultados para os sistemas com as linguagens da 
# reportagem fornecida (imagem "GitHub-Octoverse-2024-top-programming-languages) 
# com os resultados de sistemas em outras linguagens.
# Métricas: Total de pull requests aceitas, total de releases, tempo até a última atualização
# Gráfico: Boxplot
def grafico_extra_linguagens_populares(df):
    linguagens_populares = [
        "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "PHP", "Shell", "C", "Go"
    ]
    df['Grupo Linguagem'] = df['Primary Language'].apply(
        lambda x: 'Popular' if x in linguagens_populares else 'Outras'
    )
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], utc=True)
    now = datetime.now(timezone.utc)
    df['Dias desde última atualização'] = (now - df['Last Updated']).dt.days

    fig, axes = plt.subplots(1, 3, figsize=(18,6))

    sns.boxplot(x='Grupo Linguagem', y='Merged Pull Requests', data=df, ax=axes[0])
    axes[0].set_title('Pull Requests Aceitas')

    sns.boxplot(x='Grupo Linguagem', y='Releases', data=df, ax=axes[1])
    axes[1].set_title('Total de Releases')

    sns.boxplot(x='Grupo Linguagem', y='Dias desde última atualização', data=df, ax=axes[2])
    axes[2].set_title('Dias desde última atualização')

    fig.suptitle('Comparação: Linguagens populares vs Outras')
    salvar_grafico('RQ07.linguagens_populares')

# Gráfico adicional: Heatmap de correlações entre métricas
def grafico_extra_heatmap_correlacoes(df):
    df['Created At'] = pd.to_datetime(df['Created At'], utc=True)
    now = datetime.now(timezone.utc)
    df['Idade (anos)'] = (now - df['Created At']).dt.days / 365
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], utc=True)
    df['Dias desde última atualização'] = (now - df['Last Updated']).dt.days

    cols = [
        'Stars', 'Merged Pull Requests', 'Releases',
        'Closed Issues Ratio', 'Idade (anos)', 'Dias desde última atualização'
    ]
    corr = df[cols].corr()

    plt.figure(figsize=(10,8))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Heatmap de Correlação entre Métricas dos Repositórios')
    salvar_grafico('extra_correlacoes')

def main():
    df = pd.read_csv('./code/src/repos_data.csv')

    grafico_idade_repos(df)
    grafico_pull_requests(df)
    grafico_releases(df)
    grafico_tempo_ultima_atualizacao(df)
    grafico_linguagem_primaria(df)
    grafico_percentual_issues_fechadas(df)
    grafico_extra_linguagens_populares(df)
    grafico_extra_heatmap_correlacoes(df) 

if __name__ == '__main__':
    main()