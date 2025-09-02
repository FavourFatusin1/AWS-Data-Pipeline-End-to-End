# AWS-Data-Pipeline-End-to-End

<img width="2720" height="950" alt="image" src="https://github.com/user-attachments/assets/bb8973d9-2652-4c84-9f23-046aa643b819" />

1. Source Data Ingestion
Raw data is stored in the Source S3 bucket (source_path).
An S3 event notification is triggered whenever a new file arrives.
<img width="1440" height="447" alt="image" src="https://github.com/user-attachments/assets/3811fe92-03e2-4715-a63d-c29788720df8" />
2. Event Propagation
The notification is sent to an SNS topic (Source SNS).
The SNS topic fan-outs the event to SQS (Source Queue) for reliable delivery.

3. ETL Processing
The SQS message triggers an ETL Lambda function.
Lambda initiates an AWS Glue job to process the incoming file:
Cleans, transforms, and deduplicates the data.
Writes the processed output to the Target S3 bucket (target path) in Parquet format.

4. Data Cataloguing
Once new data lands in the target bucket, another S3 notification triggers a Crawler Lambda.
This Lambda runs a Glue Crawler that updates the Glue Data Catalog with the new schema/partitions.
Updated metadata enables Athena to query the latest data.

5. Monitoring & Alerts
Dead-letter queue (DLQ) captures failed SQS messages.
CloudWatch Alarm monitors DLQ and sends alerts via PagerDuty SNS topic.
Alerts are integrated with PagerDuty and Slack for real-time monitoring.

6. Event-driven Notifications
EventBridge Rules capture pipeline-related events (success/failure).
These rules publish to PagerDuty SNS, ensuring visibility in PagerDuty and Slack.

AWS Data Pipeline ingests raw data to S3, triggers SNS→SQS for reliable delivery, and ETL Lambda runs Glue jobs to clean/transform into Parquet in target S3. A Crawler Lambda updates Glue Catalog for Athena queries. DLQ &amp; CloudWatch monitor errors, while EventBridge + PagerDuty + Slack provide real-time alerts and observability.
