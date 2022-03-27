from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hola Mundo de los SUPERHeroes: Secret Value"}

def test_read_v1():
    response = client.get("/first/")
    assert response.status_code == 200
    assert response.json() == {"message": "Esta es la versión 1.0\nEstá apenas en construcción"}

#def test_read_heroes():
#    response = client.get("/first/heroes/")
#    assert response.status_code == 200
#    assert response.json() == {"message": "Get Heroes!"}