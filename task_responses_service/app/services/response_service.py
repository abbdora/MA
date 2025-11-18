from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.response_repo import ResponseRepository
from app.schemas.response import Response, ResponseCreate, ResponseList


class ResponseService:
    def __init__(self, db: Session):
        self.repo = ResponseRepository(db)

    async def create_response(self, response_data: ResponseCreate, user_id: UUID) -> Response:
        existing_responses = self.repo.get_responses_by_task(response_data.task_title)
        user_responses = [r for r in existing_responses if r.user_id == user_id]

        if user_responses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already responded to this task"
            )

        return self.repo.create_response(
            task_title=response_data.task_title,
            user_id=user_id,
            text=response_data.text
        )

    async def get_task_responses(self, task_id: UUID, current_user_id: UUID,
                                 is_task_author: bool = False) -> ResponseList:
        responses = self.repo.get_responses_by_task(task_id)

        if not is_task_author:
            responses = [r for r in responses if r.user_id == current_user_id]

        return ResponseList(items=responses, total=len(responses))

    async def accept_response(self, response_id: UUID, current_user_id: UUID) -> Response:
        response = self.repo.get_response_by_id(response_id)

        is_author = await self._check_task_author(response.task_title, current_user_id)
        if not is_author:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only task author can accept responses"
            )

        accepted_response = self.repo.update_response_status(response_id, "accepted")

        self.repo.reject_other_responses(response.task_title, response_id)

        return accepted_response

    async def _check_task_author(self, task_title: str, user_id: UUID) -> bool:
        return True

    async def reject_response(self, response_id: UUID, current_user_id: UUID) -> Response:
        response = self.repo.get_response_by_id(response_id)

        is_author = await self._check_task_author(response.task_title, current_user_id)
        if not is_author:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only task author can reject responses"
            )

        return self.repo.update_response_status(response_id, "rejected")

    async def start_work(self, response_id: UUID, user_id: UUID) -> Response:
        response = self.repo.get_response_by_id(response_id)

        if response.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only response author can start work"
            )

        if response.status != "accepted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only start work on accepted responses"
            )

        return self.repo.update_response_status(response_id, "in_progress")

    async def complete_work(self, response_id: UUID, user_id: UUID) -> Response:
        response = self.repo.get_response_by_id(response_id)

        if response.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only response author can complete work"
            )

        if response.status != "in_progress":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only complete work that is in progress"
            )

        return self.repo.update_response_status(response_id, "completed")

    async def approve_work(self, response_id: UUID, user_id: UUID) -> Response:
        response = self.repo.get_response_by_id(response_id)

        is_author = await self._check_task_author(response.task_title, user_id)
        if not is_author:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only task author can approve work"
            )

        if response.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only approve completed work"
            )

        return self.repo.update_response_status(response_id, "approved")

    async def request_revision(self, response_id: UUID, user_id: UUID) -> Response:
        response = self.repo.get_response_by_id(response_id)

        is_author = await self._check_task_author(response.task_title, user_id)
        if not is_author:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only task author can request revision"
            )

        if response.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only request revision for completed work"
            )

        return self.repo.update_response_status(response_id, "needs_revision")