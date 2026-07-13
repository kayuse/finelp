from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import sample, auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(sample.router, prefix=settings.API_V1_STR, tags=["sample"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Welcome to FinElp API"}
