from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest
from app.services.rag import answer_question

router = APIRouter()

@router.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        answer = await answer_question(request.question)
        return {"answer": answer}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to generate answer")