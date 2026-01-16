import os
import pdfplumber

_DOCX_IMPORT_ERROR = None
try:
    from docx import Document as DocxDocument
except ModuleNotFoundError as exc:
    DocxDocument = None
    missing_name = getattr(exc, "name", None)
    if missing_name == "exceptions":
        _DOCX_IMPORT_ERROR = (
            "Detected the deprecated 'docx' package. Run `pip uninstall docx` and `pip install python-docx`."
        )
    else:
        _DOCX_IMPORT_ERROR = "Unable to import python-docx; install it via `pip install python-docx`."

class TextExtractorService:
    
    @staticmethod
    def extract_text(file_path: str) -> str :
        extension = os.path.splitext(file_path)[1].lower()

        if extension == '.pdf':
            return TextExtractorService._extract_text_from_pdf(file_path)
        elif extension in ['.docx', '.doc']:
            return TextExtractorService._extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
        
    @staticmethod
    def _extract_text_from_pdf(file_path: str) -> str:
        text_content = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        return "\n".join(text_content)
    
    @staticmethod
    def _extract_text_from_docx(file_path: str) -> str:
        if DocxDocument is None:
            raise ImportError(_DOCX_IMPORT_ERROR or "python-docx is required to parse DOC/DOCX files.")
        document = DocxDocument(file_path)
        paragraphs = [para.text for para in document.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
