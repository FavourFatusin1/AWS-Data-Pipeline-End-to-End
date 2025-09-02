# AWS-Data-Pipeline-End-to-End

<img width="2720" height="950" alt="image" src="https://github.com/user-attachments/assets/bb8973d9-2652-4c84-9f23-046aa643b819" />


AWS Data Pipeline ingests raw data to S3, triggers SNS→SQS for reliable delivery, and ETL Lambda runs Glue jobs to clean/transform into Parquet in target S3. A Crawler Lambda updates Glue Catalog for Athena queries. DLQ &amp; CloudWatch monitor errors, while EventBridge + PagerDuty + Slack provide real-time alerts and observability.
