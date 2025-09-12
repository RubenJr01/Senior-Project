from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, events

app = FastAPI(title="Planner API", version="0.1.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"], # Make sure HTML is here #
  allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(events.router, prefix="/events", tags=["events"])

@app.get("/health")
def health(): return {"ok": True}