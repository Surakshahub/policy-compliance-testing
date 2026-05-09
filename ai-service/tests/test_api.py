import pytest
from app import app


@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):

    response = client.get("/")

    assert response.status_code == 200


def test_health(client):

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "UP"


def test_metrics(client):

    response = client.get("/metrics")

    assert response.status_code == 200


def test_describe_success(client):

    response = client.post(
        "/describe",
        json={
            "text": "Sensitive customer data exposed publicly"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


def test_describe_empty(client):

    response = client.post(
        "/describe",
        json={}
    )

    assert response.status_code == 400


def test_describe_malicious(client):

    response = client.post(
        "/describe",
        json={
            "text": "<script>alert('hack')</script>"
        }
    )

    assert response.status_code == 400


def test_recommend_success(client):

    response = client.post(
        "/recommend",
        json={
            "text": "Employee passwords stored in plain text"
        }
    )

    assert response.status_code == 200


def test_generate_report_success(client):

    response = client.post(
        "/generate-report",
        json={
            "text": "Financial customer records exposed publicly"
        }
    )

    assert response.status_code == 200