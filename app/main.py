from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_documents, routes_flashcards, routes_export
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Study Buddy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(routes_flashcards.router, prefix="/api/flashcards", tags=["Flashcards"])
app.include_router(routes_export.router, prefix="/api/export", tags=["Export"])

@app.get("/api/health")
def health_check():
    return {"success": True, "data": {"status": "ok"}, "error": None}
