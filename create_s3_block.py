from prefect.filesystems import S3


s3 = S3(
    bucket_path='bucket',
    aws_access_key_id='<key_id>',
    aws_secret_access_key='<key_secret>',
)
s3.save('name', overwrite=True)