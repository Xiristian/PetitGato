# PetitGato

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

O PetitGato é um sistema desenvolvido para gerenciar uma cafeteria temática com gatos. A cafeteria permite que os clientes desfrutem de uma boa xícara de café enquanto interagem com gatos. Este documento fornece uma visão geral do projeto, seus objetivos e suas principais funcionalidades.

![logo (1)](https://github.com/Xiristian/PetitGato/assets/127258498/9a7d6215-8dd4-43d8-835c-a1a60ad43b07)


## Documentação

As instruções contidas na [Documentação do Mkdocs](https://xiristian.github.io/PetitGato/) permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.


## Desenho de Arquitetura

![image](https://github.com/Xiristian/PetitGato/assets/127258498/78f6e7a5-6666-4865-921a-61c46453982a)


## Ferramentas utilizadas

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


## Autores

*  *Scripts de criação das tabelas e população* - [Ana Carolina Machado](https://github.com/anacarolina1002)
*  *Aquivo Power BI para criação dos Dashboards e criação do modelo da camada Gold* - [Bruna Peruch](https://github.com/brupperuch)
*  *Integração de todas as partes* - [Christian Hederson Cypriano](https://github.com/Xiristian)
*  *Configuração Data Lake e SQLs KPI* - [Guilherme Pizzollo](https://github.com/guilhermebp030504)
*  *Documentação Mkdocs e README* - [Julia De Luca](https://github.com/judwluca)
*  *Documentação Mkdocs* - [Luz Brenda Oliveira](https://github.com/luzbrendaoliv)
*  *Configuração dos Scripts de população da Gold e montagem das KPIs* - [Rafael Rodrigues](https://github.com/Rafael171022)
*  *Configuração Ambiente Data Lake* - [Wallace Mendes](https://github.com/WallaceB2)

Você também pode consultar todos os colaboradores [aqui](https://github.com/Xiristian/PetitGato/graphs/contributors). 


## Referências

[CHATGPT](https://chatgpt.com/)
[Documentação - Faker](https://faker.readthedocs.io/en/master/)
[Repositório - Faker](https://github.com/joke2k/faker)
[Datastore Classe](https://learn.microsoft.com/pt-br/python/api/azureml-core/azureml.core.datastore.datastore?view=azure-ml-py)
[Proof of concept connecting to SQL using pyodbc](https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16)
[Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html)
