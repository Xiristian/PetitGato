# Databricks notebook source
# MAGIC %md
# MAGIC ##Validando a SparkSession

# COMMAND ----------

spark

# COMMAND ----------

# MAGIC %md
# MAGIC ##Conectando Azure ADLS Gen2 no Databricks

# COMMAND ----------

# MAGIC %md
# MAGIC ### Definindo uma função para montar um ADLS com um ponto de montagem com ADLS SAS 

# COMMAND ----------

storageAccountName = "datalake271297fb88ef6733"
sasToken = "sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupyx&se=2024-06-29T00:29:26Z&st=2024-06-28T16:29:26Z&spr=https&sig=NPxuYKGVwZPiye%2FpKprMavdDoJLyIFt5WfkJE40TNFE%3D"

# COMMAND ----------

# MAGIC %md
# MAGIC ###Mostrando os pontos de montagem no cluster Databricks

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mostrando todos os arquivos da camada bronze

# COMMAND ----------

display(dbutils.fs.ls(f"/mnt/{storageAccountName}/bronze"))

# COMMAND ----------

# MAGIC %md
# MAGIC ###Gerando um dataframe dos delta lake no container bronze do Azure Data Lake Storage

# COMMAND ----------

df_customerorder = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/customerorder")
df_orderitem     = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/orderitem")
df_item          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/item")
df_customer      = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/customer")
df_category      = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/category")
df_coffeetable   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/coffeetable")
df_payment       = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/payment")
df_cat           = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/cat")
df_customercat   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/customercat")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Adicionando metadados de data e hora de processamento e nome do arquivo de origem

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_customerorder = df_customerorder.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("customerorder"))
df_orderitem     = df_orderitem.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("orderitem"))
df_item          = df_item.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("item"))
df_customer      = df_customer.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("customer"))
df_category      = df_category.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("category"))
df_coffeetable   = df_coffeetable.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("coffeetable"))
df_payment       = df_payment.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("payment"))
df_cat           = df_cat.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("cat"))
df_customercat   = df_customercat.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("customercat"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fazer as transformacoes de forma massiva

# COMMAND ----------

def renomear_colunas(diretorio):
    df = spark.read.format('delta').load(diretorio)
    tabela = diretorio.split('/')[-2]

    for coluna in df.columns:
        novo_nome = coluna.upper()
        novo_nome = novo_nome.replace("ID", "CODIGO")
        novo_nome = novo_nome.replace("ORDER", "PEDIDO")
        novo_nome = novo_nome.replace("PRICE", "VALOR")
        novo_nome = novo_nome.replace("TABLE", "MESA")
        novo_nome = novo_nome.replace("VALUE", "VALOR")
        novo_nome = novo_nome.replace("COST", "CUSTO")
        novo_nome = novo_nome.replace("ADOPTION_DATE", "DATA_ADOCAO")
        novo_nome = novo_nome.replace("DATE", "DATA")
        novo_nome = novo_nome.replace("CUSTOMER", "CLIENTE")
        novo_nome = novo_nome.replace("PAYMENT", "PAGAMENTO")
        novo_nome = novo_nome.replace("NAME", "NOME")
        novo_nome = novo_nome.replace("PHONE", "TELEFONE")
        novo_nome = novo_nome.replace("CATEGORY", "CATEGORIA")
        novo_nome = novo_nome.replace("DESCRIPTION", "DESCRICAO")
        novo_nome = novo_nome.replace("ACTIVE", "ATIVO")
        novo_nome = novo_nome.replace("OCUPPIED", "OCUPADA")
        novo_nome = novo_nome.replace("QUANTITY", "QUANTIDADE")
        novo_nome = novo_nome.replace("OPENED", "ABERTO")
        novo_nome = novo_nome.replace("CAT", "GATO")
        novo_nome = novo_nome.replace("AGE", "IDADE")

        if "CODIGO" in novo_nome:
            novo_nome = novo_nome.removesuffix("CODIGO")
            novo_nome = f"CODIGO_{novo_nome}"
        
        df = df.withColumnRenamed(coluna, novo_nome)
        df = df.drop("DATA_HORA_BRONZE")
        df = df.drop("NOME_ARQUIVO")
        df = df.withColumn("NOME_ARQUIVO_BRONZE", lit(tabela))
        df = df.withColumn("DATA_ARQUIVO_SILVER", current_timestamp())

    df.write.format('delta').save(f"/mnt/{storageAccountName}/silver/{tabela}")

def renomear_arquivos_delta(diretorio):
    nomes_arquivos_delta = []
    arquivos = dbutils.fs.ls(diretorio)
    for arquivo in arquivos:
        nome_arquivo = arquivo.path
        renomear_colunas(nome_arquivo)

    return nomes_arquivos_delta

# COMMAND ----------

diretorio = f'/mnt/{storageAccountName}/bronze'
renomear_arquivos_delta(diretorio)

# COMMAND ----------

spark.read.format('delta').load(f'/mnt/{storageAccountName}/silver/item').limit(10).display()
