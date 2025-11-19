# storage/dataset_store.py

from typing import BinaryIO
from .s3_client import s3_client, S3_BUCKET_DATASETS


class DatasetStore:

    def __init__(self, bucket: str | None = None, prefix: str = "datasets"):
        self.s3 = s3_client
        self.bucket = bucket or S3_BUCKET_DATASETS
        self.prefix = prefix

    def _build_key(self, dataset_id: str, filename: str) -> str:
        return f"{self.prefix}/{dataset_id}/{filename}"

    def upload_dataset(
        self,
        dataset_id: str,
        file_obj: BinaryIO,
        filename: str,
    ) -> str:
        key = self._build_key(dataset_id, filename)
        self.s3.upload_fileobj(file_obj, self.bucket, key)
        return key

    def download_dataset(
        self,
        dataset_id: str,
        filename: str,
    ) -> bytes:
        key = self._build_key(dataset_id, filename)
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read()

    def delete_dataset(
        self,
        dataset_id: str,
        filename: str,
    ) -> None:
        key = self._build_key(dataset_id, filename)
        self.s3.delete_object(Bucket=self.bucket, Key=key)
