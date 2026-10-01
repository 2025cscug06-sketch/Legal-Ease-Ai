import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str,
        additional_instructions: str,
    ) -> str:

        prompt = f"""
You are a legal document drafting assistant.

Generate a professional draft legal document based
on the information below.

Document type:
{document_type}

Parties:
{parties}

Terms:
{terms}

Effective date:
{effective_date}

Jurisdiction:
{jurisdiction}

Additional instructions:
{additional_instructions}

Requirements:
- Use clear professional legal language.
- Organize the document with headings and clauses.
- Do not invent important facts.
- Clearly indicate information that is missing.
- This is a draft for review and not legal advice.

Return only the document content.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        return response.text