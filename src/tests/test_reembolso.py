# teste_model.py
from src.model import Reembolso

# Crie uma instância da classe Reembolso (você pode passar valores dummy para os argumentos)
reembolso_teste = Reembolso("Colaborador Teste", "Empresa Teste", 1, "Descrição Teste", "2025-05-11", "Tipo Teste", "Centro Teste", "Ordem Teste", "Divisão Teste", "PEP Teste", "BRL", "10", "2", 20.00, 5.00, 1)

# Tente chamar o método to_dict
try:
    dicionario_reembolso = reembolso_teste.to_dict()
    print("Método to_dict encontrado e executado com sucesso:")
    print(dicionario_reembolso)
except AttributeError as e:
    print(f"Erro: {e}")