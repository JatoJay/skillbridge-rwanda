import uuid
from fastapi import APIRouter, HTTPException
from models.candidate import ChatRequest, ChatResponse, ProfileFinalizeRequest, CandidateProfile
from services.gemini_service import gemini_service
from services.embedding_service import embedding_service
from services.vector_search import vector_search_service
from services.database import db

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())

        existing_messages = await db.get_chat_session(session_id)

        messages = [{"role": m.role, "content": m.content} for m in request.messages]

        result = await gemini_service.chat_profile(messages, request.language)

        all_messages = existing_messages + messages
        await db.save_chat_session(session_id, all_messages)

        extracted_profile = None
        if result.get("extracted_profile"):
            extracted_profile = CandidateProfile(**result["extracted_profile"])

        return ChatResponse(
            message=result["message"],
            session_id=session_id,
            profile_complete=result["profile_complete"],
            extracted_profile=extracted_profile
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/finalize")
async def finalize_profile(request: ProfileFinalizeRequest):
    try:
        messages = await db.get_chat_session(request.session_id)

        if not messages:
            raise HTTPException(status_code=404, detail="Session not found")

        result = await gemini_service.chat_profile(messages, "en")

        if not result.get("extracted_profile"):
            final_messages = messages + [{"role": "user", "content": "Please summarize my profile now."}]
            result = await gemini_service.chat_profile(final_messages, "en")

        profile_data = result.get("extracted_profile", {})

        profile_text = embedding_service.create_candidate_text(profile_data)
        embedding = await embedding_service.get_embedding(profile_text)
        profile_data["embedding"] = embedding

        candidate_id = await db.create_candidate(profile_data)

        await vector_search_service.index_candidate(candidate_id, embedding)

        return {
            "candidate_id": candidate_id,
            "profile": profile_data,
            "message": "Profile created successfully!"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    messages = await db.get_chat_session(session_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "messages": messages}
