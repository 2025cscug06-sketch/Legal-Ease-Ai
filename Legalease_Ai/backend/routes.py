from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.config import APP_VERSION, MODEL_MOCK
from backend.schemas import DocumentRequest, DocumentResponse, HealthResponse

router = APIRouter()

generator = None


def get_generator():
    global generator

    if generator is None:
        try:
            generator = GeminiDocumentGenerator()
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    return generator


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        service="LegalEase API",
        version=APP_VERSION,
        ai_mode="mock" if MODEL_MOCK else "gemini",
    )


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        document_generator = get_generator()

        content = document_generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction or "Not specified",
            additional_instructions=request.additional_instructions or "",
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=content,
            message="Document generated successfully.",
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document generation failed: " + str(exc),
        )
        