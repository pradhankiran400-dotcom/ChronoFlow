from data.documents import documents
from rag.pipeline import RAGPipeline


rag = RAGPipeline(documents)


question = input("Ask a question: ")


context = rag.get_context(question)


print("\nRelevant Information:\n")

print(context)