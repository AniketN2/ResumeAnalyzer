from langchain_community.document_loaders import PyPDFLoader

def extract_text_from_pdf(pdf_path):
    text = ""
    page_count = 0

    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        page_count = len(docs)
        
        for doc in docs:
            text += doc.page_content + "\n"

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return text, page_count