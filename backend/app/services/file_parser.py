import os
from docx import Document as DocxDocument
import fitz  # PyMuPDF


def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def parse_pdf(file_path: str) -> str:
    text = []
    pdf = fitz.open(file_path)
    for page in pdf:
        text.append(page.get_text())
    pdf.close()
    return "\n".join(text)


def parse_docx(file_path: str) -> str:
    doc = DocxDocument(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])


def parse_file(file_path: str, file_type: str) -> str:
    file_type = file_type.lower()

    if file_type == "txt":
        return parse_txt(file_path)
    elif file_type == "pdf":
        return parse_pdf(file_path)
    elif file_type == "docx":
        return parse_docx(file_path)
    else:
        raise ValueError(f"暂不支持的文件类型: {file_type}")