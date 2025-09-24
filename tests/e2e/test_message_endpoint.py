from fastapi.testclient import TestClient
import pytest


def test_weather_messages(client: TestClient):
    weather_messages = ["RAINY", "SUNNY", "CLOUDY", "STORMY"]
    for msg in weather_messages:
        payload = {"content": msg}
        response = client.post("/api/v1/messages", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["is_ai"] == False


def test_food_messages(client: TestClient):
    food_messages = ["PIZZA", "PASTA", "ICECREAM", "BURGER"]
    for msg in food_messages:
        payload = {"content": msg}
        response = client.post("/api/v1/messages", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["is_ai"] == True
