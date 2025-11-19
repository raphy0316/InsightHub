from fastapi import UploadFile
from storage.model_store import ModelStore
from storage.adapter_store import AdapterStore
from storage.dataset_store import DatasetStore
import uuid
import asyncio
from typing import Optional

model_store = ModelStore()
adapter_store = AdapterStore()
dataset_store = DatasetStore()

async def save_model_file(file: UploadFile, version: Optional[int] = None):
    model_id = str(uuid.uuid4())
    
    storage_key = await asyncio.to_thread(
        _upload_model_sync,
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

def _upload_model_sync(model_id: str, file_obj, filename: str, version: Optional[int] = None) -> str:
    return model_store.upload_model(
        model_id=model_id,
        file_obj=file_obj,
        filename=filename,
        version=version,
    )


def save_adapter_file(file: UploadFile, base_model_id: str | None = None) -> str:
    adapter_id = str(uuid.uuid4())
    return adapter_store.upload_adapter(
        adapter_id=adapter_id,
        file_obj=file.file,
        filename=file.filename,
        base_model_id=base_model_id,
    )


def save_dataset_file(file: UploadFile) -> str:
    dataset_id = str(uuid.uuid4())
    return dataset_store.upload_dataset(
        dataset_id=dataset_id,
        file_obj=file.file,
        filename=file.filename,
    )