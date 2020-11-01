from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery


def process(source: DataFrame) -> StreamingQuery:

    query = source.writeStream.format("memory").queryName("example").start()

    return query
