from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.search import SearchRequest
from app.services.retriever import retrieve_chunks

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/")
def search_chunks(
    data: SearchRequest,
    current_user: User = Depends(get_current_user),
):
    results = retrieve_chunks(data.query, top_k=data.top_k)
    return results