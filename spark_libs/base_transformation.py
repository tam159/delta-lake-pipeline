"""Base transformation."""

from typing import Any, List, Tuple

from pyspark.sql import Column, DataFrame
from pyspark.sql.functions import col, length, when


class BaseTransformation:
    """Spark base transformation."""

    @staticmethod
    def add_column_prefix(
        dataframe: DataFrame, columns: List[str], prefix: str
    ) -> DataFrame:
        """
        Rename columns by adding a prefix.

        :param dataframe: DataFrame
        :param columns: list of columns
        :param prefix: e.g. _, _raw, _refined
        :return: dataframe with added prefix columns
        """
        prefix_dataframe: DataFrame = dataframe

        for column in columns:
            prefix_dataframe = prefix_dataframe.withColumnRenamed(
                column, f"{prefix}{column}"
            )

        return prefix_dataframe

    @staticmethod
    def flatten_df(dataframe: DataFrame) -> DataFrame:
        """
        Flatten dataframe.

        :param dataframe: DataFrame
        :return: flattened dataframe
        """
        stack: List[Tuple[Tuple[Any, ...], DataFrame]] = [((), dataframe)]
        columns: List[Column] = []

        while len(stack) > 0:
            parents, df = stack.pop()

            flat_cols: List[Column] = [
                col(".".join(parents + (c[0],))).alias("_".join(parents + (c[0],)))
                for c in df.dtypes
                if c[1][:6] != "struct"
            ]

            columns.extend(flat_cols)

            nested_cols: List[str] = [c[0] for c in df.dtypes if c[1][:6] == "struct"]

            for nested_col in nested_cols:
                projected_df = df.select(nested_col + ".*")
                stack.append((parents + (nested_col,), projected_df))

        return dataframe.select(columns)

    @staticmethod
    def convert_empty_string_to_null(dataframe: DataFrame) -> DataFrame:
        """
        Convert empty string to null in string columns.

        :param dataframe: DataFrame
        :return: converted dataframe
        """
        return dataframe.select(
            [
                when(length(col(c[0])) == 0, None).otherwise(col(c[0])).alias(c[0])
                if c[1] == "string"
                else col(c[0])
                for c in dataframe.dtypes
            ]
        )
