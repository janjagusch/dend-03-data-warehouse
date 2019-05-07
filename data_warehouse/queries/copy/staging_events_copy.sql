COPY staging_events
FROM '{}'
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
FORMAT AS JSON '{}';
