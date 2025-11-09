from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGsearch

if __name__ == "__main__":
    # docs = load_all_documents("data")
    store = FaissVectorStore()
    # store.build_from_documents(docs)
    store.load()
    print(store.query("What is my CGPA till 4th sem?", top_k = 3))

    rag_search = RAGsearch()
    query = "What is my CGPA till 4th sem?"
    summary = rag_search.search_and_summarize(query, top_k = 3)
    print("Summary: ", summary)
    
