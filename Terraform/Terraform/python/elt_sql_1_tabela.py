import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError
from urllib.parse import quote_plus

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do SQL Server
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
schema = os.getenv("SQL_SCHEMA", "dbo")  # Se o schema não estiver definido, usar "dbo" por padrão
table_name = os.getenv("SQL_TABLE_NAME")
username = os.getenv("SQL_USERNAME")

# Obter a senha como string
password = os.getenv("SQL_PASSWORD")

# Se a senha estiver como bytes, decodificar para string
if isinstance(password, bytes):
    password = password.decode()

# Codificar a senha usando quote_plus se necessário
password_quoted = quote_plus(password) if password else ""

# Configurações do Azure Data Lake Storage
account_name = os.getenv("ADLS_ACCOUNT_NAME")
file_system_name = os.getenv("ADLS_FILE_SYSTEM_NAME")
directory_name = database  # Usando o nome do banco de dados como diretório
sas_token = os.getenv("ADLS_SAS_TOKEN")

# Consulta SQL
query = f"SELECT * FROM {schema}.{table_name}"

# Conectar ao SQL Server e ler os dados
conn_str = f"mssql+pyodbc://{username}:{password_quoted}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
df = pd.read_sql(query, conn_str)

# Escrever os dados no Azure Data Lake Storage
file_system_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", 
                                           credential=sas_token)

# Tentar criar o diretório, se não existir
try:
    file_system_client.create_file_system(file_system_name)
    print(f"O sistema de arquivos '{file_system_name}' foi criado.")
except ResourceExistsError:
    print(f"O sistema de arquivos '{file_system_name}' já existe.")

# Criar o diretório dentro do sistema de arquivos
directory_client = file_system_client.get_file_system_client(file_system_name).get_directory_client(directory_name)
directory_client.create_directory()

# Carregar o arquivo para o Azure Data Lake Storage
file_client = directory_client.get_file_client(f"{table_name}.csv")

# Converter DataFrame para CSV e obter os dados como bytes
data = df.to_csv(index=False).encode()

# Carregar os dados
file_client.upload_data(data, overwrite=True)

print(f"Dados carregados com sucesso para '{directory_name}/{table_name}.csv' no Azure Data Lake Storage.")
