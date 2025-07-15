from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.services.correction_chain import CorrectionChainService
from app.services.user_state import (
    set_bangla_sentence,
    get_bangla_sentence,
)

router = APIRouter()
service = CorrectionChainService()

# Request model for correction
class CorrectionRequest(BaseModel):
    user_id: int
    user_translation: str

# GET /bangla_sentence?user_id=123
@router.get("/bangla_sentence")
async def get_bangla_sentence_route(user_id: int = Query(...)):
    """
    Generate a new Bangla sentence for the user based on grammar topic progression.
    """
    bangla_sentence = service.generate_bangla_sentence(user_id)
    set_bangla_sentence(user_id, bangla_sentence)
    return {"sentence": bangla_sentence}

# POST /correction
@router.post("/correction")
async def correction_route(data: CorrectionRequest):
    """
    Correct the user's translation and return feedback + IELTS score.
    """
    bangla_sentence = get_bangla_sentence(data.user_id)

    if not bangla_sentence:
        return {
            "correction": "❌ No Bangla sentence found for this user. Please start with /start."
        }

    correction = service.get_correction(bangla_sentence, data.user_translation)
    return {"correction": correction}
