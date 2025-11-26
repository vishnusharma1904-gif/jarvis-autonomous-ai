"""
Document Processor for PDF and DOCX files
"""

import io
from typing import Optional
from PyPDF2 import PdfReader
from docx import Document

def read_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_bytes: PDF file bytes
    
    Returns:
        Extracted text
    """
    try:
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PdfReader(pdf_file)
        
        text_parts = []
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                text_parts.append(f"--- Page {page_num + 1} ---\n{text}")
        
        return "\n\n".join(text_parts) if text_parts else "No text extracted from PDF"
    
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def read_docx(file_bytes: bytes) -> str:
    """
    Extract text from DOCX file
    
    Args:
        file_bytes: DOCX file bytes
    
    Returns:
        Extracted text
    """
    try:
        docx_file = io.BytesIO(file_bytes)
        doc = Document(docx_file)
        
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        
        return "\n\n".join(text_parts) if text_parts else "No text extracted from DOCX"
    
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def process_document(file_bytes: bytes, filename: str) -> Optional[str]:
    """
    Process document based on file extension
    
    Args:
        file_bytes: File bytes
        filename: Name of file
    
    Returns:
        Extracted text or None
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return read_pdf(file_bytes)
    elif filename_lower.endswith('.docx'):
        return read_docx(file_bytes)
    else:
        return None
