from fastapi import APIRouter, File, UploadFile, HTTPException, Response, Query
import os

from ..services.pinecone_upsert import upsert

from ..core.log import logger

from typing import List


router = APIRouter()


@router.post("/upload-pdf/", status_code=201)
async def upload_pdf(files: List[UploadFile] = File(...), examid: str = Query(..., description="The ID of the exam related to the uploaded PDF")) -> dict:
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")


    # Print the exam ID and the number of files uploaded
    logger.info(f"Exam ID: {examid}")
    logger.info(f"Number of files uploaded: {len(files)}")
    errors = []
    for file in files:
        if file.content_type != 'application/pdf':
            errors.append(f"Unsupported file type for {file.filename}. Please upload PDF.")
            continue  # Skip files that are not PDFs

        success = upsert(file, examid)  # Assuming upsert is correctly defined to handle async operations
        if not success:
            errors.append(f"Failed to process {file.filename}.")

    if errors:
        raise HTTPException(status_code=500, detail="Errors occurred during processing: " + "; ".join(errors))
    
    return {"message": "All PDFs uploaded successfully."}
