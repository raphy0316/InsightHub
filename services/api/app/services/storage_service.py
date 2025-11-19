from fastapi import UploadFile
from storage.model_store import ModelStore
from storage.adapter_store import AdapterStore
from storage.dataset_store import DatasetStore
import uuid
from typing import Optional

model_store = ModelStore()
adapter_store = AdapterStore()
dataset_store = DatasetStore()

def save_model_file(file: UploadFile, version: Optional[int] = None):
    model_id = str(uuid.uuid4())
    storage_key = model_store.upload_model(
        model_id=model_id,
        file_obj=file.file,
        filename=file.filename,
        version=version,
    )
    return {
        "model_id": model_id,
        "version": version,
        "filename": file.filename,
        "storage_key": storage_key,
    }


def save_adapter_file(file: UploadFile, base_model_id: str | None = None) -> str:
    return adapter_store.upload_adapter(
        adapter_id=adapter_id,
        file_obj=file.file,
        filename=file.filename,
        base_model_id=base_model_id,
    )


def save_dataset_file(file: UploadFile) -> str:
    return dataset_store.upload_dataset(
        dataset_id=dataset_id,
        file_obj=file.file,
        filename=file.filename,
    )