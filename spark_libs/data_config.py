"""Data configuration."""

CDF_COLUMNS = ["_change_type", "_commit_version", "_commit_timestamp"]
KAFKA_KEY_COLUMNS = ["key", "value"]
KAFKA_TOPIC_COLUMNS = ["topic", "partition", "offset", "timestamp", "timestampType"]
KAFKA_COLUMNS = KAFKA_KEY_COLUMNS + KAFKA_TOPIC_COLUMNS

DATA_FILES_RETENTION_HOURS = 24 * 7
