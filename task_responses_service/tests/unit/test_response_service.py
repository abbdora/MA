import pytest
import asyncio
from unittest.mock import Mock, patch
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from app.services.response_service import ResponseService
from app.schemas.response import Response, ResponseCreate

class TestResponseService:
    @pytest.fixture
    def response_service(self):
        mock_repo = Mock()
        with patch.object(ResponseService, '__init__', lambda self, repo: setattr(self, 'repo', repo)):
            return ResponseService(mock_repo)

    def test_create_response_success(self, response_service):
        """Создание отклика"""
        user_id = uuid4()
        task_title = "test_task"
        response_data = ResponseCreate(task_title=task_title, text="I can help")

        now = datetime.utcnow()
        mock_response = Response(
            id=uuid4(), task_title=task_title, user_id=user_id,
            text="I can help", status="pending",
            created_at=now, updated_at=now
        )
        response_service.repo.get_responses_by_task.return_value = []
        response_service.repo.create_response.return_value = mock_response

        # Запускаем асинхронную функцию
        result = asyncio.run(response_service.create_response(response_data, user_id))

        assert result.task_title == task_title
        response_service.repo.create_response.assert_called_once()

    def test_create_response_duplicate(self, response_service):
        """Попытка создать дублирующий отклик"""
        user_id = uuid4()
        task_title = "test_task"
        response_data = ResponseCreate(task_title=task_title, text="I can help")

        now = datetime.utcnow()
        existing_response = Response(
            id=uuid4(), task_title=task_title, user_id=user_id,
            text="Existing response", status="pending",
            created_at=now, updated_at=now
        )
        response_service.repo.get_responses_by_task.return_value = [existing_response]

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(response_service.create_response(response_data, user_id))

        assert exc_info.value.status_code == 400

    def test_start_work_permission_denied(self, response_service):
        """Попытка начать работу не автором отклика"""
        response_id = uuid4()
        user_id = uuid4()

        now = datetime.utcnow()
        mock_response = Response(
            id=response_id, task_title="test_task", user_id=uuid4(),  # другой user_id
            text="Response text", status="accepted",
            created_at=now, updated_at=now
        )
        response_service.repo.get_response_by_id.return_value = mock_response

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(response_service.start_work(response_id, user_id))

        assert exc_info.value.status_code == 403