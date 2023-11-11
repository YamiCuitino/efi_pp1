import pytest

from app import app, db
from app.models.models import Pais

#creamos un cliente para hacer el test
@pytest.fixture #queda definido para todos los test
def cliente():
    with app.app_context():
        db.create_all()
    cliente= app.test_client()
    yield cliente #como el return pero no frena el proceso, continua aunque falle lo que esta abajo
    with app.app_context():
        db.session.rollback() #ejecta cambioisn en la base de datos cuando termina los test deshace los cambios


def test_get_all_paises_fail(cliente):
    response = cliente.get('/api/v1/pais')
    import ipdb; ipdb.set_trace()
    assert response.status_code== 200

def test_get_all_paises(cliente):
    response = cliente.get('/pais')

    data = response.json()
   # assert len(data)== 5
    assert data[2] == dict (id=1, nombre="Argentina")
    assert response.status_code == 200

def test_create_pais(cliente):
    data = dict(nombre="Japon")
    responde = cliente.post("/pais", json=data)
    assert response.status_code == 201

    with app.app_ccontext():
        pais = Pais.quey.last()
    assert pais.nombre== "Japon"



