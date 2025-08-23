# Relatório Preliminar - Características de Repositórios Populares

Este projeto realiza a coleta automática de dados e métricas dos 100 repositórios públicos mais populares no GitHub, utilizando a **API GraphQL** do GitHub.  
São obtidas informações como número de estrelas, linguagem principal, releases, issues abertas e fechadas, pull requests mesclados, data de criação e última atualização.

## Funcionalidades

- Consulta automática aos 100 repositórios mais populares do GitHub (ordenados por estrelas).
- Utilização da API GraphQL para coletar informações detalhadas.
- Requisições automáticas com tolerância a erros temporários (retries para status 502, 503 e 504).
- Cálculo da razão de issues fechadas em relação ao total de issues.

## Hipóteses Informais para as Questões de Pesquisa

A seguir, são apresentadas as **questões de pesquisa (RQs)** e as respectivas **hipóteses informais** que orientarão a análise dos dados:

- **RQ 01. Sistemas populares são maduros/antigos?**  
  - **Hipótese Informal:** Espera-se que **sistemas populares sejam maduros/antigos**, pois a longevidade geralmente contribui para a sua popularidade e estabilidade. Um projeto com mais tempo de existência tende a ter mais funcionalidades, uma base de usuários estabelecida e maior confiança na comunidade.

- **RQ 02. Sistemas populares recebem muita contribuição externa?**  
  - **Hipótese Informal:** Espera-se que **sistemas populares recebam um alto volume de contribuições externas** (medido pelo total de *pull requests* aceitas), indicando uma comunidade ativa e engajada que impulsiona o desenvolvimento e a melhoria contínua do projeto.

- **RQ 03. Sistemas populares lançam *releases* com frequência?**  
  - **Hipótese Informal:** Espera-se que **sistemas populares lancem *releases* com frequência**, demonstrando um desenvolvimento contínuo e a entrega regular de novas funcionalidades, correções de bugs ou melhorias aos usuários. Isso sinaliza um projeto ativo e bem mantido.

- **RQ 04. Sistemas populares são atualizados com frequência?**  
  - **Hipótese Informal:** Espera-se que **sistemas populares sejam atualizados com muita frequência**, o que é crucial para manter a relevância, segurança, compatibilidade com novas tecnologias e para atender às demandas dos usuários e do ecossistema.

- **RQ 05. Sistemas populares são escritos nas linguagens mais populares?**  
  - **Hipótese Informal:** Espera-se que **sistemas populares sejam majoritariamente escritos nas linguagens de programação mais populares**, o que facilita a contribuição de uma base maior de desenvolvedores e a adoção por um público mais amplo, dado que essas linguagens possuem mais ferramentas, documentação e suporte.

- **RQ 06. Sistemas populares possuem um alto percentual de *issues* fechadas?**  
  - **Hipótese Informal:** Espera-se que **sistemas populares possuam um alto percentual de *issues* fechadas**, refletindo a eficiência da equipe de desenvolvimento em resolver problemas, responder às necessidades dos usuários e manter a qualidade do projeto. Um bom gerenciamento de *issues* é um indicativo de maturidade do projeto.

---

## Requisitos do projeto

- Python 3.11.0 ou superior
- Token de autenticação GitHub
- Pacote Python: `requests`

### Versões

- Python==3.11.0
- requests==2.32.3

## Preparação do ambiente

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **(Opcional) Crie um ambiente virtual**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências**:

   ```bash
   pip install requests
   ```

   ou

   ```bash
   pip install -r requirements.txt
   ```

4. **Gere seu token de acesso do GitHub**:

   - Vá até: [Configurações de Tokens do GitHub](https://github.com/settings/tokens)
   - Crie um token com permissões de leitura para repositórios públicos.
   - Copie o token gerado.

5. **Adicione o token ao código**:
   No início do arquivo principal, substitua `"TOKEN"` pelo seu token:

   ```python
   TOKEN = "seu_token_aqui"
   ```

6. **Documentação da API GraphQL do GitHub**:
   - [GraphQL API GitHub Docs](https://docs.github.com/pt/graphql)

## Uso

Para executar a coleta de dados, basta rodar:

```bash
python3 main.py
```

O script exibirá no console os dados coletados para cada repositório.

## Informações coletadas

Para cada repositório, são obtidos:

- **Nome do repositório** (owner/repo)
- **Número de estrelas**
- **Data de criação**
- **Última atualização**
- **Linguagem primária**
- **Número de releases**
- **Issues abertas**
- **Issues fechadas**
- **Razão de issues fechadas**
- **Pull requests mesclados**

## Descrição das funções principais

### `run_query(query, variables=None, retries=3)`

Executa uma consulta GraphQL para a API do GitHub.

- Aceita variáveis opcionais e número máximo de tentativas (`retries`).
- Trata erros temporários (502, 503, 504) com repetição automática.

### `get_top_repo_ids(total_repos=100)`

Obtém a lista com os `owner` e `name` dos repositórios mais populares, ordenados por estrelas.  
Usa paginação GraphQL para buscar até atingir `total_repos`.

### `get_repo_details(owner, name)`

Busca informações detalhadas de um repositório específico, incluindo métricas de issues, releases, linguagem primária e pull requests.

### `collect_and_print_repo_data()`

Função principal que orquestra:

1. Obtenção da lista de repositórios mais populares.
2. Consulta dos detalhes de cada repositório.
3. Impressão dos dados no console.
