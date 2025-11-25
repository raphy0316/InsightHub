import boto3
from typing import Any, Dict
from libs.config import settings

def get_s3_client() :
    common_kwargs: Dict[str, Any] = {
        "aws_access_key_id": settings.S3_ACCESS_KEY,
        "aws_secret_access_key": settings.S3_SECRET_KEY,
        "region_name": settings.S3_REGION,
    }

    if settings.STORAGE_BACKEND == "minio":
        return boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT,
            **common_kwargs
        )
    elif settings.STORAGE_BACKEND == "aws":
        return boto3.client(
            "s3",
            **common_kwargs
        )
    else:
        raise ValueError(f"Invalid storage backend: {settings.STORAGE_BACKEND}")

s3_client = get_s3_client()
S3_BUCKET_MODELS = settings.S3_BUCKET_MODELS
S3_BUCKET_ADAPTERS = settings.S3_BUCKET_ADAPTERS
S3_BUCKET_DATASETS = settings.S3_BUCKET_DATASETS