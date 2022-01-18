# Databricks notebook source
dbutils.help()

# COMMAND ----------

dbutils.fs.help()

# COMMAND ----------

dbutils.notebook.help()

# COMMAND ----------

dbutils.widgets.help()

# COMMAND ----------

dbutils.secrets.help()

# COMMAND ----------

raw_bucket_name = "delta-lake-raw-dev"
raw_mount_name = "raw"
dbutils.fs.mount("s3a://%s" % raw_bucket_name, "/mnt/%s" % raw_mount_name)

# COMMAND ----------

refined_bucket_name = "delta-lake-refined-dev"
refined_mount_name = "refined"
dbutils.fs.mount("s3a://%s" % refined_bucket_name, "/mnt/%s" % refined_mount_name)

# COMMAND ----------

curated_bucket_name = "delta-lake-curated-dev"
curated_mount_name = "curated"
dbutils.fs.mount("s3a://%s" % curated_bucket_name, "/mnt/%s" % curated_mount_name)

# COMMAND ----------

dbutils.fs.refreshMounts()

# COMMAND ----------

display(dbutils.fs.ls("/mnt/raw"))

# COMMAND ----------

display(dbutils.fs.ls("/mnt/refined"))

# COMMAND ----------

display(dbutils.fs.ls("/mnt/curated"))

# COMMAND ----------
