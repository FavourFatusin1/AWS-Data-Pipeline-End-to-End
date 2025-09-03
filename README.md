# AWS-Data-Pipeline-End-to-End


This project implements an event-driven, serverless ETL pipeline on AWS. Raw data is ingested into S3, event notifications trigger downstream services (SNS → SQS → Lambda), and AWS Glue performs scalable data transformations into Parquet. A Glue Crawler updates the Data Catalog for querying in Athena, while CloudWatch, EventBridge, and PagerDuty provide robust monitoring and alerting.

**The full pipeline architecture is illustrated in the flowchart below.**

<img width="776" height="522" alt="image" src="https://github.com/user-attachments/assets/fc423c79-4a41-4284-9070-ae4c213e9750" />



**1. Source Data Ingestion**

- Raw data is stored in the Source S3 bucket (**edp-source-09022025**).

- An S3 event notification is triggered whenever a new file arrives.

<img width="720" height="223" alt="image" src="https://github.com/user-attachments/assets/3811fe92-03e2-4715-a63d-c29788720df8" />

**2. Event Propagation**

The notification is sent to an SNS topic (**arn:aws:sns:us-east-2:966656799543:edp-topic-09022025**).
The SNS topic **then** fan-outs the event to an SQS queue (**arn:aws:sqs:us-east-2:966656799543:edp-queue-09022025**) for reliable delivery.

<img width="552" height="132" alt="image" src="https://github.com/user-attachments/assets/bf1dbc26-c537-49a3-b0f8-eae71a9a8f50" />


**3. ETL Processing**

The SQS message triggers an ETL Lambda function.
Lambda initiates an AWS Glue job to process the incoming file:
Cleans, transforms, and deduplicates the data.
Writes the processed output to the Target S3 bucket (target path) in Parquet format.

<img width="476" height="214" alt="image" src="https://github.com/user-attachments/assets/e4a3be23-cdcc-443b-a5b3-7f5df8fbc918" />

<img width="709" height="280" alt="image" src="https://github.com/user-attachments/assets/ecf79330-ae73-4b96-84a8-085c466fa873" />



**4. Data Cataloguing**

Once new data lands in the target bucket, another S3 notification triggers a Crawler Lambda.
This Lambda runs a Glue Crawler that updates the Glue Data Catalog with the new schema/partitions.
Updated metadata enables Athena to query the latest data. A table in the AWS database becomes visible with the necessary data from the files.

<img width="200" height="215" alt="image" src="https://github.com/user-attachments/assets/77c0ce63-605e-4bff-a6f1-b15dc05a85f0" />

<img width="725" height="360" alt="image" src="https://github.com/user-attachments/assets/728bdc5a-b59a-4a35-9cc0-2df7ccb7b175" />


**5. Monitoring & Alerts**

Dead-letter queue (DLQ) captures failed SQS messages.
CloudWatch Alarm monitors DLQ and sends alerts via PagerDuty SNS topic.
Alerts are integrated with PagerDuty and Slack for real-time monitoring.


**6. Event-driven Notifications**

EventBridge Rules capture pipeline-related events (success/failure).
These rules publish to PagerDuty SNS, ensuring visibility in PagerDuty and Slack.

AWS Data Pipeline ingests raw data to S3, triggers SNS→SQS for reliable delivery, and ETL Lambda runs Glue jobs to clean/transform into Parquet in target S3. A Crawler Lambda updates Glue Catalog for Athena queries. DLQ &amp; CloudWatch monitor errors, while EventBridge + PagerDuty + Slack provide real-time alerts and observability.
