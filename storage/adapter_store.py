# storage/adapter_store.py

from typing import BinaryIO, Optional
from .s3_client import s3_client, S3_BUCKET_ADAPTERS


class AdapterStore:

    def __init__(self, bucket: Optional[str] = None, prefix: str = "adapters"):
        self.s3 = s3_client
        self.bucket = bucket or S3_BUCKET_ADAPTERS
        self.prefix = prefix

    def _build_key(
        self,
        adapter_id: str,
        filename: str,
        base_model_id: Optional[str] = None,
    ) -> str:
        if base_model_id:
            return f"{self.prefix}/{base_model_id}/{adapter_id}/{filename}"
        return f"{self.prefix}/{adapter_id}/{filename}"

    def upload_adapter(
        self,
        adapter_id: str,
        file_obj: BinaryIO,
        filename: str,
        base_model_id: Optional[str] = None,
    ) -> str:
        key = self._build_key(
            adapter_id=adapter_id,
            filename=filename,
            base_model_id=base_model_id,
        )
        self.s3.upload_fileobj(file_obj, self.bucket, key)
        return key

    def download_adapter(
        self,
        adapter_id: str,
        filename: str,
        base_model_id: Optional[str] = None,
    ) -> bytes:
        key = self._build_key(
            adapter_id=adapter_id,
            filename=filename,
            base_model_id=base_model_id,
        )
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read()

    def delete_adapter(
        self,
        adapter_id: str,
        filename: str,
        base_model_id: Optional[str] = None,
    ) -> None:
        key = self._build_key(
            adapter_id=adapter_id,
            filename=filename,
            base_model_id=base_model_id,
        )
        self.s3.delete_object(Bucket=self.bucket, Key=key)
