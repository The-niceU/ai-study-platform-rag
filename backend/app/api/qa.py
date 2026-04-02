from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.qa import QARequest, QAResponse
from app.services.prompt_builder import build_qa_prompt
from app.services.retriever import retrieve_chunks
from app.services.llm_service import generate_answer

router = APIRouter(prefix="/qa", tags=["qa"])


@router.post("/", response_model=QAResponse)
def ask_question(
    data: QARequest,
    current_user: User = Depends(get_current_user),
):
    try:
        print("QA START")
        print("query =", data.query)
        print("top_k =", data.top_k)

        retrieved_chunks = retrieve_chunks(data.query, top_k=data.top_k)
        print("retrieved_chunks count =", len(retrieved_chunks))

        prompt = build_qa_prompt(data.query, retrieved_chunks)
        print("prompt built")

        answer = generate_answer(prompt)
        print("answer generated")

        return {
            "answer": answer,
            "sources": retrieved_chunks,
        }
    except Exception as e:
        print("QA ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))