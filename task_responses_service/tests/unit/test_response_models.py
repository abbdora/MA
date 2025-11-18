import pytest
from uuid import uuid4
from datetime import datetime
from app.schemas.response import Response, ResponseCreate


class TestResponseModels:
    def test_response_create_valid(self):
        """Создание модели ResponseCreate"""
        response_data = ResponseCreate(
            task_title="test_task",
            text="I can help with this task"
        )
        assert response_data.task_title == "test_task"
        assert response_data.text == "I can help with this task"

    def test_response_model_valid(self):
        """Создание полной модели Response"""
        response_id = uuid4()
        user_id = uuid4()
        now = datetime.utcnow()

        response = Response(
            id=response_id,
            task_title="test_task",
            user_id=user_id,
            text="Response text",
            status="pending",
            created_at=now,
            updated_at=now
        )
        assert response.id == response_id
        assert response.user_id == user_id
        assert response.status == "pending"