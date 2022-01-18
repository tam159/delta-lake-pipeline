"""Streaming ingestion from Confluent Kafka."""

import argparse

from delta_lake_library.confluent_libs import SparkKafka
from delta_lake_library.helpers import StringConversion
from delta_lake_library.spark_io import SparkIO
from pyspark.sql import SparkSession

spark = SparkSession.builder.config("spark.files.overwrite", "true").getOrCreate()

spark_kafka = SparkKafka(spark)
spark_io = SparkIO(spark)

parser = argparse.ArgumentParser()
parser.add_argument("--data_type", help="data type")
parser.add_argument("--topic_name", help="topic name")

args = parser.parse_args()
topic_name = args.topic_name
data_type = args.data_type

topic_snake_case_name = StringConversion.camel_to_snake(topic_name)


if __name__ == "__main__":
    topic_df = spark_kafka.read_stream(topic_name)

    if data_type == "event":
        topic_schema = spark_kafka.get_schema(topic_name)
        topic_final_df = spark_kafka.get_structured_df(topic_df, topic_schema)
    elif data_type == "cdc":
        topic_final_df = spark_kafka.get_payload_df(topic_df)
        topic_snake_case_name = f"{data_type}_{topic_snake_case_name}"
    else:
        raise ValueError("data_type should be event or cdc")

    spark_io.write_stream(
        dataframe=topic_final_df,
        table_name=f"raw.{topic_snake_case_name}",
        checkpoint_location=f"/mnt/raw/checkpoint/{topic_snake_case_name}",
    )
