from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
)
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGsearch
import os

app = Flask(__name__)
CORS(app, origins="https://rag-tutorial-three.vercel.app/")  
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "txt", "csv", "docx", "json", "xls", "xlsx"}

def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize RAG components once when the app starts
print("Initializing RAG system...")
try:
    # Optional: Load documents if the index doesn't exist
    # if not os.path.exists("faiss_index"):
    #     print("Building vector store from documents...")
    #     docs = load_all_documents("data")
    #     store = FaissVectorStore()
    #     store.build_from_documents(docs)
    #     store.save("faiss_index") # Assuming your vector store has a save method

    # Load the pre-built vector store
    # store = FaissVectorStore()
    # store.load() # Ensure this path matches where your index is saved
    
    # Initialize the main RAG searcher
    rag_search = RAGsearch()
    print("RAG system initialized successfully.")
except Exception as e:
    print(f"Error initializing RAG system: {e}")
    rag_search = None

@app.route('/api/query', methods=['POST'])
def query_rag():
    if not rag_search:
        return jsonify({"error": "RAG system is not initialized."}), 500

    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body."}), 400

    query = data['query']
    top_k = data.get('top_k', 3)

    try:
        summary = rag_search.search_and_summarize(query, top_k=top_k)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "rag_initialized": rag_search is not None}), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if not rag_search:
        return jsonify({"error": "RAG system is not initialized."}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type."}), 400

    filename = secure_filename(file.filename)
    save_path = DATA_DIR / filename
    file.save(str(save_path))

    try:
        ext = save_path.suffix.lower()
        if ext == ".pdf":
            loader = PyMuPDFLoader(str(save_path))
        elif ext == ".txt":
            loader = TextLoader(str(save_path))
        elif ext == ".csv":
            loader = CSVLoader(str(save_path))
        elif ext == ".docx":
            loader = Docx2txtLoader(str(save_path))
        elif ext in (".xls", ".xlsx"):
            loader = UnstructuredExcelLoader(str(save_path))
        elif ext == ".json":
            loader = JSONLoader(str(save_path))
        else:
            return jsonify({"error": "Unsupported file type."}), 400

        docs = loader.load()
        rag_search.vectorstore.build_from_documents(docs)
        return jsonify({"message": "File uploaded and indexed.", "filename": filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)