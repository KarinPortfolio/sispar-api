import pytest
from src.app import create_app
from src.model.colaborador_model import Colaborador
import time


#------------------------CONFIGURAÇÕES--------------------------------------

@pytest.fixture # Configurar os testes
def app():
    app = create_app()
    yield app # Armazenar o valor em memória
    
@pytest.fixture # Configura nossos testes de requisição
def client(app):
    return app.test_client()
#----------------------------------------------------------------------------

def test_pegar_todos_colaboradores(client):
    resposta = client.get('/colaborador/todos-colaboradores') 
    assert resposta.status_code == 200
    assert isinstance(resposta.json, list)

def test_desempenho_requisicao_get(client):
    comeco = time.time() # Pega  a hora atual e transforma em segundos
    
    for _ in range(100): # _ omite a variavel auxiliar
        resposta = client.get('/colaborador/todos-colaboradores') 
    
    fim = time.time() - comeco
    
    assert fim < 0.1 # Segundos
    

