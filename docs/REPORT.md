# Relatório técnico: Características de Repositórios Populares

## Objetivo

Este projeto realiza a coleta automática de dados e métricas dos 100 repositórios públicos mais populares no GitHub, utilizando a **API GraphQL** do GitHub.  
São obtidas informações como número de estrelas, linguagem principal, releases, issues abertas e fechadas, pull requests mesclados, data de criação e última atualização.

## Linguagem de Programação

O experimento foi desenvolvido utilizando Python 3.11.0, escolhido pelo suporte a bibliotecas modernas e ampla compatibilidade com pacotes de análise de dados e requisições HTTP.

## Requisitos do Projeto

Para executar o experimento, são necessários:
- Python 3.11.0 ou superior
- Token de autenticação do GitHub
- Pacotes Python:
   - requests: para realizar requisições HTTP à API do GitHub
   - keyring: para recuperar o token de autenticação armazenado de forma segura
   - pandas: para manipulação e análise dos dados coletados
   - seaborn: para visualização gráfica das métricas dos repositórios
   - matplotlib: para suporte à renderização e salvamento dos gráficos

## Funcionalidades

- Consulta automática aos 100 repositórios mais populares do GitHub (ordenados por estrelas).
- Utilização da API GraphQL para coletar informações detalhadas.
- Requisições automáticas com tolerância a erros temporários (retries para status 502, 503 e 504).
- Cálculo da razão de issues fechadas em relação ao total de issues.

## API Utilizada

Foi utilizada a GitHub API para coletar os dados necessários dos repositórios. Mais detalhes sobre a API podem ser encontrados na documentação do GitHub REST API.

- [GitHub REST API Documentation](https://docs.github.com/pt/rest?apiVersion=2022-11-28)

## Metodologia

### 1. Escopo

- Coletar dados dos 1000 repositórios públicos mais populares, ordenados pelo número de estrelas.
- O critério de popularidade foi definido pela contagem de estrelas (stargazerCount).

### 2. Coleta de dados: 

A coleta de dados foi realizada utilizando a API do GitHub para obter informações detalhadas dos 1000 repositórios públicos mais populares, ordenados pelo número de estrelas. Como critério do experimento, foram considerados apenas os repositórios públicos com pelo menos uma estrela. Repositórios privados ou com menos relevância em termos de popularidade não foram incluídos na análise.

### 3. Implementação da Coleta

- Linguagem de consulta: Foi utilizado o GraphQL para consultas sob medida, evitando overfetching ou underfetching de informações. Essa abordagem também reduz o número de requisições, oferece paginação mais eficiente e diminui a carga tanto na API quanto no script de coleta.
- Paginação: Foram utilizadas funções para lidar com paginação, permitindo obter resultados em lotes de 100 repositórios por requisição e garantindo maior estabilidade da coleta devido ao grande número de repositórios consultados, mantendo maior controle do progresso e respeitando os limites de requisição da API.
- Cálculo de Issues: Foi utilizado um método para calcular a razão de issues fechadas em relação ao total de issues do repositório, obtida dividindo-se o número de issues fechadas pelo número total de issues (abertas + fechadas). Essa métrica fornece uma indicação da eficiência de resolução de problemas e do nível de manutenção do projeto, permitindo comparar a capacidade de gerenciamento de issues entre repositórios populares.
- Ordenação dos resultados: A query de busca retorna os repositórios em ordem decrescente de estrelas, salvando no CSV sem aplicar nenhuma ordenação adicional, sendo essa determinada pela própria API do GitHub.
- Tolerância a falhas: Foi implementado um mecanismo básico de tolerância a falhas, onde são disparadas requisições automáticas com tolerância a erros temporários (mas limitado a erros temporários da API), incluindo retries para os status 502, 503 e 504.

3. Métricas Coletadas

Para cada repositório, foram obtidas as seguintes métricas:

- Número de estrelas (stargazerCount)
- Dono/proprietário do repositório
- Data de criação e última atualização
- Linguagem primária do projeto
- Número de releases
- Número de issues abertas e fechadas
- Razão de issues fechadas sobre o total
- Número de pull requests mesclados

4. Análise Gráfica

Para explorar os dados coletados e responder às questões de pesquisa (RQs), foram criados gráficos utilizando Python com a biblioteca Seaborn, incluindo:

- Violin Plot: Distribuição da idade dos repositórios e percentual de issues fechadas.
- Histograma (histplot): Distribuição de tempo desde a última atualização dos repositórios.
- Scatter Plot: Relação entre estrelas e número de releases, e entre estrelas e pull requests aceitas.
- Swarmplot: Distribuição das linguagens primárias dos repositórios populares.
- Heatmap: Correlação entre todas as métricas coletadas para identificar padrões e relações.

Cada gráfico foi salvo em arquivo PNG para posterior análise e interpretação dos resultados.

5. Execução e Validação

- O script foi implementado em Python e os dados coletados foram salvos em um arquivo CSV (repos_data.csv) para posterior análise.
- O tempo total de execução foi registrado para avaliação de desempenho do processo de coleta e análise.
- Todos os dados e gráficos foram revisados para garantir consistência, completude e confiabilidade nas interpretações.

## URL da API

A busca foi realizada através do seguinte endpoint da API do GitHub:



## Hipóteses Informais para as Questões de Pesquisa

A seguir, são apresentadas as **questões de pesquisa (RQs)** e as respectivas **hipóteses informais** que orientarão a análise dos dados:

- **RQ 01. Sistemas populares são maduros/antigos?**

  - **Hipótese Informal:** Espera-se que **sistemas populares sejam maduros/antigos**, pois a longevidade geralmente contribui para a sua popularidade e estabilidade. Um projeto com mais tempo de existência tende a ter mais funcionalidades, uma base de usuários estabelecida e maior confiança na comunidade.

- **RQ 02. Sistemas populares recebem muita contribuição externa?**

  - **Hipótese Informal:** Espera-se que **sistemas populares recebam um alto volume de contribuições externas** (medido pelo total de _pull requests_ aceitas), indicando uma comunidade ativa e engajada que impulsiona o desenvolvimento e a melhoria contínua do projeto.

- **RQ 03. Sistemas populares lançam _releases_ com frequência?**

  - **Hipótese Informal:** Espera-se que **sistemas populares lancem _releases_ com frequência**, demonstrando um desenvolvimento contínuo e a entrega regular de novas funcionalidades, correções de bugs ou melhorias aos usuários. Isso sinaliza um projeto ativo e bem mantido.

- **RQ 04. Sistemas populares são atualizados com frequência?**

  - **Hipótese Informal:** Espera-se que **sistemas populares sejam atualizados com muita frequência**, o que é crucial para manter a relevância, segurança, compatibilidade com novas tecnologias e para atender às demandas dos usuários e do ecossistema.

- **RQ 05. Sistemas populares são escritos nas linguagens mais populares?**

  - **Hipótese Informal:** Espera-se que **sistemas populares sejam majoritariamente escritos nas linguagens de programação mais populares**, o que facilita a contribuição de uma base maior de desenvolvedores e a adoção por um público mais amplo, dado que essas linguagens possuem mais ferramentas, documentação e suporte.

- **RQ 06. Sistemas populares possuem um alto percentual de _issues_ fechadas?**
  - **Hipótese Informal:** Espera-se que **sistemas populares possuam um alto percentual de _issues_ fechadas**, refletindo a eficiência da equipe de desenvolvimento em resolver problemas, responder às necessidades dos usuários e manter a qualidade do projeto. Um bom gerenciamento de _issues_ é um indicativo de maturidade do projeto.

---

## Metodologia PROFESSOR

- **Coleta de dados:** Foi utilizada a GitHub API para obter informações detalhadas dos repositórios que incluem a palavra-chave "microservices" em seus tópicos ou descrições. Como restrição do experimento, a coleta não inclui repositórios que implementam microsserviços, mas que não mencionam explicitamente a palavra-chave microservices em nenhum lugar.
- **Filtragem e paginação:** A coleta de dados envolveu a utilização da paginação da API do GitHub devido ao grande número de informações nos repositórios mais relevantes. Esse processo pode levar em média 30 minutos para terminar devido à necessidade de lidar com múltiplas requisições e alto volume de dados.
- **Normalização de dados:** Os dados foram normalizados usando a técnica de min-max scaling, garantindo que todos os valores estivessem na mesma escala para o cálculo da pontuação composta.
- **Cálculo da pontuação composta:** Foi utilizado um método de combinação linear ponderada (scores) para calcular uma pontuação composta para cada repositório, levando em consideração tanto as estrelas quanto os forks.
- **Ordenação dos Repositórios:** Os repositórios foram ordenados em ordem decrescente com base na pontuação composta calculada.

## Busca de repositórios no GitHub com a palavra-chave "microservices"

Esta funcionalidade utiliza a API do GitHub para buscar repositórios que tenham relação com a palavra-chave `microservices`. A busca é feita de acordo com diferentes critérios, como nome do repositório, descrição, README, e tópicos associados. Abaixo estão os detalhes de como cada critério é utilizado:

### URL da API

A busca é realizada através do seguinte endpoint da API do GitHub:

https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page={num_repos}

- **keyword**: palavra-chave usada na busca (neste caso, `"microservices"`).
- **num_repos**: número de repositórios a serem retornados.

### Critérios de busca

1. **Nome do repositório**:

   - Repositórios cujo nome contém a palavra-chave `microservices`.

2. **Descrição do repositório**:

   - Repositórios cuja descrição menciona a palavra-chave `microservices`.

3. **README**:

   - Repositórios cujo arquivo `README` contém a palavra-chave `microservices`.

4. **Tópicos do repositório**:
   - Repositórios que possuem tópicos (tags) associadas que contêm a palavra-chave `microservices`.

## Análise

## Resultados Encontrados

### Tempo Médio de Execução

Devido à paginação dos resultados retornados pela API do GitHub, o script tem um tempo médio de execução de aproximadamente **12 minutos**.  
Esse tempo pode variar conforme o número de repositórios processados e o limite de resultados por página.

---

### Estrutura do Arquivo CSV

O arquivo **repos_data.csv** gerado pelo script contém as seguintes colunas:

- **name**: Nome do repositório.
- **stars**: Número de estrelas recebidas.
- **language**: Linguagem de programação principal utilizada.
- **releases**: Número de releases publicadas.
- **open_issues**: Número de issues abertas.
- **closed_issues**: Número de issues fechadas.
- **merged_prs**: Número de pull requests mesclados.
- **created_at**: Data de criação do repositório.
- **updated_at**: Data da última atualização do repositório.

---

### Exemplo de Dados

| name           | stars | language   | releases | open_issues | closed_issues | merged_prs | created_at          | updated_at          |
| -------------- | ----- | ---------- | -------- | ----------- | ------------- | ---------- | ------------------- | ------------------- |
| example-repo-1 | 1500  | Python     | 10       | 5           | 50            | 20         | 2020-01-01T12:00:00 | 2025-08-29T12:00:00 |
| example-repo-2 | 1200  | JavaScript | 8        | 3           | 30            | 15         | 2019-05-15T12:00:00 | 2025-08-28T12:00:00 |

---

Esses dados podem ser utilizados para **análise estatística**, **visualização de tendências** e **comparação** entre repositórios populares no GitHub.

## Conclusão

Este experimento demonstrou a viabilidade de coletar e analisar dados de repositórios populares no GitHub que implementam microsserviços. A metodologia utilizada permitiu identificar e ranquear os principais repositórios com base em critérios objetivos como estrelas e forks, apesar da limitação de apenas considerar repositórios que explicitamente mencionam "microservices" em seus metadados. O algoritmo de ranqueamento leva em média 30 minutos para rodar devido à necessidade de lidar com a paginação da API do GitHub, enquanto o algoritmo de cálculos estatísticos é instantâneo, pois os repositórios são fixos no código.
