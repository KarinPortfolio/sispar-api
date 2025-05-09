from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from flasgger import swag_from  # type: ignore
import datetime
from sqlalchemy.exc import SQLAlchemyError

bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")
@bp_reembolso.route("/reembolsos")
@swag_from('../docs/reembolso/listar_reembolsos.yml')
def listar_todos_reembolsos():
    try:
        reembolsos = db.session.execute(db.select(Reembolso)).scalars().all()
        print(f"Tipo de 'reembolsos': {type(reembolsos)}")
        if reembolsos:
            for item in reembolsos:
                print(f"Tipo de item em 'reembolsos': {type(item)}")
            
            reembolsos = [reembolso.all_data() for reembolso in reembolsos]
            return jsonify(reembolsos), 200
        else:
            return jsonify({'response': 'Não há reembolsos cadastrados'}), 404

    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(error)}), 500

@bp_reembolso.route('/num_prestacao/<int:num_prestacao>', methods=['GET'])
def buscar_por_nprestacao(num_prestacao):
    try:
        reembolsos = db.session.execute(
            db.select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)
        ).scalars().all()

        if not reembolsos:
            return jsonify({'erro': f'Não foram encontrados reembolsos com o número de prestação: {num_prestacao}'}), 404

        reembolsos_json = [reembolso.to_dict() for reembolso in reembolsos] # Use to_dict ou all_data
        return jsonify(reembolsos_json), 200

    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(error)}), 500
@bp_reembolso.route('/solicitacao', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_novo_reembolso():
    try:
        listar_solicitacao = request.get_json()

        # Validar
        if not listar_solicitacao:
            return jsonify({'erro': 'A lista está vazia.'}), 400

        objetos_solicitacao = []
        for dados_solicitacao in listar_solicitacao:
            if not all(key in dados_solicitacao for key in ['colaborador', 'empresa', 'num_prestacao', 'descricao', 'data', 'tipo_reembolso', 'centro_custo', 'ordem_interna', 'divisao', 'pep', 'moeda', 'distancia_km', 'valor_km', 'valor_faturado', 'despesa', 'id_colaborador']):
                return jsonify({'erro': f'Faltando dados obrigatórios para o colaborador {dados_solicitacao["colaborador"]}'}), 400
            
            try:
                data_obj = datetime.datetime.strptime(dados_solicitacao['data'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': f'Formato de data inválido para o colaborador {dados_solicitacao["colaborador"]}. Use o formato AAAA-MM-DD.'}), 400
            

            nova_solicitacao = Reembolso(
                colaborador=dados_solicitacao['colaborador'],
                empresa=dados_solicitacao['empresa'],
                num_prestacao=dados_solicitacao['num_prestacao'],
                descricao=dados_solicitacao['descricao'],
                data=data_obj,
                tipo_reembolso=dados_solicitacao['tipo_reembolso'],
                centro_custo=dados_solicitacao['centro_custo'],
                ordem_interna=dados_solicitacao['ordem_interna'],
                divisao=dados_solicitacao['divisao'],
                pep=dados_solicitacao['pep'],
                moeda=dados_solicitacao['moeda'],
                distancia_km=dados_solicitacao['distancia_km'],
                valor_km=dados_solicitacao['valor_km'],
                valor_faturado=dados_solicitacao['valor_faturado'],
                despesa=dados_solicitacao['despesa'],
                id_colaborador=dados_solicitacao['id_colaborador'],
                status='analisando',
            )
            objetos_solicitacao.append(nova_solicitacao)

        db.session.add_all(objetos_solicitacao)
        db.session.commit()
        return jsonify({'response': 'Solicitação feita com sucesso'}), 201

    except ValueError as ve:
        return jsonify({'erro': 'Erro ao processar os dados: Formato inválido', 'detalhes': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'erro': 'Erro ao processar os dados: Chave não encontrada', 'detalhes': str(ke)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao acessar o banco de dados', 'detalhes': str(e)}), 500
    except Exception as erro:
        db.session.rollback()
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(erro)}), 500
@bp_reembolso.route('<int:id>')
def buscar_por_id_colaborador(id):
    
    try:
        reembolsos = db.session.execute(
            db.select(Reembolso).where(Reembolso.id_colaborador == id)
        ).scalars().all()
        
        if not reembolsos:
            return jsonify({'error': 'Não há reembolsos desse ID de Colaborador'}), 404
        
        reembolsos = [ reembolso.all_data() for reembolso in reembolsos ]
        
        return jsonify(reembolsos), 200
    except Exception as error:
        return jsonify({'error': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500

@bp_reembolso.route('deletar/<int:id>', methods=['DELETE'])
def deletar_por_id(id):
    try:
        reembolso = db.session.execute(
            db.select(Reembolso).where(Reembolso.id == id)
        ).scalar()
        if not reembolso:
            return jsonify({'erro': 'Reembolso não encontrado'}), 404

        db.session.delete(reembolso)
        db.session.commit()

        return jsonify({'mensagem': f'Reembolso {id} deletado com sucesso'}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(error)}), 500