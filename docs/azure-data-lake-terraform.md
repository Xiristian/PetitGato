# Configuração do Azure Data Lake e SQL Server com Terraform

## Pré-Requisitos

Antes de começar, certifique-se de ter instalado e configurado os seguintes itens:

- [Azure CLI](https://docs.microsoft.com/pt-br/cli/azure/install-azure-cli)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- Conta Microsoft Learning (assinatura sandbox)

## Passos

### 1. Ativar uma Assinatura de Teste

Utilize a assinatura MS Learn Sandbox para limitar o tempo de uso.

### 2. Configuração da Azure CLI

Antes de iniciar, clone o projeto contendo os arquivos `.tf` e abra-o no Visual Studio Code.

#### 2.1 Login na Azure CLI

```sh
az login
```

#### 2.2 Obter o Nome do Grupo de Recursos

```sh
az group list -o table
```

#### 2.2 Obter o Nome do Grupo de Recursos

```sh
az group list -o table
```

### 3. Executar o Terraform

#### 3.1 Inicializar o Terraform

```sh
terraform init
```

#### 3.2 Validar o código nos arquivos .tf

```sh
terraform validate
```

#### 3.3 Ajustar a formatação nos arquivos .tf

```sh
terraform fmt
```

#### 3.4 Criar um plano de execução

```sh
terraform plan
```

#### 3.5 Aplicar o Terraform na nuvem

```sh
terraform apply
```

### 4. Verificar o deploy do ADLS e do SQL Server

- Faça login em [Portal Azure](https://portal.azure.com/) e verifique o ADLS e o SQL Server criado.
- Liberar IP no firewall do SQL Server nas configurações de rede









