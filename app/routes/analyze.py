from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai import score_resume

router = APIRouter()

class AnalyzeRequest(BaseModel):
    resume: str
    jd: str

@router.post("/analyze")
async def analyze_resume(body: AnalyzeRequest):
    result = await score_resume(body.resume, body.jd)
    return result
