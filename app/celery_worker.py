import os
import pymupdf
import asyncio
from celery import Celery
from sentence_transformers import SentenceTransformer

# Importuri pentru baza de date (AM ADĂUGAT 'engine' AICI)
from app.database import async_session_maker, engine
from app.models import DocumentChunk

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("pdf_worker", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(task_track_started=True, task_serializer='json', accept_content=['json'])

print("Încărcare model AI pentru embeddings (384 dimensiuni)...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model AI încărcat cu succes!")


def extract_text_and_chunk(file_path: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    doc = pymupdf.open(file_path)
    full_text = "".join([page.get_text("text") + "\n" for page in doc])

    chunks = []
    start = 0
    text_length = len(full_text)

    while start < text_length:
        end = start + chunk_size
        chunk = full_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks


# Funcție asincronă izolată pentru a salva datele în PostgreSQL
async def save_chunks_to_db(document_id: str, chunks: list[str], embeddings: list[list[float]]):
    async with async_session_maker() as session:
        for text, emb in zip(chunks, embeddings):
            db_chunk = DocumentChunk(
                document_id=document_id,
                text_content=text,
                embedding=emb
            )
            session.add(db_chunk)
        await session.commit()

    # FIX: Golim conexiunile pentru a permite rularea următoarelor task-uri
    # dintr-un event loop nou, fără a genera eroarea 'NoneType' object has no attribute 'send'
    await engine.dispose()


@celery_app.task(bind=True)
def process_pdf_task(self, file_path: str, document_id: str):
    print(f"Încep procesarea documentului {document_id}...")

    try:
        chunks = extract_text_and_chunk(file_path)
        print(f"Am extras {len(chunks)} fragmente. Generez vectorii...")

        embeddings = embedding_model.encode(chunks)
        print(f"Am generat {len(embeddings)} vectori. Salvez în baza de date...")

        # Rulăm operațiunea asincronă de scriere în DB dintr-un mediu sincron (Celery)
        asyncio.run(save_chunks_to_db(document_id, chunks, embeddings.tolist()))

        print("[SUCCES] Toate fragmentele au fost salvate în PostgreSQL cu pgvector!")
        return {"status": "completed", "document_id": document_id, "chunks_saved": len(chunks)}
    except Exception as e:
        print(f"[EROARE] Procesare eșuată: {str(e)}")
        return {"status": "failed", "document_id": document_id, "error": str(e)}