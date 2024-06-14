from fastapi import APIRouter, File, UploadFile, HTTPException, Response, Query
import os

from ..services.pinecone_upsert import upsert

router = APIRouter()

@router.post("/upload-pdf/", status_code=201)
async def upload_pdf(file: UploadFile = None, examid: str = Query(..., description="The ID of the exam related to the uploaded PDF")) -> dict:
    if file is None:
        file = File(...)

    """Endpoint to upload a PDF and upsert its contents into a Pinecone vector store."""
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload a PDF.")

    # Assuming 'upsert' is an async function; if not, consider wrapping with 'await'
    # or adjust the function to be a regular call if it's designed to be synchronous
    success =  upsert(file, examid)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to process the PDF file.")

    # Directly return a message if upsert is successful; 'Response(status_code=201)' is redundant with `status_code=201` in the decorator
    return {"message": "PDF uploaded successfully."}
