
from typing import BinaryIO, Optional
from .s3_client import s3_client, S3_BUCKET_MODELS


class ModelStore:

    def __init__(self, bucket: Optional[str] = None, prefix: str = "models"):
        self.s3 = s3_client
        self.bucket = bucket or S3_BUCKET_MODELS
        self.prefix = prefix

    def _build_key(
        self,
        model_id: str,
        filename: str,
        version: Optional[int] = None,
    ) -> str:
        if version is None:
            return f"{self.prefix}/{model_id}/{filename}"
        return f"{self.prefix}/{model_id}/v{version}/{filename}"

    def upload_model(
        self,
        model_id: str,
        file_obj: BinaryIO,
        filename: str,
        version: Optional[int] = None,
    ) -> str:
        key = self._build_key(model_id=model_id, filename=filename, version=version)
        self.s3.upload_fileobj(file_obj, self.bucket, key)
        return key

    def download_model(
        self,
        model_id: str,
        filename: str,
        version: Optional[int] = None,
    ) -> bytes:
        key = self._build_key(model_id=model_id, filename=filename, version=version)
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read()

    def delete_model_file(
        self,
        model_id: str,
        filename: str,
        version: Optional[int] = None,
    ) -> None:
        key = self._build_key(model_id=model_id, filename=filename, version=version)
        self.s3.delete_object(Bucket=self.bucket, Key=key)