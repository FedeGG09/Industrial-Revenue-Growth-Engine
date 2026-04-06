import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_data",
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.leads = self.client.get_or_create_collection(settings.chroma_collection_leads)
        self.policies = self.client.get_or_create_collection(settings.chroma_collection_policies)

    def upsert_leads(self, ids, documents, metadatas, embeddings=None):
        kwargs = {"ids": ids, "documents": documents, "metadatas": metadatas}
        if embeddings is not None:
            kwargs["embeddings"] = embeddings
        self.leads.upsert(**kwargs)

    def search_leads(self, query_text: str, n_results: int = 5):
        return self.leads.query(query_texts=[query_text], n_results=n_results)
