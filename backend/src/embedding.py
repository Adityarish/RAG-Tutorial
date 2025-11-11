from typing import List, Union
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
import numpy as np
from src.data_loader import load_all_documents


class EmbeddingPipeline:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = SentenceTransformer(model_name)
        print(f"[INFO] Loaded embedding model: {model_name}")

    def chunk_documents(self, documents: List[Union[str, Document]]) -> List[Document]:
        """
        Splits text documents into smaller chunks suitable for embedding.
        Accepts either plain strings or LangChain Document objects.
        """
        if not documents:
            print("[WARN] No documents provided for chunking.")
            return []

        # Convert string inputs to LangChain Document objects
        if isinstance(documents[0], str):
            documents = [Document(page_content=doc) for doc in documents]

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = splitter.split_documents(documents)
        print(f"[INFO] Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks

    def embed_chunks(self, chunks: List[Document]) -> np.ndarray:
        """
        Generates embeddings for each text chunk.
        """
        if not chunks:
            print("[WARN] No chunks provided for embedding.")
            return np.array([])

        texts = [chunk.page_content for chunk in chunks]
        print(f"[INFO] Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"[INFO] Embeddings shape: {embeddings.shape}")
        return embeddings
