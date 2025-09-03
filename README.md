# AWS-Data-Pipeline-End-to-End


This project implements an event-driven, serverless ETL pipeline on AWS. Raw data is ingested into S3, event notifications trigger downstream services (SNS → SQS → Lambda), and AWS Glue performs scalable data transformations into Parquet. A Glue Crawler updates the Data Catalog for querying in Athena, while CloudWatch, EventBridge, and PagerDuty provide robust monitoring and alerting.

**The full pipeline architecture is illustrated in the flowchart below.**

<img width="1560" height="1054" alt="image" src="https://github.com/user-attachments/assets/10767a84-02d6-4df3-8cf9-84caa81770c1" />



**1. Source Data Ingestion**

Raw data is stored in the Source S3 bucket (**edp-source-09022025**).
An S3 event notification is triggered whenever a new file arrives.

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

https://mail.google.com/mail/u/0?ui=2&ik=56901e0374&attid=0.1&permmsgid=msg-a:r769492459743353411&th=1990ca771e5ee0d1&view=fimg&fur=ip&permmsgid=msg-a:r769492459743353411&sz=s0-l75-ft&attbid=ANGjdJ8v29_TlhaGTYiXQT4602qnSl4OUrP8lFLfAt4hNRhy-baklx_EpUE0w1AcXTcqQZbBJzR_MvhNBCku4jDrPnxWl2JfKQCPaEi8ObzT6eHsjR9PUuxl43KRw48&disp=emb&realattid=ii_mf30iirj0&zw<img width="500" height="430" alt="image" src="https://github.com/user-attachments/assets/77c0ce63-605e-4bff-a6f1-b15dc05a85f0" />

https://mail.google.com/mail/u/0?ui=2&ik=56901e0374&attid=0.2&permmsgid=msg-a:r769492459743353411&th=1990ca771e5ee0d1&view=fimg&fur=ip&permmsgid=msg-a:r769492459743353411&sz=s0-l75-ft&attbid=ANGjdJ9gT34-hI9nDN6Tl8oe0e9eSvnk5USaViSoPMxP_U8w45FuZYaWGwHAluq5ywWhdzwQbQ7KeMFrfFYWAtvHV8MdUtRV9fJXgf22sL9mIGmp3k6llsaTZGWVhcY&disp=emb&realattid=ii_mf30j28b1&zw<img width="1550" height="720" alt="image" src="https://github.com/user-attachments/assets/728bdc5a-b59a-4a35-9cc0-2df7ccb7b175" />


**5. Monitoring & Alerts**

Dead-letter queue (DLQ) captures failed SQS messages.
CloudWatch Alarm monitors DLQ and sends alerts via PagerDuty SNS topic.
Alerts are integrated with PagerDuty and Slack for real-time monitoring.


**6. Event-driven Notifications**

EventBridge Rules capture pipeline-related events (success/failure).
These rules publish to PagerDuty SNS, ensuring visibility in PagerDuty and Slack.

AWS Data Pipeline ingests raw data to S3, triggers SNS→SQS for reliable delivery, and ETL Lambda runs Glue jobs to clean/transform into Parquet in target S3. A Crawler Lambda updates Glue Catalog for Athena queries. DLQ &amp; CloudWatch monitor errors, while EventBridge + PagerDuty + Slack provide real-time alerts and observability.
