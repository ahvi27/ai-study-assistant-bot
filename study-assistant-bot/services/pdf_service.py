"""
PDF Processing Service
Extract text from PDF files
"""

from typing import Tuple, Optional, List
from pathlib import Path
import fitz  # PyMuPDF
import pdfplumber
from utils.logger import logger


class PDFService:
    """Service for processing PDF documents"""

    @staticmethod
    def extract_text(file_path: str) -> Tuple[Optional[str], int]:
        """
        Extract all text from PDF file

        Args:
            file_path: Path to PDF file

        Returns:
            Tuple of (extracted_text, page_count) or (None, 0) if error
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                logger.error(f"PDF file not found: {file_path}")
                return None, 0

            if not file_path.suffix.lower() == ".pdf":
                logger.error(f"File is not a PDF: {file_path}")
                return None, 0

            # Use PyMuPDF for initial extraction
            try:
                doc = fitz.open(file_path)
                page_count = doc.page_count
                text = ""

                for page in doc:
                    text += page.get_text()

                doc.close()

                return text, page_count

            except Exception as e:
                logger.warning(f"PyMuPDF extraction failed, trying pdfplumber: {e}")

                # Fallback to pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    page_count = len(pdf.pages)
                    text = ""

                    for page in pdf.pages:
                        text += page.extract_text() or ""

                    return text, page_count

        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            return None, 0

    @staticmethod
    def extract_text_by_page(file_path: str) -> List[str]:
        """
        Extract text from each page separately

        Args:
            file_path: Path to PDF file

        Returns:
            List of text from each page
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                logger.error(f"PDF file not found: {file_path}")
                return []

            try:
                doc = fitz.open(file_path)
                pages = []

                for page in doc:
                    pages.append(page.get_text())

                doc.close()
                return pages

            except Exception as e:
                logger.warning(f"PyMuPDF extraction failed, trying pdfplumber: {e}")

                pages = []
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        pages.append(page.extract_text() or "")

                return pages

        except Exception as e:
            logger.error(f"Error extracting pages from PDF {file_path}: {e}")
            return []

    @staticmethod
    def extract_text_with_metadata(file_path: str) -> dict:
        """
        Extract text and metadata from PDF

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary with text and metadata
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return {"error": "File not found"}

            doc = fitz.open(file_path)

            metadata = doc.metadata
            page_count = doc.page_count
            text = ""

            for page in doc:
                text += page.get_text()

            doc.close()

            return {
                "text": text,
                "page_count": page_count,
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
            }

        except Exception as e:
            logger.error(f"Error extracting metadata from PDF: {e}")
            return {"error": str(e)}

    @staticmethod
    def extract_tables(file_path: str) -> List[dict]:
        """
        Extract tables from PDF

        Args:
            file_path: Path to PDF file

        Returns:
            List of extracted tables
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return []

            tables = []

            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()

                    if page_tables:
                        for table in page_tables:
                            tables.append({
                                "page": page_num + 1,
                                "data": table,
                            })

            return tables

        except Exception as e:
            logger.error(f"Error extracting tables from PDF: {e}")
            return []

    @staticmethod
    def get_page_images(file_path: str) -> List[dict]:
        """
        Extract images from PDF

        Args:
            file_path: Path to PDF file

        Returns:
            List of image information
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return []

            images = []
            doc = fitz.open(file_path)

            for page_num, page in enumerate(doc):
                image_list = page.get_images()

                for image_index, img in enumerate(image_list):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)

                    images.append({
                        "page": page_num + 1,
                        "index": image_index,
                        "width": pix.width,
                        "height": pix.height,
                        "colorspace": pix.colorspace.name,
                    })

            doc.close()
            return images

        except Exception as e:
            logger.error(f"Error extracting images from PDF: {e}")
            return []

    @staticmethod
    def is_valid_pdf(file_path: str) -> bool:
        """
        Check if file is a valid PDF

        Args:
            file_path: Path to file

        Returns:
            True if valid PDF, False otherwise
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return False

            if not file_path.suffix.lower() == ".pdf":
                return False

            # Try to open and verify
            doc = fitz.open(file_path)
            doc.close()
            return True

        except Exception:
            return False

    @staticmethod
    def get_pdf_info(file_path: str) -> dict:
        """
        Get PDF information

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary with PDF info
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return {"error": "File not found"}

            doc = fitz.open(file_path)

            info = {
                "page_count": doc.page_count,
                "metadata": doc.metadata,
                "is_pdf": True,
                "file_size": file_path.stat().st_size,
            }

            doc.close()
            return info

        except Exception as e:
            logger.error(f"Error getting PDF info: {e}")
            return {"error": str(e)}

    @staticmethod
    def clean_extracted_text(text: str) -> str:
        """
        Clean extracted text

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = " ".join(text.split())

        # Remove common OCR artifacts
        text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")

        # Remove multiple consecutive punctuation
        import re
        text = re.sub(r"\.{2,}", ".", text)
        text = re.sub(r"\s{2,}", " ", text)

        return text
