import pandas as pd
from datetime import datetime
import sys
# Retrieve input parameters
# bucket_name = sys.argv[1]
# file_prefix = sys.argv[2]

from awsglue.utils import getResolvedOptions
# getResolvedOptions function is used to retrieve the resolved (final) values of the command-line arguments and job parameters that were passed to the Glue job. 
ARGS_LIST = [
"bucket_name",
"file_prefix"]
params = getResolvedOptions(sys.argv, ARGS_LIST)

bucket_name=“edp-source-09022025”
file_prefix=“source_files/part-00000_orders_1.csv”
source_s3_url = “s3://edp-source-09022025/source_files/part-00000_orders_1.csv”

print("bucket_name : ",bucket_name)
print("file_prefix : ",file_prefix)
print("source_s3_url : ",source_s3_url)

now = datetime.now()
formatted_date_time = int(now.strftime("%Y%m%d%H%M%S"))
target_s3_url="s3://edp-target-090220252/target/orders/"+str(formatted_date_time)+'.parquet'

print("target_s3_url : ",target_s3_url)

df = pd.read_csv(source_s3_url)
print(df)

df.drop_duplicates(inplace = True) 
df = df.reset_index(drop=True)
df.to_parquet(target_s3_url)
