from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from flasgger import swag_from  # type: ignore
import datetime
from sqlalchemy.exc import SQLAlchemyError

bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")
@bp_reembolso.route('/solicitacao', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados_requisicao = request.get_json()

    if not dados_requisicao:
        return jsonify({'mensagem': 'Dados não inseridos. A requisição está vazia.'}), 400

    campos_obrigatorios = ['colaborador', 'empresa', 'num_prestacao', 'data', 'tipo_reembolso',
                           'centro_custo', 'ordem_interna', 'moeda', 'valor_faturado']
    if not all(campo in dados_requisicao for campo in campos_obrigatorios):
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in dados_requisicao]
        return jsonify({'mensagem': 'Dados incompletos. Preencha todos os campos obrigatórios.',
                        'campos_faltantes': campos_faltantes}), 400

    try:        
        data_str = dados_requisicao.get('data')
        try:
            data_obj = datetime.datetime.strptime(data_str, '%Y-%m-%d')  # Ajuste o formato conforme necessário
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use o formato AAAA-MM-DD.', 'data_recebida': data_str}), 400

        # Cria uma nova instância de Reembolso
        nova_solicitacao = Reembolso(
            colaborador=dados_requisicao.get('colaborador'),
            empresa=dados_requisicao.get('empresa'),
            num_prestacao=dados_requisicao.get('num_prestacao'),
            descricao=dados_requisicao.get('descricao'),
            data=data_obj,
            tipo_reembolso=dados_requisicao.get('tipo_reembolso'),
            centro_custo=dados_requisicao.get('centro_custo'),
            ordem_interna=dados_requisicao.get('ordem_interna'),
            divisao=dados_requisicao.get('divisao'),
            pep=dados_requisicao.get('pep'),
            moeda=dados_requisicao.get('moeda'),
            distancia_km=dados_requisicao.get('distancia_km'),
            valor_km=dados_requisicao.get('valor_km'),
            valor_faturado=dados_requisicao.get('valor_faturado'),
            despesa=dados_requisicao.get('despesa'),
            id_colaborador=dados_requisicao.get('id_colaborador'),
            status='analisando',  # Define o status inicial
        )

        # Adiciona a nova solicitação à sessão do banco de dados
        db.session.add(nova_solicitacao)
        db.session.commit()

        return jsonify({'mensagem': 'Solicitação de reembolso criada com sucesso.', 'id': nova_solicitacao.id}), 201  # Retorna o ID da solicitação criada

    except ValueError as ve:
        db.session.rollback()  # Rollback em caso de erro
        return jsonify({'erro': 'Erro de valor inválido.', 'detalhes': str(ve)}), 400
    except KeyError as ke:
        db.session.rollback()
        return jsonify({'erro': 'Erro de chave não encontrada.', 'detalhes': str(ke)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro de banco de dados.', 'detalhes': str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro desconhecido.', 'detalhes': str(e)}), 500


@bp_reembolso.route("/reembolsos")
@swag_from('../docs/reembolso/listar_reembolso.yml')
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
@swag_from('../docs/reembolso/num_prestacao.yml')
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

@bp_reembolso.route('<int:id>')
def buscar_por_id_colaborador(id):
    try:
        reembolsos = db.session.execute(
            db.select(Reembolso).where(Reembolso.id_colaborador == id)
        ).scalars().all()

        reembolsos = [ reembolso.all_data() for reembolso in reembolsos ]

        return jsonify(reembolsos), 200
    except Exception as error:
        return jsonify({'error': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500

@bp_reembolso.route('deletar/<int:id>', methods=['DELETE'])
@swag_from('../docs/reembolso/remover_reembolso.yml')
def deletar_por_id(id):
    try:
        reembolso = db.session.execute(
            db.select(Reembolso).where(Reembolso.id == id)
        ).scalar()

        db.session.delete(reembolso)
        db.session.commit()

        return jsonify({'mensagem': f'Reembolso {id} deletado com sucesso'}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(error)}), 500
    
@bp_reembolso.route('/atualizar/<int:num_processo>', methods=['PUT'])
@swag_from('../docs/reembolso/atualizar_reembolso.yml')
def atualizar_solicitacao(num_processo):
    dados_atualizacao = request.get_json()

    if not dados_atualizacao:
        return jsonify({'mensagem': 'Dados para atualização não fornecidos.'}), 400

    reembolso = db.session.get(Reembolso, num_processo)

    if not reembolso:
        return jsonify({'mensagem': f'Processo com número {num_processo} não encontrado.'}), 404

    for chave, valor in dados_atualizacao.items():
        if hasattr(reembolso, chave):
            if chave == 'data':
                try:
                    setattr(reembolso, chave, datetime.datetime.strptime(valor, '%Y-%m-%d').date())
                except ValueError:
                    return jsonify({'erro': 'Formato de data inválido. Use o formato AAAA-MM-DD.', 'data_recebida': valor}), 400
            else:
                setattr(reembolso, chave, valor)

    try:
        db.session.commit()
        db.session.refresh(reembolso)  # Recarrega a instância 'reembolso'
        return jsonify({'mensagem': f'Dados do processo {num_processo} foi atualizado com sucesso.', 'processo': reembolso.all_data()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao atualizar o banco de dados.', 'detalhes': str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro inesperado ao processar a requisição.', 'detalhes': str(e)}), 500