from fastapi import UploadFile
from storage.model_store import ModelStore
from storage.adapter_store import AdapterStore
from storage.dataset_store import DatasetStore


model_store = ModelStore()
adapter_store = AdapterStore()
dataset_store = DatasetStore()

def save_model_file(model_id: str, file: UploadFile, version: Optional[int] = None):
    return model_store.upload_model(
        model_id = model_id, 
        file_obj = file.file, 
        filename = file.filename,
        version = version,
    )


def save_adapter_file(adapter_id: str, file: UploadFile, base_model_id: str | None = None) -> str:
    return adapter_store.upload_adapter(
        adapter_id=adapter_id,
        file_obj=file.file,
        filename=file.filename,
        base_model_id=base_model_id,
    )


def save_dataset_file(dataset_id: str, file: UploadFile) -> str:
    return dataset_store.upload_dataset(
        dataset_id=dataset_id,
        file_obj=file.file,
        filename=file.filename,
    )