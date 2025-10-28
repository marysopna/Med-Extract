from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingestion import process_upload

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        chunks = await process_upload(file)
        return {"status": "success", "chunks_uploaded": len(chunks)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")