import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.schemas.chunk import ChunkResponse
from app.services.file_parser import parse_file
from app.services.chunker import split_text
from app.services.retriever import rebuild_chunk_index

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = "uploads"


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else "unknown"
    unique_name = f"{uuid4().hex}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        user_id=current_user.id,
        file_name=file.filename,
        file_type=file_ext,
        file_path=save_path,
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    try:
        text = parse_file(save_path, file_ext)
        chunks = split_text(text)

        for idx, chunk_text in enumerate(chunks):
            chunk = Chunk(
                document_id=new_doc.id,
                chunk_index=idx,
                content=chunk_text,
                page_num=None,
            )
            db.add(chunk)

        db.commit()
        rebuild_chunk_index(db)

    except Exception as e:
        print("FILE PARSE ERROR:", repr(e))

    return new_doc


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    docs = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )
    return docs


@router.get("/{document_id}/chunks", response_model=list[ChunkResponse])
def get_document_chunks(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id, Document.user_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")

    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_index.asc())
        .all()
    )
    return chunks

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id, Document.user_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")

    db.query(Chunk).filter(Chunk.document_id == document_id).delete()

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    rebuild_chunk_index(db)

    return {"message": "删除成功"}