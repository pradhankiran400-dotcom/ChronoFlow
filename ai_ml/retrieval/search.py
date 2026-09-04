import numpy as np

from emmbeddings.embedder import Embedder


class Retriever:

    def __init__(self):

        self.embedder = Embedder()

    def search(
        self,
        question,
        articles,
        top_k=3
    ):

        if not articles:
            return []

        article_texts = []

        for article in articles:

            text = (
                f"Title: {article['title']}\n"
                f"Summary: {article.get('summary') or ''}\n"
                f"Content: {article['content']}"
            )

            article_texts.append(text)

        article_embeddings = (
            self.embedder.model.encode(
                article_texts,
                normalize_embeddings=True
            )
        )

        question_embedding = (
            self.embedder.create_embedding(question)
        )

        scores = np.dot(
            article_embeddings,
            question_embedding
        )

        top_indices = (
            np.argsort(scores)[-top_k:][::-1]
        )

        results = []

        for index in top_indices:

            article = articles[int(index)].copy()

            article["similarity_score"] = float(
                scores[index]
            )

            results.append(article)

        return results