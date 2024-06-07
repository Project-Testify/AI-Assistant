from fastapi import APIRouter, File, UploadFile, HTTPException
import os

from ..services.pinecone_upsert import upsert

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload a PDF.")



    # upsert
    upsert(file,examid='examid')

    return {"filename": file.filename}



   
