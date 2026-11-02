from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importăm modulele pentru rute
from app.routers import users, documents

# Inițializăm aplicația cu metadate profesionale
app = FastAPI(
    title="RAG PDF Chat API",
    description="API asincron pentru procesare de documente și căutare semantică vectorială.",
    version="1.0.0"
)

# Configurare CORS pentru a permite viitorului frontend (ex: React) să comunice cu API-ul
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Înregistrăm rutele în aplicație
app.include_router(users.router)
app.include_router(documents.router)

# Endpoint de Health Check
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "message": "Sistemul RAG este operațional."}