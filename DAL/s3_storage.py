import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, ReadTimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


def is_transient_error(e):
    return isinstance(e, (EndpointConnectionError, ReadTimeoutError, ClientError))


class S3Storage:
    def __init__(self, bucket: str):
        self.bucket = bucket
        self.s3 = boto3.client("s3")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((EndpointConnectionError, ReadTimeoutError, ClientError))
    )
    def upload_file(self, local_path: str, remote_key: str):
        try:
            self.s3.upload_file(local_path, self.bucket, remote_key)
        except ClientError as e:
            raise RuntimeError(f"Error while uploading : {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((EndpointConnectionError, ReadTimeoutError, ClientError))
    )
    def download_file(self, remote_key: str, local_path: str):
        try:
            self.s3.download_file(self.bucket, remote_key, local_path)
        except ClientError as e:
            raise RuntimeError(f"Error while downloading : {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((EndpointConnectionError, ReadTimeoutError, ClientError))
    )
    def list_files(self, prefix: str = "") -> list[str]:
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            return [obj["Key"] for obj in response.get("Contents", [])]
        except ClientError as e:
            raise RuntimeError(f"Error while listing : {e}")
