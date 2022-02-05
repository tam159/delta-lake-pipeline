# Delta Lake Pipeline

### Data pipelines for Spark structured streaming and Spark batching jobs.
- spark_jobs: Spark jobs to ingest data from Kafka and process it in micro batches.
- spark_libs: Spark common libraries for all jobs to process data such as flattening nested json data, .etc


## Delta Lake Overview
![ML Workflow](https://raw.githubusercontent.com/tam159/delta-lake-pipeline/main/images/Delta-Lake.png)

## Delta Lake Data Pipeline
![ML Workflow](https://raw.githubusercontent.com/tam159/delta-lake-pipeline/main/images/Lakehouse-Pipeline.png)

1. Regarding to data sources, there can be multiple sources such as:
- OLTP systems logs can be captured and sent to Apache Kafka (1a)
- Third party tools can also be integrated with the Kafka through various connectors (1b)
- And back-end team can produce event data directly to the Kafka (1c)
2. Once we have the data in the Kafka, we will use Spark Structured Streaming to consume the data and load it into Delta tables in a raw area. Thanks to checkpointing which stores Kafka offsets in this case, we can recover from failures with exactly-once fault-tolerant. We need to enable the Delta Lake CDF feature in these raw tables in order to serve further layers.
3. We will use the Spark Structured Streaming again to ingest changes from the raw tables. Then we would do some transformations like flattening and exploding nested data, .etc and load the cleansed data to a next area which is a refined zone. Remember to add the CDF in the refined tables properties.
4. Now we are ready to build data mart tables for business level by aggregating or joining tables from the refined area. This step is still in near real-time process because one more time we read the changes from previous layer tables by Spark Structured Streaming.
5. All the metadata is stored in the Databricks Data Catalog and all above tables can be queried in Databricks SQL Analytics, where we can create SQL endpoints and use a SQL editor. Beside the default catalog, we can use an open source [Amundsen](https://github.com/amundsen-io/amundsen) for the metadata discovery.
6. Eventually we can build some data visualizations from Databricks SQL Analytics Dashboards (formerly [Redash](https://github.com/getredash/redash)) or use BI tools like Power BI, [Streamlit](https://github.com/streamlit/streamlit), .etc.

## Detail Articles

### [Road to Lakehouse - Part 1: Delta Lake data pipeline overview][Road to Lakehouse - Part 1]
### [Road to Lakehouse - Part 2: Ingest and process data from Kafka with CDC and Delta Lake’s CDF][Road to Lakehouse - Part 2]


<!-- links -->
[Road to Lakehouse - Part 1]: https://www.linkedin.com/pulse/road-lakehouse-part-1-delta-lake-data-pipeline-overview-tam-nguyen
[Road to Lakehouse - Part 2]: https://tam159.medium.com/road-to-lakehouse-part-2-ingest-and-process-data-from-kafka-with-cdc-and-delta-lakes-cdf-318708468a47
