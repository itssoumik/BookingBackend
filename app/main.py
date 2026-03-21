from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our new router
from app.api.v1 import hotels

app = FastAPI(
    title="Guest House API",
    description="Backend engine for the Guest House Booking System",
    version="1.0.0"
)

# Configure CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotels.router, prefix="/api/v1/hotels", tags=["Hotels"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Guest House API is running!"}