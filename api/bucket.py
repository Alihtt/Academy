from django.conf import settings
import boto3


class Bucket:
    """CDN Bucket Manager

    init method creates an connection

    NOTE: None of these methods are async, use publick interface in tasks.py instead.

    """

    def __init__(self) -> None:
        session = boto3.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None

    def delete_object(self, key):
        self.conn.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as file:
            self.conn.download_fileobj(
                settings.AWS_STORAGE_BUCKET_NAME, key, file)


bucket = Bucket()
