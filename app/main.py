from fastapi import FastAPI
from app.routers import documents,tickets,comments

app = FastAPI(title="LineMate API")
app.include_router(documents.router)
app.include_router(tickets.router)
app.include_router(comments.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

