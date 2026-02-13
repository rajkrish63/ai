import os
from typing import List, Dict, Optional

class DocumentService:
    """
    Handles document processing: text extraction and chunking.
    """
    
    def __init__(self, rag_dir: str = "rag"):
        self.rag_dir = rag_dir
        self.documents_dir = os.path.join(rag_dir, "documents")
        os.makedirs(self.documents_dir, exist_ok=True)
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except ImportError:
            return "Error: PyPDF2 not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"Error extracting PDF: {e}"
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except ImportError:
            return "Error: python-docx not installed. Run: pip install python-docx"
        except Exception as e:
            return f"Error extracting DOCX: {e}"
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            return f"Error reading TXT file: {e}"
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from supported file formats.
        
        Args:
            file_path: Path to document file
            
        Returns:
            Extracted text
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            return f"Error: Unsupported file format: {ext}"
    
    def chunk_text(self, text: str, chunk_size: int = 512, 
                   overlap: int = 50) -> List[str]:
        """
        Split text into chunks with overlap.
        
        Args:
            text: Input text
            chunk_size: Size of each chunk in tokens (approximated by words)
            overlap: Number of overlapping tokens between chunks
            
        Returns:
            List of text chunks
        """
        # Simple word-based chunking (approximates tokens)
        words = text.split()
        chunks = []
        
        if len(words) <= chunk_size:
            return [text]
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
            
            # Stop if we've processed all words
            if i + chunk_size >= len(words):
                break
        
        return chunks
    
    def process_document(self, file_path: str, doc_id: str) -> Dict:
        """
        Process a document: extract text and chunk it.
        
        Args:
            file_path: Path to document
            doc_id: Unique document ID
            
        Returns:
            Dictionary with document metadata and chunks
        """
        # Extract text
        text = self.extract_text(file_path)
        
        if text.startswith("Error"):
            return {"error": text}
        
        # Chunk text
        chunks = self.chunk_text(text)
        
        # Create metadata
        metadata = {
            "id": doc_id,
            "filename": os.path.basename(file_path),
            "file_path": file_path,
            "chunk_count": len(chunks),
            "chunks": chunks,
            "text_length": len(text)
        }
        
        return metadata
    
    def list_documents(self) -> List[Dict]:
        """List all processed documents."""
        documents = []
        if os.path.exists(self.documents_dir):
            for filename in os.listdir(self.documents_dir):
                if filename.endswith('.json'):
                    import json
                    try:
                        with open(os.path.join(self.documents_dir, filename), 'r') as f:
                            doc = json.load(f)
                            documents.append({
                                "id": doc.get("id"),
                                "filename": doc.get("filename"),
                                "chunk_count": doc.get("chunk_count", 0)
                            })
                    except:
                        pass
        return documents
