# Configuração Inicial do Projeto

## Instalação das Ferramentas

### 1. Abrir o Powershell como administrador

### 2. Instalar o Pyenv (gerenciamento de versões do Python)

```sh
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

### 3. Instala o PIPX (instala e gerencia pacotes Python globais)

```sh 
 pip install  pipx
```

### 4. Instalar o Poetry (gerencia dependências e empacotamento Python)

```sh
pipx install poetry 
```

## Reestruturação das Tabelas e Configurações Adicionais


<details>
<summary>Detalhes da Reestruturação das Tabelas</summary>

Após a instalação das ferramentas e configuração inicial do ambiente, foram realizadas as seguintes ações adicionais:

Reestruturação das Tabelas: As tabelas existentes foram modificadas para remover a tabela cache e as colunas de total do item e pedido. Foi adicionada uma nova coluna 'gato' com informações como nome, idade e data de acolhimento. Além disso, criou-se uma coluna para relacionar o gato com o cliente, incluindo informações de data de adoção.
</details>
<details >
<summary >Ferramentas Utilizadas</summary>
VSCode
Python
SQL Server
Docker
</details>