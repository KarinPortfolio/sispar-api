# bcrypt_test.py
import bcrypt

print(f"Módulo bcrypt: {bcrypt}")
print(f"Tipo de bcrypt: {type(bcrypt)}")
print(f"Dicionário de bcrypt keys(): {bcrypt.__dict__.keys()}")

try:
    senha = b"senha_de_teste"
    senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')
    print(f"Hash gerado: {senha_hash}")
    print("bcrypt está funcionando corretamente.")
except AttributeError as e:
    print(f"Erro de atributo: {e}")
except ImportError as e:
    print(f"Erro de importação: {e}")

try:
    senha = b"senha_de_teste"
    senha_hash_armazenado = b"$2b$12$H4K65/6Hv/X/ImwLGf0X.Oe4474/i/yY3y/B5Q9l/y/t/w.9x77C" # Um hash de exemplo
    if bcrypt.checkpw(senha, senha_hash_armazenado):
        print("checkpw está funcionando corretamente.")
    else:
        print("checkpw falhou (isso é esperado com um hash aleatório).")
except AttributeError as e:
    print(f"Erro de atributo em checkpw: {e}")
except ImportError as e:
    print(f"Erro de importação em checkpw: {e}")