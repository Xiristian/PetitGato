from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Azure Data Lake Storage
account_name = os.getenv("ADLS_ACCOUNT_NAME")
file_system_name = os.getenv("ADLS_FILE_SYSTEM_NAME")
directory_name = os.getenv("ADLS_DIRECTORY_NAME")
sas_token = os.getenv("ADLS_SAS_TOKEN")

# Criar cliente do Azure Data Lake Storage
file_system_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", 
                                           credential=sas_token,
                                           api_version="2020-02-10")

# Tentar criar o diretório, se não existir
try:
    directory_client = file_system_client.get_file_system_client(file_system_name).get_directory_client(directory_name)
    directory_client.create_directory()
except ResourceExistsError:
    print(f"O diretório '{directory_name}' já existe.")