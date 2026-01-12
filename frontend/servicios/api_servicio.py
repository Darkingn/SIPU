import requests

BASE_URL = "http://localhost:8000"

class ApiService:

    @staticmethod
    def post(endpoint, data):
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get(endpoint):
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
