from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.services.correction_chain import CorrectionChainService
from app.services.user_state import set_bangla_sentence, get_bangla_sentence

router = APIRouter()
service = CorrectionChainService()

class CorrectionRequest(BaseModel):
    user_id: int
    user_translation: str

@router.get("/bangla_sentence")
async def get_bangla_sentence_route(user_id: int = Query(...)):
    bangla_sentence = service.generate_bangla_sentence(user_id)
    set_bangla_sentence(user_id, bangla_sentence)
    return {"sentence": bangla_sentence}

@router.post("/correction")
async def correction_route(data: CorrectionRequest):
    bangla_sentence = get_bangla_sentence(data.user_id)
    if not bangla_sentence:
        return {"correction": "❌ No Bangla sentence found for this user. Please start with /start."}
    correction = service.get_correction(bangla_sentence, data.user_translation)
    return {"correction": correction}
