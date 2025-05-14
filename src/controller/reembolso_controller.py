from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from flasgger import swag_from  # type: ignore
import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")

@bp_reembolso.route('/solicitacao', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados_requisicao = request.get_json()
    id_colaborador_padrao = int(1)  # Defina o ID do colaborador aqui

    if not isinstance(dados_requisicao, list):
        return jsonify({'mensagem': 'Formato de dados incorreto. Espera-se uma lista de solicitações.'}), 400

    if not dados_requisicao:
        return jsonify({'mensagem': 'Nenhuma solicitação de reembolso fornecida.'}), 400

    solicitacoes_criadas = []
    erros = []

    for item_requisicao in dados_requisicao:
        campos_obrigatorios = ['colaborador', 'empresa', 'num_prestacao', 'data', 'tipo_reembolso',
                              'centro_custo', 'moeda', 'valor_faturado']  # Removi 'id_colaborador' da lista de obrigatórios
        if not all(campo in item_requisicao for campo in campos_obrigatorios):
            campos_faltantes = [campo for campo in campos_obrigatorios if campo not in item_requisicao]
            erros.append({'erro': 'Dados incompletos para uma solicitação.', 'campos_faltantes': campos_faltantes, 'dados_recebidos': item_requisicao})
            continue

        num_prestacao = item_requisicao.get('num_prestacao')
        reembolso_existente = db.session.execute(
            db.select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)
        ).scalar_one_or_none()

        if reembolso_existente:
            erros.append({'erro': f'O número de prestação {num_prestacao} já existe.', 'dados_recebidos': item_requisicao})
            continue

        else:
            data_str = item_requisicao.get('data')
            if not data_str:
                erros.append({'erro': 'Campo "data" ausente para uma solicitação.', 'dados_recebidos': item_requisicao})
                continue
            try:
                data_obj = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()
            except ValueError:
                erros.append({'erro': 'Formato de data inválido para uma solicitação. Use AAAA-MM-DD.', 'data_recebida': data_str, 'dados_recebidos': item_requisicao})
                continue

            nova_solicitacao = Reembolso(
                colaborador=item_requisicao.get('colaborador'),
                empresa=item_requisicao.get('empresa'),
                num_prestacao=num_prestacao,
                descricao=item_requisicao.get('descricao'),
                data=data_obj,
                tipo_reembolso=item_requisicao.get('tipo_reembolso'),
                centro_custo=item_requisicao.get('centro_custo'),
                ordem_interna=item_requisicao.get('ordem_interna'),
                divisao=item_requisicao.get('divisao'),
                pep=item_requisicao.get('pep'),
                moeda=item_requisicao.get('moeda'),
                distancia_km=item_requisicao.get('distancia_km'),
                valor_km=item_requisicao.get('valor_km'),
                valor_faturado=item_requisicao.get('valor_faturado'),
                despesa=item_requisicao.get('despesa'),
                id_colaborador=id_colaborador_padrao, # Usando o valor pré-definido aqui
                status='analisando',
            )

            db.session.add(nova_solicitacao)
            db.session.flush()
            solicitacoes_criadas.append({'id': nova_solicitacao.id, 'num_prestacao': nova_solicitacao.num_prestacao})

    if solicitacoes_criadas:
        db.session.commit()

    if erros:
        return jsonify({'mensagem': 'Algumas solicitações falharam.', 'sucesso': solicitacoes_criadas, 'falhas': erros}), 409
    else:
        return jsonify({'mensagem': f'{len(solicitacoes_criadas)} solicitações de reembolso criadas com sucesso.', 'solicitacoes': solicitacoes_criadas}), 201
@bp_reembolso.route("/reembolsos")
@swag_from('../docs/reembolso/listar_reembolso.yml')
def listar_reembolso():
    reembolsos = db.session.execute(
        db.select(Reembolso)
    ).scalars().all()

    reemb_lista = [reembolso.to_dict() for reembolso in reembolsos]

    return jsonify(reemb_lista)


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

@bp_reembolso.route('deletar/<int:num_prestacao>', methods=['DELETE'])
@swag_from('../docs/reembolso/remover_reembolso.yml')
def deletar_por_num_p(num_prestacao):
    try:
        reembolso = db.session.execute(
            db.select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)
        ).scalar()

        db.session.delete(reembolso)
        db.session.commit()

        return jsonify({'mensagem': f'Reembolso {num_prestacao} deletado com sucesso'}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(error)}), 500
    
@bp_reembolso.route('/atualizar/<int:num_prestacao>', methods=['PUT'])
@swag_from('../docs/reembolso/atualizar_reembolso.yml')
def atualizar_solicitacao(num_prestacao):
    dados_atualizacao = request.get_json()

    if not dados_atualizacao:
        return jsonify({'mensagem': 'Dados para atualização não fornecidos.'}), 400

    reembolso = db.session.execute(
        select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)  # Use select e where
    ).scalar_one_or_none()

    if not reembolso:
        return jsonify({'mensagem': f'Processo com número {num_prestacao} não encontrado.'}), 404

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
        db.session.refresh(reembolso)
        return jsonify({'mensagem': f'Dados do processo {num_prestacao} foi atualizado com sucesso.', 'processo': reembolso.to_dict()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao atualizar o banco de dados.', 'detalhes': str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro inesperado ao processar a requisição.', 'detalhes': str(e)}), 500