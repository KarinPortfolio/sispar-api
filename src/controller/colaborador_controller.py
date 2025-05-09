from flask import Blueprint, jsonify, request
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import checar_senha, hash_senha
from flasgger import swag_from

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@bp_colaborador.route('/todos-colaboradores')
@swag_from('../docs/colaborador/listar_colaborador.yml')

def pegar_dados_todos_colaboradores():
    try:
        colaboradores = db.session.execute(
            db.select(Colaborador)
        ).scalars().all()

        if not colaboradores:
            return jsonify({'response': 'Não há colaboradores cadastrados.'}), 404

        colaboradores = [colaborador.all_data() for colaborador in colaboradores]
        return jsonify(colaboradores), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhe': str(error)}), 500

@bp_colaborador.route('/cadastrar', methods=['POST'])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')

def cadastrar_colaborador():
    dados_requisicao = request.get_json()

    if not dados_requisicao or not all(k in dados_requisicao for k in ('nome', 'email', 'senha', 'cargo', 'salario')):
        return jsonify({'mensagem': 'Dados não inseridos. Preencha todos os campos obrigatórios (nome, email, senha, cargo, salario).'}), 400

    email = dados_requisicao.get('email')
    if colaborador_existente := db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar():
        # Log or handle the case where the user already exists
        print('Usuário já existe')
        return jsonify({'mensagem': 'Email já existe.'}), 500
    else:
        novo_colaborador = Colaborador(
            nome=dados_requisicao.get('nome'),
            email=dados_requisicao.get('email'),
            senha=hash_senha(dados_requisicao['senha']), # A senha é hasheada AQUI
            cargo=dados_requisicao.get('cargo'),
            salario=dados_requisicao.get('salario')
        )
        db.session.add(novo_colaborador)
        db.session.commit()
        return jsonify({'mensagem': 'Colaborador cadastrado com sucesso', 'colaborador': novo_colaborador.all_data()}), 201


@bp_colaborador.route('/login', methods=['POST'])
@swag_from('../docs/colaborador/login.yml')
def login():
    dados_requisicao = request.get_json()
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')

    if not email or not senha:
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400

    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar()

    if not colaborador:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

    if checar_senha(senha, colaborador.senha):
        return jsonify({'mensagem': 'Login realizado com sucesso.'}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas.'}), 401


@bp_colaborador.route('/atualizar/<int:colaborador_id>', methods=['PUT'])
@swag_from('../docs/colaborador/atualizar_colaborador.yml')
def atualizar_colaborador(colaborador_id):
    dados_atualizacao = request.get_json()

    if not dados_atualizacao:
        return jsonify({'mensagem': 'Dados para atualização não fornecidos.'}), 400

    colaborador = db.session.get(Colaborador, colaborador_id)

    if not colaborador:
        return jsonify({'mensagem': f'Colaborador com ID {colaborador_id} não encontrado.'}), 404

    if 'nome' in dados_atualizacao:
        colaborador.nome = dados_atualizacao['nome']
    if 'cargo' in dados_atualizacao:
        colaborador.cargo = dados_atualizacao['cargo']
    if 'salario' in dados_atualizacao:
        colaborador.salario = dados_atualizacao['salario']
    if 'senha' in dados_atualizacao:
        colaborador.senha = hash_senha(dados_atualizacao['senha']) # A senha é hasheada AQUI
    if 'email' in dados_atualizacao:
        colaborador.email = dados_atualizacao['email']

    db.session.commit()
    return jsonify({'mensagem': f'Dados do colaborador com ID {colaborador_id} atualizado com sucesso.', 'colaborador': colaborador.all_data()}), 200

@bp_colaborador.route('/deletar/<int:colaborador_id>', methods=['DELETE'])
@swag_from('../docs/colaborador/deletar_colaborador.yml')
def deletar_colaborador(colaborador_id):
    colaborador = db.session.get(Colaborador, colaborador_id)

    if not colaborador:
        return jsonify({'mensagem': f'Colaborador com ID {colaborador_id} não encontrado.'}), 404

    db.session.delete(colaborador)
    db.session.commit()
    return jsonify({'mensagem': f'Colaborador com ID {colaborador_id} deletado com sucesso.'}), 200