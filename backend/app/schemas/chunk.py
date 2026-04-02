from datetime import datetime
from pydantic import BaseModel


class ChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    content: str
    page_num: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True