from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.response import Response, ResponseCreate, ResponseList
from app.services.response_service import ResponseService
from app.services.auth_client import AuthClient
from app.database import get_db

router = APIRouter(prefix="/responses", tags=["Responses"])
security = HTTPBearer()
auth_client = AuthClient()

async def get_current_user(token: str = Depends(security)):
    user_data = await auth_client.verify_token(token.credentials)
    return user_data

def get_response_service(db: Session = Depends(get_db)) -> ResponseService:
    return ResponseService(db)

@router.post("/", response_model=Response)
async def create_response(
    response_data: ResponseCreate,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.create_response(response_data, UUID(current_user["id"]))

@router.get("/tasks/{task_title}/responses", response_model=ResponseList)
async def get_task_responses(
    task_title: str,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.get_task_responses(
        task_title,
        UUID(current_user["id"]),
        is_task_author=False
    )

@router.post("/{response_id}/accept", response_model=Response)
async def accept_response(
    response_id: UUID,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.accept_response(response_id, UUID(current_user["id"]))

@router.post("/{response_id}/reject", response_model=Response)
async def reject_response(
    response_id: UUID,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.reject_response(response_id, UUID(current_user["id"]))

@router.post("/{response_id}/start", response_model=Response)
async def start_work(
    response_id: UUID,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.start_work(response_id, UUID(current_user["id"]))

@router.post("/{response_id}/complete", response_model=Response)
async def complete_work(
    response_id: UUID,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.complete_work(response_id, UUID(current_user["id"]))

@router.post("/{response_id}/approve", response_model=Response)
async def approve_work(
    response_id: UUID,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.approve_work(response_id, UUID(current_user["id"]))

@router.post("/{response_id}/request_revision", response_model=Response)
async def request_revision(
    response_id: UUID,
    current_user: dict = Depends(get_current_user),
    response_service: ResponseService = Depends(get_response_service)
):
    return await response_service.request_revision(response_id, UUID(current_user["id"]))