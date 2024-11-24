!pip install pyspark


from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, lit


spark = SparkSession.builder.appName('HoverEventProcessing').getOrCreate()


file_path = '/content/hover_events.txt'
df = spark.read.text(file_path)


df_split = df.select(split(col('value'), ' \| ').alias('columns'))


df_events = df_split.select(
    col('columns')[0].alias('timestamp'),
    col('columns')[1].alias('action'),
    col('columns')[2].alias('product'),
    col('columns')[3].alias('quantity')
)


df_hovered = df_events.filter(df_events['action'] == 'Hovered over')


df_product_count = df_hovered.groupBy('product').count()


df_result = df_product_count.withColumn('timestamp', lit('2024/11/23 19:34:10')) \
                             .withColumn('action', lit('Hovered over')) \
                             .select('timestamp', 'action', 'product', 'count')


df_result_formatted = df_result.select(
    col('timestamp'),
    col('action'),
    col('product'),
    col('count')
).rdd.map(lambda row: f"{row['timestamp']} | {row['action']} | {row['product']} | {row['count']}")


output_path = '/content/hovered_events_output.txt'
df_result_formatted.saveAsTextFile(output_path)


for line in df_result_formatted.take(10):
    print(line)





>>>>
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, sum, count


spark = SparkSession.builder.appName('PurchaseEventProcessing').getOrCreate()


file_path = '/content/purchase_events.txt'
df = spark.read.text(file_path)


df_split = df.select(split(col('value'), ' \| ').alias('columns'))


df_events = df_split.select(
    col('columns')[0].alias('timestamp'),
    col('columns')[1].alias('action'),
    col('columns')[2].alias('product'),
    col('columns')[3].alias('quantity'),
    col('columns')[4].alias('price')
)


df_purchased = df_events.filter(df_events['action'] == 'Product purchased')


df_purchased = df_purchased.withColumn('quantity', col('quantity').cast('int'))
df_purchased = df_purchased.withColumn('price', col('price').cast('int'))


df_product_stats = df_purchased.groupBy('product').agg(
    count('quantity').alias('purchase_count'),
    sum('price').alias('total_price')
)


df_result = df_product_stats.withColumn('timestamp', lit('2024/11/23 19:34:10')) \
                             .withColumn('action', lit('Product purchased')) \
                             .select('timestamp', 'action', 'product', 'purchase_count', 'total_price')


df_result_formatted = df_result.select(
    col('timestamp'),
    col('action'),
    col('product'),
    col('purchase_count'),
    col('total_price')
).rdd.map(lambda row: f"{row['timestamp']} | {row['action']} | {row['product']} | {row['purchase_count']} | {row['total_price']}")


output_path = '/content/purchased_output.txt'
df_result_formatted.saveAsTextFile(output_path)


