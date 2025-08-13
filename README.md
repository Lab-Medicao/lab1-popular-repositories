# Coleta de Dados dos 100 Repositórios Mais Populares no GitHub via GraphQL

Este projeto realiza a coleta automática de dados e métricas dos 100 repositórios públicos mais populares no GitHub, utilizando a **API GraphQL** do GitHub.  
São obtidas informações como número de estrelas, linguagem principal, releases, issues abertas e fechadas, pull requests mesclados, data de criação e última atualização.

## Funcionalidades

- Consulta automática aos 100 repositórios mais populares do GitHub (ordenados por estrelas).
- Utilização da API GraphQL para coletar informações detalhadas.
- Requisições automáticas com tolerância a erros temporários (retries para status 502, 503 e 504).
- Cálculo da razão de issues fechadas em relação ao total de issues.

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
