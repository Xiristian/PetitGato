## 📓 Pré-Requisitos

- Python/pip, PyEnv, Pipx, Poetry
- Seguir passos do seguinte [README.MD](../terraform/readme.md)

## 👣 Passos

#### Baixar e instalar pyenv

```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
& "./install-pyenv-win.ps1"
```

#### Instalar pipx

```bash
pip install pipx
```

#### Adicionar pipx ao PATH

```bash
pipx ensurepath
```

#### Instalar poetry usando pipx

```bash
pipx install poetry
```

#### Navegar até o diretório do projeto

```bash
cd petit-gato
```

#### Copiar o arquivo de exemplo .env

```bash
copy .env.example .env
```

#### Instalar as dependências do projeto com poetry

```bash
poetry install
```

#### Executar os scripts

```bash
poetry run python gerar_dados.py
poetry run python criar_landing_zone.py
```

##### 4. Verificar os dados

- Faça login em [portal.azure.com](https://portal.azure.com/) e verifique na landing zone do ADLS se os CSVs foram criados.
