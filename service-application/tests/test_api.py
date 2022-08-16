import pytest
import mock
from http import HTTPStatus
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestApplicationPostAPI:
    @pytest.mark.usefixtures("db_connection", "mock_settings")
    @mock.patch('src.main.rmq_client')
    def test_create_application_success(self, mocker):
        post_data = {"first_name": "A", "last_name": "B"}
        response = client.post("/application/", json=post_data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "success": True,
            "application_id": response.json()["application_id"]
        }

    @pytest.mark.usefixtures("db_connection", "mock_settings")
    def test_create_application_failed_with_missing_first_name(self):
        post_data = {"last_name": "B"}
        response = client.post("/application/", json=post_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "first_name"]
        assert response.json()["detail"][0]["msg"] == "field required"

    @pytest.mark.usefixtures("db_connection", "mock_settings")
    def test_create_application_failed_with_missing_last_name(self):
        post_data = {"first_name": "A"}
        response = client.post("/application/", json=post_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "last_name"]
        assert response.json()["detail"][0]["msg"] == "field required"


class TestApplicationGetAPI:
    @pytest.mark.usefixtures("db_connection", "mock_settings")
    def test_get_application_by_status(self):
        response = client.get("/applications/completed")

        assert response.status_code == HTTPStatus.OK
        assert response.json()["success"] == True
        for row in response.json()["data"]:
            assert row["status"] == "completed"

    @pytest.mark.usefixtures("db_connection", "mock_settings")
    def test_get_application_by_id(self):
        response = client.get("/application/66cd16f4-2d68-49ae-a15a-71b9de47ac19")

        assert response.status_code == HTTPStatus.OK
        assert response.json()["data"]["id"] == "66cd16f4-2d68-49ae-a15a-71b9de47ac19"
