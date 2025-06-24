# FLASKPROYECTO/proyecto_a/test_app.py
import pytest
from app import app # Importa la instancia de la aplicación Flask desde app.py

@pytest.fixture
def client():
    # Configura el cliente de prueba para la aplicación Flask
    app.config['TESTING'] = True # Activa el modo de prueba
    with app.test_client() as client:
        yield client

def test_saludo(client):
    # Prueba la ruta /saludo para verificar que devuelve el saludo correcto
    response = client.get('/saludo')
    assert response.status_code == 200
    assert b"Hola desde Proyecto A" in response.data

def test_recibir_get(client):
    # Prueba la ruta /recibir_get con un parámetro GET
    response = client.get('/recibir_get?mensaje=TestGET')
    assert response.status_code == 200
    assert b"GET: TestGET de Proyecto B" in response.data

def test_recibir_post(client):
    # Prueba la ruta /recibir_post enviando un JSON
    response = client.post('/recibir_post', json={"mensaje": "TestPOST"})
    assert response.status_code == 200
    assert b"POST: TestPOST de Proyecto B" in response.data