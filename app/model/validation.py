from pydantic import BaseModel, validator

class CorrectionRequest(BaseModel):
    bangla_sentence: str
    user_translation: str

    @validator("bangla_sentence")
    def bangla_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Bangla sentence cannot be empty")
        if len(v) > 1500:
            raise ValueError("Bangla sentence too long (max 1500 chars)")
        return v

    @validator("user_translation")
    def english_non_empty(cls, v):
        if not v.strip():
            raise ValueError("User translation cannot be empty")
        if len(v) > 2000:
            raise ValueError("User translation too long (max 2000 chars)")
        return v

class BanglaSentenceResponse(BaseModel):
    bangla_sentence: str

class CorrectionResponse(BaseModel):
    correction: str
