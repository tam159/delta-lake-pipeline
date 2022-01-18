"""Vacuum all Delta tables."""

from delta.tables import DeltaTable
from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession

spark = SparkSession.builder.config("spark.files.overwrite", "true").getOrCreate()

dbutils = DBUtils(spark)
libs_paths = [libs_file[0] for libs_file in dbutils.fs.ls("dbfs:/spark_libs")]

sc = spark.sparkContext
sc.addPyFile(sorted(libs_paths)[-1])

from base_spark import BaseSpark
from data_config import DATA_FILES_RETENTION_HOURS
from log_util import get_logger

logger = get_logger()

if __name__ == "__main__":
    base_spark = BaseSpark(spark)
    for table in base_spark.get_catalog_tables:
        DeltaTable.forName(spark, table).vacuum(
            retentionHours=DATA_FILES_RETENTION_HOURS
        )

        logger.info(f"{table} vacuum completed")
