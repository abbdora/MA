from uuid import UUID
from sqlalchemy.orm import Session
from app.models.response import ResponseDB
from app.schemas.response import Response


class ResponseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_response(self, task_title: str, user_id: UUID, text: str) -> Response:
        db_response = ResponseDB(
            task_title=task_title,
            user_id=user_id,
            text=text
        )
        self.db.add(db_response)
        self.db.commit()
        self.db.refresh(db_response)
        return Response.model_validate(db_response)

    def get_responses_by_task(self, task_title: str) -> list[Response]:
        db_responses = self.db.query(ResponseDB).filter(
            ResponseDB.task_title == task_title
        ).order_by(ResponseDB.created_at.desc()).all()
        return [Response.model_validate(resp) for resp in db_responses]

    def get_response_by_id(self, response_id: UUID) -> Response:
        db_response = self.db.query(ResponseDB).filter(
            ResponseDB.id == response_id
        ).first()
        if not db_response:
            raise ValueError("Response not found")
        return Response.model_validate(db_response)

    def update_response_status(self, response_id: UUID, status: str) -> Response:
        db_response = self.db.query(ResponseDB).filter(
            ResponseDB.id == response_id
        ).first()
        if not db_response:
            raise ValueError("Response not found")

        db_response.status = status
        self.db.commit()
        self.db.refresh(db_response)
        return Response.model_validate(db_response)

    def reject_other_responses(self, task_title: str, accepted_response_id: UUID) -> None:
        self.db.query(ResponseDB).filter(
            ResponseDB.task_title == task_title,
            ResponseDB.id != accepted_response_id,
            ResponseDB.status == "pending"
        ).update({"status": "rejected"})
        self.db.commit()