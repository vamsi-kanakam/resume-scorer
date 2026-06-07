from fastapi import FastAPI
from Backend.app.routes.analyze import router

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Resume Scorer API!"}

