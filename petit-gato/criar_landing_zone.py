import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError
from sqlalchemy import create_engine
from urllib.parse import quote_plus

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Azure Data Lake Storage
account_name = os.getenv("ADLS_ACCOUNT_NAME")
file_system_name = os.getenv("ADLS_FILE_SYSTEM_NAME")
sas_token = os.getenv("ADLS_SAS_TOKEN")

# Configurações do SQL Server
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
schema = os.getenv("SQL_SCHEMA")
username = os.getenv("SQL_USERNAME")
password = quote_plus(os.getenv("SQL_PASSWORD"))

# Conectar ao SQL Server
conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Criar a engine do SQLAlchemy
engine = create_engine(conn_str)

# Consulta SQL para obter todas as tabelas do esquema
query = f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '{schema}'"

# Criar cliente do Azure Data Lake Storage
file_system_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", 
                                           credential=sas_token,
                                           api_version="2020-02-10")

# Tentar criar o diretório, se não existir
try:
    directory_client = file_system_client.get_file_system_client(file_system_name).get_directory_client('petitgato')
    directory_client.create_directory()
except ResourceExistsError:
    print(f"O diretório já existe.")

# Executar a consulta para obter todas as tabelas do esquema
tables_df = pd.read_sql(query, engine)

# Para cada tabela encontrada, ler os dados e carregar para o Azure Data Lake Storage
for index, row in tables_df.iterrows():
    table_name = row["table_name"]
    query = f"SELECT * FROM {schema}.{table_name}"
    df = pd.read_sql(query, conn_str)
    
    # Carregar os dados para o Azure Data Lake Storage
    file_client = directory_client.get_file_client(f"{table_name}.csv")
    data = df.to_csv(index=False).encode()
    file_client.upload_data(data, overwrite=True)
    print(f"Dados da tabela '{table_name}' carregados com sucesso.")
