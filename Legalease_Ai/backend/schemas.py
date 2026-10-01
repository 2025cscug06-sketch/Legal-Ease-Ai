from pydantic import BaseModel
from typing import Optional


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str
    jurisdiction: Optional[str] = None
    additional_instructions: Optional[str] = None


class DocumentResponse(BaseModel):
    success: bool
    document_type: str
    content: str
    message: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    ai_mode: str