from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import service, schemas, exceptions
from .dependencies import get_db
from agents.message.agent import get_app_name
from src.runner.runner import setup_session_and_runner, execute_agent

router = APIRouter()


@router.post(
    "/references",
    response_model=schemas.MessageReferenceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="메시지 레퍼런스 생성",
    description="새로운 메시지 레퍼런스를 생성합니다."
)
async def create_reference(ref: schemas.MessageReferenceCreate, db: Session = Depends(get_db)):
    return service.create_message_reference(db=db, ref=ref)


@router.get(
    "/references/{reference_id}",
    response_model=schemas.MessageReferenceResponse,
    summary="메시지 레퍼런스 상세 조회",
    description="특정 ID의 메시지 레퍼런스 정보를 조회합니다."
)
async def get_reference(reference_id: int, db: Session = Depends(get_db)):
    db_ref = service.get_message_reference(db=db, reference_id=reference_id)
    if db_ref is None:
        raise exceptions.MessageReferenceNotFound()
    return db_ref


@router.post(
    "/run_sse",
    response_model=schemas.EventResponse,
    status_code=status.HTTP_200_OK,
    summary="메시지 생성 워크플로우 진행",
    description="SSE 기반 에이전트의 응답을 스트리밍합니다."
)
async def run_agent_sse(req: schemas.MessageAgentRequest) -> StreamingResponse:
    app_name = get_app_name()
    try:
        session_id, runner = await setup_session_and_runner(
            app_name=app_name,
            user_id=req.user_id,
            session_id=req.session_id,
            state_config=req.config.model_dump(mode="json")
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return StreamingResponse(
        execute_agent(
            user_id=req.user_id,
            session_id=session_id,
            runner=runner
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post(
    "/get_sse_report",
    response_model=None,
    status_code=status.HTTP_200_OK,
    summary="메시지 생성 워크플로우 리포트 조회",
    description="SSE 기반 에이전트의 최종 리포트를 조회합니다."
)
async def get_sse_report(req: schemas.MessageAgentRequest) -> Response:
    app_name = get_app_name()
    try:
        session_id, runner = await setup_session_and_runner(
            app_name=app_name,
            user_id=req.user_id,
            session_id=req.session_id,
            state_config=req.config.model_dump(mode="json")
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    try:
        events = []
        async for event in execute_agent(
            user_id=req.user_id,
            session_id=session_id,
            runner=runner
        ):
            events.append(event)
        
        if not events:
            raise HTTPException(status_code=500, detail="에이전트로부터 응답을 받지 못했습니다.")
            
        last_event_str = events[-1]
        
        # SSE 포맷 (data: {json}\n\n)에서 JSON 추출
        import json
        json_str = last_event_str.replace("data: ", "").strip()
        last_event_data = json.loads(json_str)
        
        if last_event_data.get("event_status") != schemas.EventStatus.COMPLETE:
            raise HTTPException(status_code=400, detail="Agent is not complete")
        
        return Response(
            content=json.dumps(last_event_data, ensure_ascii=False),
            media_type="application/json",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        