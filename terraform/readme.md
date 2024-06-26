#Data Lake

## 📓 Pré-Requisitos

- Python/pip, PyEnv, Pipx, Poetry
- Azure CLI ( Use esse site para baixar o Azure Cli: [Download Azure CLI](https://learn.microsoft.com/pt-br/cli/azure/install-azure-cli-windows?tabs=azure-cli) )
- Visual Studio Code
- Terraform ( Siga os passos desse [Tutorial no youtube](https://www.youtube.com/watch?v=g6llmNxrutc) para realizar a instalação do terraform de forma correta)
- Microsoft Learning account (assinatura sandbox)
- [Databricks Community](https://community.databricks.com/)

## 👣 Passos

##### 1. Ative uma assinatura de teste
[MS Learn Sandbox (Restrict Area)](https://learn.microsoft.com/pt-br/training/modules/develop-test-deploy-azure-functions-with-core-tools/5-exercise-publish-function-core-tools?ns-enrollment-type=learningpath&ns-enrollment-id=learn.create-serverless-applications) - Limite de 4 horas!

##### 2. Azure CLI
Antes de começar esse passo a passo, é necessario clonar o projeto contendo os arquivos .tf e abrir o VScode.

###### 2.1 Login
```
az login <- Ele vai pedir para selecinar a assinatura desejada, só digitar "1" e "Enter".
```

###### 2.2 Obter o nome do grupo de recursos da conta da Assinatura Concierge
```
az group list -o table
```

###### 2.3 Ajustar variables.tf com o resultado do passo anterior
```
variable "resource_group_name" {
  default = "learn-6645ede3-dbe7-406c-b6b7-68539495cbf4" <- Coloque a assinatura que foi gerada através do passo anterior aqui dentro no Vscode.
}
```

##### 3. Criar recursos no Azure
###### 3.1 Iniciar o Terraform
```
terraform init
```

###### 3.2 Validar o código nos arquivos .tf
```
terraform validate
```

###### 3.3 Ajustar a formatação nos arquivos .tf
```
terraform fmt
```

###### 3.4 Criar um plano de execução
```
terraform plan
```

###### 3.5 Aplicar o Terraform na nuvem
```
terraform apply
```

##### 4. Verificar o deploy do ADLS e do SQL Server
```
Faça login em [portal.azure.com](https://portal.azure.com/) e verifique o ADLS e o SQL Server criado.
```

###### 4.1 Aplicar o Terraform na nuvem
Liberar IP no firewall do SQL Server nas configurações de rede
