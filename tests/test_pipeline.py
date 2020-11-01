import unittest
from pyspark.sql import SparkSession
from pipeline import pipeline
from pyspark.sql.types import StructType, StructField, StringType

message_schema = StructType([StructField("name", StringType())])


class Test(unittest.TestCase):
    def test_pipeline(self) -> None:
        spark = _spark()
        data = spark.readStream.json(path="test_data/", schema=message_schema)

        stream = pipeline.process(data)

        stream.processAllAvailable()
        stream.stop()

        self.assertEquals(2, spark.sql("SELECT COUNT(1) AS count FROM example").first()["count"])
        self.assertEquals(1, spark.sql("SELECT COUNT(1) AS count FROM example WHERE name = 'a'").first()["count"])
        self.assertEquals(1, spark.sql("SELECT COUNT(1) AS count FROM example WHERE name = 'b'").first()["count"])


def _spark() -> SparkSession:
    return SparkSession.builder.appName("streaming-test").getOrCreate()
