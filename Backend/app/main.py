from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .api import auth, events

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

# Redirect the root path to interactive API docs for easier onboarding
@app.get("/", include_in_schema=False)
def root():
  return RedirectResponse(url="/docs")

# Auto-create tables on startup for local development
@app.on_event("startup")
def on_startup():
  # Import inside the function to avoid circular imports at module load time
  from .db.session import engine, Base
  from .db import models  # noqa: F401 ensures models are registered with Base
  Base.metadata.create_all(bind=engine)
