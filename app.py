from src.data_loader import load_all_documents
from src.embedding import EmbeddingPipeline
# from src.vectorstore import FaissVectorStore
# from src.search import RAGsearch

if __name__ == "__main__":
    docs = load_all_documents("data")
    pipe = EmbeddingPipeline()
    chunks = pipe.chunk_documents(docs)
    chunkvectors = pipe.embed_chunks(chunks)
    print(chunkvectors)
    print(chunkvectors)