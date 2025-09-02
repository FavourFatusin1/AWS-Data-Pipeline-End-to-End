# AWS-Data-Pipeline-End-to-End

https://mail.google.com/mail/u/0?ui=2&ik=56901e0374&attid=0.1&permmsgid=msg-a:r-3344140873114552128&th=1990b195d4deed6a&view=fimg&fur=ip&permmsgid=msg-a:r-3344140873114552128&sz=s0-l75-ft&attbid=ANGjdJ8aEW4nGspfTlrQ5YW90Qr69wJl0DXfqPNnubRJZSaAudZCZKWsE2-loq_Y7anFm8PK781dYIkNE_PabLMrFsMy3VxGexseGspJcWBw7E79_dGHxFkUlFWmjVA&disp=emb&realattid=ii_mf2pxew00&zw<img width="2720" height="950" alt="image" src="https://github.com/user-attachments/assets/bb8973d9-2652-4c84-9f23-046aa643b819" />


AWS Data Pipeline ingests raw data to S3, triggers SNS→SQS for reliable delivery, and ETL Lambda runs Glue jobs to clean/transform into Parquet in target S3. A Crawler Lambda updates Glue Catalog for Athena queries. DLQ &amp; CloudWatch monitor errors, while EventBridge + PagerDuty + Slack provide real-time alerts and observability.
