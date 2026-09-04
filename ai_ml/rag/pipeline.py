from retrieval.search import Retriever
from services.groq_service import GroqService


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()

        self.groq_service = GroqService()

    def ask(
        self,
        question,
        articles
    ):

        relevant_articles = (
            self.retriever.search(
                question=question,
                articles=articles,
                top_k=3
            )
        )

        if not relevant_articles:

            return {
                "answer": (
                    "No relevant information was found."
                ),
                "sources": []
            }

        context_parts = []

        for article in relevant_articles:

            context_parts.append(
                f"""
TITLE:
{article['title']}

SUMMARY:
{article.get('summary') or ''}

CONTENT:
{article['content']}
"""
            )

        context = "\n\n".join(context_parts)

        answer = (
            self.groq_service.generate_answer(
                question=question,
                context=context
            )
        )

        sources = []

        for article in relevant_articles:

            sources.append(
                {
                    "id": article["id"],
                    "title": article["title"]
                }
            )

        return {
            "answer": answer,
            "sources": sources
        }