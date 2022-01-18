"""Raw events schemas."""

from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

transaction_schema = StructType(
    [
        StructField(
            "transaction",
            StructType(
                [
                    StructField("createdBy", StringType(), True),
                    StructField("createdDate", TimestampType(), True),
                    StructField("lastModifiedBy", StringType(), True),
                    StructField("lastModifiedDate", TimestampType(), True),
                    StructField("id", StringType(), True),
                    StructField("clientId", StringType(), True),
                    StructField("clientCode", StringType(), True),
                    StructField("eventId", StringType(), True),
                    StructField("clientTransactionId", StringType(), True),
                    StructField("networkTransactionId", StringType(), True),
                    StructField("time", TimestampType(), True),
                    StructField("state", StringType(), True),
                    StructField("clientCustomerId", StringType(), True),
                    StructField("homeCurrency", StringType(), True),
                    StructField("homeAmount", DoubleType(), True),
                    StructField("merchantCurrency", StringType(), True),
                    StructField("merchantAmount", DoubleType(), True),
                    StructField("savedInKafka", BooleanType(), True),
                    StructField("receiptLinkingKey", StringType(), True),
                ]
            ),
            True,
        ),
        StructField(
            "paymentSource",
            StructType(
                [
                    StructField("externalId", StringType(), True),
                    StructField("par", StringType(), True),
                    StructField("last4Digits", StringType(), True),
                    StructField("paymentSourceProduct", StringType(), True),
                    StructField("paymentFundingSource", StringType(), True),
                    StructField("paymentSourceNetwork", StringType(), True),
                    StructField("paymentMethod", StringType(), True),
                    StructField("bin", StringType(), True),
                    StructField("cardArtWork", StringType(), True),
                ]
            ),
            True,
        ),
        StructField(
            "paymentStore",
            StructType(
                [
                    StructField("storeId", StringType(), True),
                    StructField(
                        "Merchant",
                        StructType(
                            [
                                StructField("createdBy", StringType(), True),
                                StructField("createdDate", TimestampType(), True),
                                StructField("lastModifiedBy", StringType(), True),
                                StructField("lastModifiedDate", TimestampType(), True),
                                StructField("id", StringType(), True),
                                StructField("name", StringType(), True),
                                StructField("displayName", StringType(), True),
                                StructField("code", StringType(), True),
                                StructField("merchantLogoAssetId", StringType(), True),
                                StructField("status", StringType(), True),
                                StructField("website", StringType(), True),
                                StructField(
                                    "address",
                                    StructType(
                                        [
                                            StructField("address1", StringType(), True),
                                            StructField("address2", StringType(), True),
                                            StructField("address3", StringType(), True),
                                            StructField("city", StringType(), True),
                                            StructField("state", StringType(), True),
                                            StructField("zipCode", StringType(), True),
                                            StructField(
                                                "countryCode", StringType(), True
                                            ),
                                        ]
                                    ),
                                    True,
                                ),
                                StructField("contactName", StringType(), True),
                                StructField("contactEmail", StringType(), True),
                                StructField("locale", StringType(), True),
                            ]
                        ),
                        True,
                    ),
                    StructField(
                        "Store",
                        StructType(
                            [
                                StructField("createdBy", StringType(), True),
                                StructField("createdDate", TimestampType(), True),
                                StructField("lastModifiedBy", StringType(), True),
                                StructField("lastModifiedDate", TimestampType(), True),
                                StructField("id", StringType(), True),
                                StructField("name", StringType(), True),
                                StructField("status", StringType(), True),
                                StructField(
                                    "address",
                                    StructType(
                                        [
                                            StructField("address1", StringType(), True),
                                            StructField("address2", StringType(), True),
                                            StructField("address3", StringType(), True),
                                            StructField("city", StringType(), True),
                                            StructField("state", StringType(), True),
                                            StructField("zipCode", StringType(), True),
                                            StructField(
                                                "countryCode", StringType(), True
                                            ),
                                        ]
                                    ),
                                    True,
                                ),
                                StructField(
                                    "location",
                                    StructType(
                                        [
                                            StructField(
                                                "longitude", StringType(), True
                                            ),
                                            StructField("latitude", StringType(), True),
                                        ]
                                    ),
                                    True,
                                ),
                            ]
                        ),
                        True,
                    ),
                    StructField("storeName", StringType(), True),
                    StructField("categoryCode", StringType(), True),
                    StructField("mcgCode", StringType(), True),
                    StructField("mcgDescription", StringType(), True),
                    StructField("mcgIcon", StringType(), True),
                    StructField("acquirerBin", StringType(), True),
                    StructField("cardAcceptorId", StringType(), True),
                    StructField("address1", StringType(), True),
                    StructField("address2", StringType(), True),
                    StructField("city", StringType(), True),
                    StructField("state", StringType(), True),
                    StructField("zipCode", StringType(), True),
                    StructField("countryCode", StringType(), True),
                ]
            ),
            True,
        ),
    ]
)
