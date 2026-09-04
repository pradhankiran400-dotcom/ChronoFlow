from groq import Groq

from config import GROQ_API_KEY


class GroqService:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def generate_answer(
        self,
        question,
        context
    ):

        prompt = f"""
You are ChronoFlow AI.

Answer the user's question using ONLY
the information provided in the context.

If the answer cannot be found in the context,
say that the information is not available
in the ChronoFlow knowledge base.

CONTEXT:
{context}

QUESTION:
{question}

Provide a clear and concise answer.
"""

        response = (
            self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
        )