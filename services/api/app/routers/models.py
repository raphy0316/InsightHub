from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
from app.services.storage_service import save_model_file

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/upload")
async def upload_model(
    file: UploadFile = File(...),
    name: str = Form(...),
    framework: str = Form("onnx"),
    version: int = Form(1)
):
    ext = Path(file.filename).suffix.lower()
    if ext not in [".onnx"]:
        raise HTTPException(status_code=400, detail="Only .onnx files are allowed.")

    result = await save_model_file(
        file=file,
        version=version
    )

    return {
        **result,
        "framework": framework,
        "name": name,
    }
