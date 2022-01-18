"""Process raw events to refined data."""

import argparse
from typing import Optional

from delta_lake_library.spark_io import SparkIO
from pyspark.dbutils import DBUtils
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json, to_date

spark = SparkSession.builder.config("spark.files.overwrite", "true").getOrCreate()

dbutils = DBUtils(spark)
libs_paths = [libs_file[0] for libs_file in dbutils.fs.ls("dbfs:/spark_libs")]

sc = spark.sparkContext
sc.addPyFile(sorted(libs_paths)[-1])

from base_transformation import BaseTransformation
from data_config import CDF_COLUMNS, KAFKA_TOPIC_COLUMNS
from schemas.raw_event import transaction_schema

spark_io = SparkIO(spark)

parser = argparse.ArgumentParser()
parser.add_argument("--table_name", help="table name")

args = parser.parse_args()
table_name = args.table_name


class RawEventExtraction:
    """
    Raw event extraction.

    :param dataframe: event dataframe
    """

    def __init__(self, dataframe: DataFrame):
        self.dataframe = dataframe

    def _extract_transaction(self) -> DataFrame:
        """
        Extract transaction nested json data.

        :return: event with extracted data
        """
        return (
            self.dataframe.select(
                "*",
                from_json("data", transaction_schema).alias(
                    "extracted_data"
                ),
            )
            .select("*", "extracted_data.*")
            .withColumn("transaction_date", to_date(col("transaction.createdDate")))
            .drop("data", "extracted_data")
        )

    def extract_event(self, table_name: str) -> Optional[DataFrame]:
        """
        Extract event nested json data.

        :param table_name: table name
        return: dataframe with extracted data
        """
        cases = {
            "transaction": self._extract_transaction,
        }

        extracted_df = cases.get(table_name, lambda: None)()

        return extracted_df


if __name__ == "__main__":
    df = spark_io.read_stream_cdf(table_name=f"raw.{table_name}")

    renamed_kafka_df = BaseTransformation.add_column_prefix(
        dataframe=df, columns=KAFKA_TOPIC_COLUMNS, prefix="_kafka_"
    )
    renamed_cdf_df = BaseTransformation.add_column_prefix(
        dataframe=renamed_kafka_df, columns=CDF_COLUMNS, prefix="_raw"
    )

    refined_df = RawEventExtraction(renamed_cdf_df).extract_event(table_name=table_name)

    flattened_refined_df = BaseTransformation.flatten_df(dataframe=refined_df)
    final_refined_df = BaseTransformation.convert_empty_string_to_null(
        dataframe=flattened_refined_df
    )

    spark_io.write_stream(
        dataframe=final_refined_df,
        table_name=f"refined.{table_name}",
        checkpoint_location=f"/mnt/refined/checkpoint/{table_name}",
    )
