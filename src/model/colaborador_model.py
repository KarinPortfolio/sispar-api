from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DECIMAL, Integer, Float  # Importe Float

class Colaborador(db.Model):

    __tablename__ = 'colaborador' # Adicione o nome da tabela

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    email = Column(String(100))
    senha = Column(String(255))
    cargo = Column(String(100))
    salario = Column(Float(precision=2)) # Use Float com precisão

    # Método Construtor
    def __init__(self, nome, email, senha, cargo, salario):
        self.nome = nome
        self.email = email
        self.senha = senha  # A senha já deve vir hasheada do controller
        self.cargo = cargo
        self.salario = salario
# ---------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'senha': self.senha
        }

    def all_data(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            'salario': str(self.salario) # Converta para string para serialização JSON
        }
        
