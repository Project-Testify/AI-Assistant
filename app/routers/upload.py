from fastapi import APIRouter, File, UploadFile, HTTPException
import os

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload a PDF.")

    # Check if uploads directory exists, and if not, create it
    upload_folder = "./uploads"
    os.makedirs(upload_folder, exist_ok=True)

    # Save PDF to the directory
    try:
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"filename": file.filename, "status": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
