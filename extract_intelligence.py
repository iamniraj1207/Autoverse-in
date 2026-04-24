import os
import json
import re
from PyPDF2 import PdfReader

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def build_knowledge_from_pdf():
    pdf_path = "howacarworks.pdf"
    if not os.path.exists(pdf_path):
        print("PDF not found.")
        return

    try:
        print("Extracting intelligence from howacarworks.pdf using PyPDF2...")
        reader = PdfReader(pdf_path)
        intelligence = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                intelligence.append({
                    "page": i + 1,
                    "content": clean_text(text)
                })
        
        with open("intelligence_corpus.json", "w") as f:
            json.dump(intelligence, f)
        print(f"Successfully processed {len(intelligence)} pages of technical data.")
    except Exception as e:
        print(f"Extraction failed: {e}")

if __name__ == "__main__":
    build_knowledge_from_pdf()
