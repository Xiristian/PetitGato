#Data Lake

## 📓 Pré-Requisitos

- Docker
- SQL Server Management Studio (SSMS)
- Python/pip, PyEnv, Pipx, Poetry ( Use o [Guia do professor](https://storage.satc.edu.br/arquivos/docentes/4906/20241/files/ED/Python%20ED/Python%20para%20Engenharia%20de%20Dados.pdf) para explicação completa da instalação)
- Azure CLI ( Use esse site para baixar o Azure Cli: [Download Azure CLI](https://learn.microsoft.com/pt-br/cli/azure/install-azure-cli-windows?tabs=azure-cli) )
- Visual Studio Code
- Terraform ( Siga os passos desse [Tutorial no youtube](https://www.youtube.com/watch?v=g6llmNxrutc) para realizar a instalação do terraform de forma correta)
- Microsoft Learning account (assinatura sandbox)
- [Databricks Community](https://community.databricks.com/)

## 👣 Passos

##### 1. Configuração do Banco de Dados

###### 1.1 Criar um container Docker com SQL Server
```
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=123456789" -p 1433:1433 --name satc-sql-server --hostname satc-sql-server -d mcr.microsoft.com/mssql/server:2022-latest
```
###### 1.2 Conecte-se ao SSMS
# Credenciais
```
nome do servidor: localhost
usuário: sa
senha: 123456789
```

##### 2. Ative uma assinatura de teste
[MS Learn Sandbox (Restrict Area)](https://learn.microsoft.com/pt-br/training/modules/develop-test-deploy-azure-functions-with-core-tools/5-exercise-publish-function-core-tools?ns-enrollment-type=learningpath&ns-enrollment-id=learn.create-serverless-applications) - Limite de 4 horas!

##### 3. Azure CLI
Antes de começar esse passo a passo, é necessario clonar o projeto contendo os arquivos .tf e abrir o VScode.

###### 3.1 Login
```
az login <- Ele vai pedir para selecinar a assinatura desejada, só digitar "1" e "Enter".
```

###### 3.2 Obter o nome do grupo de recursos da conta da Assinatura Concierge
```
az group list -o table
```

###### 3.3 Ajustar variables.tf com o resultado do passo anterior
```
variable "resource_group_name" {
  default = "learn-6645ede3-dbe7-406c-b6b7-68539495cbf4" <- Coloque a assinatura que foi gerada através do passo anterior aqui dentro no Vscode.
}
```

##### 4. Criar recursos no Azure
###### 4.1 Iniciar o Terraform
```
terraform init
```

###### 4.2 Validar o código nos arquivos .tf
```
terraform validate
```

###### 4.3 Ajustar a formatação nos arquivos .tf
```
terraform fmt
```

###### 4.4 Criar um plano de execução
```
terraform plan
```

###### 4.5 Aplicar o Terraform na nuvem
```
terraform apply
```

##### 5. Verificar o deploy do ADLS
```
Faça login em [portal.azure.com](https://portal.azure.com/) e verifique o ADLS criado.
```

##### 6. Destruir recursos criados
**Cuidado:** Apenas use isso se você não quiser seguir para os próximos passos
```
terraform destroy
```

##### 7. Databricks
###### 7.1 Criar um novo Cluster
```
No item de menu **Compute**, clique em **Create compute**. Digite um nome para o seu novo cluster (não há necessidade de mais configurações).
```
###### 7.2 Importar os notebooks
```
No item de menu **Workspace**, clique em **Home**. Clique no ícone de seta e selecione **Importar**.

Individualmente, importe todos os arquivos **.dbc**.
```
###### 7.3 Execute os notebooks
```
Execute os notebooks. Os dados devem passar pelas camadas Bronze, Silver e Gold, começando na zona de pouso (Landing-zone) e aplicando todas as transformações para cada etapa.

Não se esqueça de, em cada notebook, ajustar as variáveis **storageAccountName** e **sasToken**.

No portal da azure é necessário importar um arquivo de dados como por exemplo um csv para dentro da Landing-zone.
```
