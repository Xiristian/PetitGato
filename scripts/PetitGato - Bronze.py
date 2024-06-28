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
# MAGIC ###Mostrando os pontos de montagem no cluster Databricks

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Definindo uma função para montar um ADLS com um ponto de montagem com ADLS SAS 

# COMMAND ----------

storageAccountName = "datalake15b08d56c4920f36"
sasToken = "sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupyx&se=2024-06-29T04:47:37Z&st=2024-06-28T20:47:37Z&spr=https&sig=3759nFSMPBdjIy2lOKOUDv1jGXRaPt%2FRtIEnshqFsFk%3D"

def mount_adls(blobContainerName):
    try:
      dbutils.fs.mount(
        source = "wasbs://{}@{}.blob.core.windows.net".format(blobContainerName, storageAccountName),
        mount_point = f"/mnt/{storageAccountName}/{blobContainerName}",
        extra_configs = {'fs.azure.sas.' + blobContainerName + '.' + storageAccountName + '.blob.core.windows.net': sasToken}
      )
      print("OK!")
    except Exception as e:
      print("Falha", e)

# COMMAND ----------

# MAGIC %md
# MAGIC ###Montando todos os containers

# COMMAND ----------

mount_adls('landing-zone')
mount_adls('bronze')
mount_adls('silver')
mount_adls('gold')

# COMMAND ----------

# MAGIC %md
# MAGIC ###Mostrando os pontos de montagem no cluster Databricks

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mostrando todos os arquivos da camada landing-zone

# COMMAND ----------

display(dbutils.fs.ls(f"/mnt/{storageAccountName}/landing-zone/petitgato/"))

# COMMAND ----------

# MAGIC %md
# MAGIC ###Gerando um dataframe para cada arquivo a partir dos arquivos CSV gravado no container landing-zone do Azure Data Lake Storage

# COMMAND ----------

df_customerorder = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/customerorder.csv")
df_orderitem     = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/orderitem.csv")
df_item          = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/item.csv")
df_customer      = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/customer.csv")
df_category      = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/category.csv")
df_coffeetable   = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/coffeetable.csv")
df_payment       = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/payment.csv")
df_cat           = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/cat.csv")
df_customercat   = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/petitgato/cat_customer.csv")


# COMMAND ----------

# MAGIC %md
# MAGIC ### Adicionando metadados de data e hora de processamento e nome do arquivo de origem

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_customerorder = df_customerorder.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("customerorder.csv"))
df_orderitem     = df_orderitem.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("orderitem.csv"))
df_item          = df_item.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("item.csv"))
df_customer      = df_customer.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("customer.csv"))
df_category      = df_category.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("category.csv"))
df_coffeetable   = df_coffeetable.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("coffeetable.csv"))
df_payment       = df_payment.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("payment.csv"))
df_cat           = df_cat.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("cat.csv"))
df_customercat   = df_customercat.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("cat_customer.csv"))


# COMMAND ----------

# MAGIC %md
# MAGIC ###Salvando os dataframes em delta lake (formato de arquivo) no data lake (repositorio cloud)

# COMMAND ----------

df_customerorder.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/customerorder")
df_orderitem.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/orderitem")
df_item.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/item")
df_customer.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/customer")
df_category.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/category")
df_coffeetable.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/coffeetable")
df_payment.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/payment")
df_cat.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/cat")
df_customercat.write.format('delta').save(f"/mnt/{storageAccountName}/bronze/customercat")

# COMMAND ----------

# MAGIC %md
# MAGIC ###Verificando os dados gravados em delta na camada bronze

# COMMAND ----------

display(dbutils.fs.ls(f"/mnt/{storageAccountName}/bronze/"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Lendo um exemplo de um delta lake para validar a existencia dos dados e das colunas do metadados

# COMMAND ----------

spark.read.format('delta').load(f'/mnt/{storageAccountName}/bronze/cat').limit(10).display()
