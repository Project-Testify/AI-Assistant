from fastapi import APIRouter, File, UploadFile, HTTPException, Response, Query
import os

from ..services.pinecone_upsert import upsert

router = APIRouter()

@router.post("/upload-pdf/", status_code=201)
async def upload_pdf(file: UploadFile = File(...), examid:str = Query(..., description="The ID of the exam related to the uploaded PDF") ) -> dict:
    """Endpoint to upload a PDF and upsert its contents into a Pinecone vector store."""

    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload a PDF.")

    # Call the upsert function from the imported service
    upsert(file, examid)

    # return {"filename": file.filename}
    Response(status_code=201)
    return {"message": "PDF uploaded successfully."}
