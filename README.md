# AWS-Data-Pipeline-End-to-End

[<img width="905" height="792" alt="image" src="https://github.com/user-attachments/assets/a045dbc0-1e18-41d4-ba84-3343f28d3311" />
](https://mail.google.com/mail/u/0?ui=2&ik=56901e0374&attid=0.1&permmsgid=msg-a:r5278225978106667764&th=1990d3c234613d7b&view=fimg&fur=ip&permmsgid=msg-a:r5278225978106667764&sz=s0-l75-ft&attbid=ANGjdJ-kuDXFYw9-T4dRM5r9sBzA04IoGtkLfAZqVM9ROa77MUtcZCHYuYlTZQbR5w48eZ16LWJ8z_FiVc6E4j-Y-qq0GwM33bXSz2iViN7rR0CNG2YTmdaC7gOME-Y&disp=emb&realattid=ii_mf3b955t0&zw)<img width="1560" height="1054" alt="image" src="https://github.com/user-attachments/assets/393b9e59-71b9-45af-a40c-169a0ec599b6" />


1. Source Data Ingestion
Raw data is stored in the Source S3 bucket (edp-source-09022025).
An S3 event notification is triggered whenever a new file arrives.
<img width="720" height="223" alt="image" src="https://github.com/user-attachments/assets/3811fe92-03e2-4715-a63d-c29788720df8" />
2. Event Propagation
The notification is sent to an SNS topic (Source SNS).
The SNS topic fan-outs the event to SQS (Source Queue) for reliable delivery.
<img width="552" height="132" alt="image" src="https://github.com/user-attachments/assets/bf1dbc26-c537-49a3-b0f8-eae71a9a8f50" />


3. ETL Processing
The SQS message triggers an ETL Lambda function.
Lambda initiates an AWS Glue job to process the incoming file:
Cleans, transforms, and deduplicates the data.
Writes the processed output to the Target S3 bucket (target path) in Parquet format.
<img width="476" height="214" alt="image" src="https://github.com/user-attachments/assets/e4a3be23-cdcc-443b-a5b3-7f5df8fbc918" />
<img width="709" height="280" alt="image" src="https://github.com/user-attachments/assets/ecf79330-ae73-4b96-84a8-085c466fa873" />



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
