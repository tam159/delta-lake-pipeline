"""Base Spark methods."""

from typing import List, Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType


class BaseSpark:
    """
    Base Spark methods.

    :param spark: SparkSession
    """

    def __init__(self, spark: SparkSession):
        self.spark = spark

    @property
    def get_catalog_tables(self) -> List[str]:
        """
        Get all catalog tables names.

        :return: List of tables names
        """
        return [
            f"{db.name}.{table.name}"
            for db in self.spark.catalog.listDatabases()
            for table in self.spark.catalog.listTables(db.name)
        ]

    def get_column_schema(
        self,
        dataframe: DataFrame,
        column_name: str,
        order_column: str,
        limit_number: Optional[int] = None,
    ) -> StructType:
        """
        Get schema from a json column.

        :param dataframe: DataFrame
        :param column_name: column name
        :param order_column: order by column name
        :param limit_number: limit number with descending
        :return: schema of the column
        """
        if limit_number:
            schema = self.spark.read.json(
                dataframe.filter(col(column_name).isNotNull())
                .orderBy(col(order_column).desc())
                .limit(limit_number)
                .select(column_name)
                .rdd.map(lambda x: x[0])
            ).schema
        else:
            schema = self.spark.read.json(
                dataframe.filter(col(column_name).isNotNull())
                .orderBy(col(order_column).desc())
                .select(column_name)
                .rdd.map(lambda x: x[0])
            ).schema

        return schema

    def convert_json_column_to_struct(
        self,
        dataframe: DataFrame,
        raw_df: DataFrame,
        column_name: str,
        order_column: str,
        limit_number: Optional[int] = None,
    ) -> DataFrame:
        """
        Convert a json column to the struct one in DataFrame.

        :param dataframe: DataFrame
        :param raw_df: raw table dataframe
        :param column_name: column name
        :param order_column: order by column name
        :param limit_number: limit number with descending
        :return: DataFrame with converted column type
        """
        return dataframe.withColumn(
            column_name,
            from_json(
                column_name,
                self.get_column_schema(raw_df, column_name, order_column, limit_number),
            ),
        )
