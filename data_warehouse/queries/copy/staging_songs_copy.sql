COPY staging_songs
FROM '{}'
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
JSON 'auto';
