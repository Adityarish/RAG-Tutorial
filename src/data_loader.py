from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
)
from langchain_community.document_loaders.excel import UnstructuredExcelLoader

def load_all_documents(data_dir: str) -> List[Any]:
    """
    Load all supported files from the data directory and convert to langchain document structure
    Supported: PDF, TXT, CSV, Excel, Word, JSON
    """

    data_path = Path(data_dir).resolve()
    print(f"[DEBUG] Data Path: {data_path}")
    documents = []

    # PDF files
    pdf_files = list(data_path.glob("**/*.pdf"))
    print(f"[DEBUG] Found {len(pdf_files)} PDF Files : {[str(f) for f in pdf_files]}")
    for pdf_file in pdf_files:
        print(f"[DEBUG] Loading pdf :{pdf_file}")
        try:
            loader = PyMuPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f"[DEBUG] loaded {len(loaded)} pdf from {pdf_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[Error] Failed to load PDF {pdf_file}: {e}")

    # Text files
    text_files = list(data_path.glob("**/*.txt"))
    print(f"[DEBUG] Found {len(text_files)} Text Files : {[str(f) for f in text_files]}")
    for text_file in text_files:
        print(f"[DEBUG] Loading text file :{text_file}")
        try:
            loader = TextLoader(str(text_file))
            loaded = loader.load()
            print(f"[DEBUG] loaded {len(loaded)} text from {text_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[Error] Failed to load Text File {text_file}: {e}")

    # CSV files
    csv_files = list(data_path.glob("**/*.csv"))
    print(f"[DEBUG] Found {len(csv_files)} CSV Files : {[str(f) for f in csv_files]}")
    for csv_file in csv_files:
        print(f"[DEBUG] Loading csv file :{csv_file}")
        try:
            loader = CSVLoader(str(csv_file))
            loaded = loader.load()
            print(f"[DEBUG] loaded {len(loaded)} csv from {csv_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[Error] Failed to load CSV File {csv_file}: {e}")

    # Excel files
    excel_files = []
    excel_files.extend(list(data_path.glob("**/*.xls")))
    excel_files.extend(list(data_path.glob("**/*.xlsx")))
    print(f"[DEBUG] Found {len(excel_files)} Excel Files : {[str(f) for f in excel_files]}")
    for excel_file in excel_files:
        print(f"[DEBUG] Loading excel file :{excel_file}")
        try:
            loader = UnstructuredExcelLoader(str(excel_file))
            loaded = loader.load()
            print(f"[DEBUG] loaded {len(loaded)} excel from {excel_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[Error] Failed to load Excel File {excel_file}: {e}")

    # Word files
    docx_files = list(data_path.glob("**/*.docx"))
    print(f"[DEBUG] Found {len(docx_files)} Word Files : {[str(f) for f in docx_files]}")
    for docx_file in docx_files:
        print(f"[DEBUG] Loading word file :{docx_file}")
        try:
            loader = Docx2txtLoader(str(docx_file))
            loaded = loader.load()
            print(f"[DEBUG] loaded {len(loaded)} word from {docx_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[Error] Failed to load Word File {docx_file}: {e}")

    # JSON files
    json_files = list(data_path.glob("**/*.json"))
    print(f"[DEBUG] Found {len(json_files)} JSON Files : {[str(f) for f in json_files]}")
    for json_file in json_files:
        print(f"[DEBUG] Loading json file :{json_file}")
        try:
            loader = JSONLoader(str(json_file))
            loaded = loader.load()
            print(f"[DEBUG] loaded {len(loaded)} json from {json_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[Error] Failed to load JSON File {json_file}: {e}")

    # SQL files (as text)
    sql_files = list(data_path.glob("**/*.sql"))
    print(f"[DEBUG] Found {len(sql_files)} SQL Files : {[str(f) for f in sql_files]}")
    for sql_file in sql_files:
        print(f"[DEBUG] Loading sql file :{sql_file}")
        try:
            loader = TextLoader(str(sql_file))
            loaded = loader.load()
            print(f"[DEBUG] loaded {len(loaded)} sql from {sql_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[Error] Failed to load SQL File {sql_file}: {e}")

    return documents