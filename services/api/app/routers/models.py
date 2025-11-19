from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/models/upload"):
async def upload_model(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in [".onnx"]:
        raise HTTPException(status_code=400, detail="Invalid file extension")
    
    save_path = f"models/{file.filename}"
    filename = file.filename
    file_content = await file.read()
    file_path = f"models/{filename}"
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    return {"filename": file.filename}
