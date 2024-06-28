# Ferramentas utilizadas

Ferramentas que foram essenciais para a realização do projeto: 

* [SQL Server](https://www.microsoft.com/pt-br/sql-server) - Armazenamento de dados
* [Python](https://www.python.org/) - Criação de scripts
* [Terrafom](https://www.terraform.io/) - Gerenciamento de infraestrutura
* [Databriks](https://docs.databricks.com/en/repos/get-access-tokens-from-git-provider.html) - Ingestão de dados/Orquestração de Fluxos de Trabalho/Processamento Distribuído de Dados
* [Azure](https://azure.microsoft.com/pt-br/) - Persistência em Object Storage
* [Power BI](https://www.microsoft.com/pt-br/power-platform/products/power-bi) - Visualização e Análise dos Dados Processados
* [MkDocs](https://www.mkdocs.org/) - Documentação

## Aplicação

__1. Gerenciamento de Fluxo de Trabalho com Databricks Airflow:__

* O Databricks Airflow é nossa plataforma principal para gerenciamento de fluxo de trabalho, orquestrando todas as tarefas dentro de nossa pipeline de dados. Ele lida com as transformações necessárias até a disponibilização dos dados em uma interface de análise.

__2. Geração de Dados Sintéticos com Faker:__

* A massa de dados será gerada utilizando a biblioteca Faker, que permite criar dados sintéticos realistas para simulações e testes.

__3. Armazenamento de Dados no SQL Server:__

* Os dados gerados serão armazenados em um banco de dados SQL Server, utilizando scripts Python para inserção e manipulação dos dados.

__4. Processamento de Dados com Spark no Databricks:__

* No Databricks, utilizamos Spark em conjunto com Airflow para ler e manipular os dados armazenados no SQL Server. Esses dados serão extraídos e transformados em arquivos CSV.

__5. Persistência de Dados no Azure Object Storage:__

* O Azure é utilizado para a persistência dos dados, armazenando-os no Object Storage, garantindo durabilidade e escalabilidade.

__6. Camadas de Dados:__

* Landing Zone:
  - Nesta camada, os dados serão extraídos do SQL Server e persistidos em seu formato bruto, em arquivos CSV.
* Camada Bronze:
  - Os dados serão extraídos da Landing Zone, e colunas de metadados serão adicionadas. As alterações serão persistidas na camada Bronze, utilizando o formato Parquet.
* Camada Silver:
  - Os dados da camada Bronze serão extraídos, e novas colunas de metadados serão criadas. Os nomes das colunas serão padronizados e traduzidos. As alterações serão salvas na camada Silver, também no formato Parquet.
* Camada Gold:
  - Nesta camada, serão criadas as tabelas de dimensões e fatos, otimizadas para análise e relatórios.

__7. Visualização de Dados com Power BI:__

* O Power BI será utilizado para a apresentação dos dados, permitindo a criação de dashboards interativos para análise e tomada de decisão.