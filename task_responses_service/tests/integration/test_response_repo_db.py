import pytest
from uuid import uuid4
from app.repositories.response_repo import ResponseRepository
from app.schemas.response import Response

class TestResponseRepoIntegration:
    """Интеграционные тесты репозитория откликов с реальной PostgreSQL БД"""

    @pytest.fixture
    def response_repo(self, session):
        return ResponseRepository(session)

    def test_create_and_retrieve_response(self, response_repo):
        """Создание и поиск отклика"""
        task_title = "integration_task"
        user_id = uuid4()
        text = "Integration test response"

        # Создание отклика
        response = response_repo.create_response(task_title, user_id, text)
        assert response.task_title == task_title
        assert response.user_id == user_id
        assert response.text == text
        assert response.status == "pending"

        # Поиск по ID
        found_response = response_repo.get_response_by_id(response.id)
        assert found_response.id == response.id
        assert found_response.text == text

        # Поиск по задаче
        task_responses = response_repo.get_responses_by_task(task_title)
        assert len(task_responses) == 1
        assert task_responses[0].id == response.id

    def test_update_response_status(self, response_repo):
        """Обновление статуса отклика"""
        response = response_repo.create_response("status_task", uuid4(), "Test text")

        updated_response = response_repo.update_response_status(response.id, "accepted")
        assert updated_response.status == "accepted"

        # Проверяем что статус сохранился в БД
        found_response = response_repo.get_response_by_id(response.id)
        assert found_response.status == "accepted"

    def test_error_handling(self, response_repo):
        """Обработка ошибок для несуществующих откликов"""
        non_existent_id = uuid4()

        with pytest.raises(ValueError, match="Response not found"):
            response_repo.get_response_by_id(non_existent_id)

        with pytest.raises(ValueError, match="Response not found"):
            response_repo.update_response_status(non_existent_id, "accepted")