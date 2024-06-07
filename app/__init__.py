# app/__init__.py
from .main import app

from .routers.upload import router as upload_router


app.include_router(upload_router, prefix="/api/v1")


# app/routers/upload.py


