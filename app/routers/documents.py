import shutil
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Document
from app.celery_worker import process_pdf_task

router = APIRouter(prefix="/documents", tags=["Documents"])
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/", status_code=status.HTTP_202_ACCEPTED)
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Doar fișierele PDF sunt acceptate.")

    doc_id = str(uuid.uuid4())
    safe_filename = f"{doc_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Salvăm Părintele (Documentul) în baza de date
    db_doc = Document(id=doc_id, filename=file.filename, file_path=file_path)
    db.add(db_doc)
    await db.commit()

    # 2. Trimitem procesarea către Celery
    task = process_pdf_task.delay(file_path, doc_id)

    return {
        "document_id": doc_id,
        "filename": file.filename,
        "task_id": task.id,
        "message": "Fișier salvat. Procesarea și vectorizarea au început în fundal."
    }