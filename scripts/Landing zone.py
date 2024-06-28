# Databricks notebook source
# MAGIC %pip install azure-storage-file-datalake

# COMMAND ----------

import pyodbc
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError
from urllib.parse import quote_plus
import numpy as np

# Configurações do Azure Data Lake Storage
account_name = 'datalaked6291d8aa88d6e0a'
file_system_name = 'landing-zone'
sas_token = 'sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupyx&se=2024-06-28T20:49:53Z&st=2024-06-28T12:49:53Z&spr=https&sig=mHQ7cNB8mifX8NLy8tgW%2B3YA6NNGXPTb2hWB%2BVZufpk%3D'

# Configurações do SQL Server
server = 'petit-gato.database.windows.net'
schema = 'dbo'
username = 'petit-gato'
password = 'c4puRRc!n0'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE=petitgato;UID={username};PWD={password}'

def fetch_data_as_dataframe(cursor, query):
    cursor.execute(query)
    data = cursor.fetchall()
    columns = []
    for i,_ in enumerate(cursor.description):
        columns.append(cursor.description[i][0])
    if data.__len__() == 0:
        return pd.DataFrame()
    df = pd.DataFrame(np.array(data), columns = columns)
    return df

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

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
    # Consulta SQL para obter todas as tabelas do esquema
    query = f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '{schema}'"
    tables_df = fetch_data_as_dataframe(cursor, query)

    # Para cada tabela encontrada, ler os dados e carregar para o Azure Data Lake Storage
    for index, row in tables_df.iterrows():
        table_name = row["table_name"]
        query = f"SELECT * FROM {schema}.{table_name}"
        df = fetch_data_as_dataframe(cursor, query)
        # Carregar os dados para o Azure Data Lake Storage
        file_client = directory_client.get_file_client(f"{table_name}.csv")
        data = df.to_csv(index=False).encode()
        file_client.upload_data(data, overwrite=True)
        print(f"Dados da tabela '{table_name}' carregados com sucesso.")

    conn.commit()
except pyodbc.Error as ex:
    print(f"Erro ao conectar ao SQL Server: {ex}")
finally:
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except pyodbc.Error as ex:
        print(f"Erro ao fechar a conexão: {ex}")


