
## Ingestão de Dados:

1. **Abrir script 'Gerar dados' dentro do Databricks**
    - Navegue até o script chamado 'Gerar dados' no seu workspace do Databricks.
    - Abra o script.

2. **Executar todos os blocos**
    - Execute todos os blocos do script 'Gerar dados' para gerar os dados necessários.

3. **Abrir script 'Landing zone'**
    - Navegue até o script chamado 'Landing zone' no seu workspace do Databricks.
    - Abra o script.

4. **Configurar variáveis**
    - Configure a variável `account_name` com o nome do Data Lake criado.
    - Configure a variável `sas_token` com o token do Data Lake. Para gerar o token, siga as instruções no link:
    [Generate SAS Token](https://learn.microsoft.com/pt-br/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)

5. **Executar todos os blocos**
    - Execute todos os blocos do script 'Landing zone' para processar os dados.
