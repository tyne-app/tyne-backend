import uuid

import boto3

from src.configuration.Settings import Settings


class AwsService:

    async def upload_to_s3(self, file: bytes, folder: str, contentType: str):
        s3_client = boto3.client(service_name='s3', region_name='us-east-1',
                                 aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY)

        identifier = str(uuid.uuid4())
        fileExtension = '.' + contentType.split("/")[-1]
        filename = identifier + fileExtension

        bucketName = "tyne"
        path = Settings.ENVIRONMENT + "/" + folder + "/" + filename

        s3_client.put_object(Body=file, Bucket=bucketName,
                             Key=path,
                             ContentType=contentType)

        url = "https://%s.s3.amazonaws.com/%s" % (bucketName, path)
        return url
