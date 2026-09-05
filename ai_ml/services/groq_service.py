import logging
from groq import Groq
from config import GROQ_API_KEY

logger = logging.getLogger(__name__)


class GroqService:

    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate_answer(self, question, context):
        if not self.client:
            # Cleanly format the fallback context without raw TITLE/CONTENT metadata dumps
            clean_summary = self._format_fallback_context(context)
            return (
                f"### 📖 Summary from ChronoFlow Knowledge Base\n\n"
                f"{clean_summary}\n\n"
                "*Tip: Configure `GROQ_API_KEY` in `backend/.env` for AI LLM synthesis.*"
            )

        prompt = f"""
You are ChronoFlow AI.

Answer the user's question using ONLY the information provided in the context.

If the answer cannot be found in the context, say that the information is not available in the ChronoFlow knowledge base.

CONTEXT:
{context}

QUESTION:
{question}

Provide a clear, accurate, and structured Markdown answer with bullet points if applicable.
"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as exc:
            logger.warning(f"Groq API call failed: {exc}")
            clean_summary = self._format_fallback_context(context)
            return f"### 📖 Summary from ChronoFlow Knowledge Base\n\n{clean_summary}"

    def _format_fallback_context(self, context: str) -> str:
        """Helper to format raw article context into clean readable text."""
        lines = context.split("\n")
        output = []
        current_title = ""
        current_summary = ""

        for line in lines:
            line_str = line.strip()
            if line_str.startswith("TITLE:"):
                current_title = ""
            elif line_str.startswith("SUMMARY:"):
                current_summary = ""
            elif line_str.startswith("CONTENT:"):
                continue
            elif line_str.startswith("Full reporting at:"):
                continue
            elif line_str.startswith("http://") or line_str.startswith("https://"):
                continue
            elif line_str:
                output.append(f"• {line_str}")

        if not output:
            return context

        # Remove duplicate bullets & truncate long raw text
        unique_bullets = []
        seen = set()
        for bullet in output:
            if bullet not in seen and len(bullet) > 5:
                seen.add(bullet)
                unique_bullets.append(bullet)

        return "\n\n".join(unique_bullets[:8])