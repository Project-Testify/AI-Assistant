# app/__init__.py
from fastapi import FastAPI
from .routers.upload import router as upload_router
from .routers.questionGenerate import router as questionGenerate_router


from .main import app

# Include routers with appropriate API version prefix
app.include_router(upload_router, prefix="/api/v1")
app.include_router(questionGenerate_router, prefix="/api/v1")
