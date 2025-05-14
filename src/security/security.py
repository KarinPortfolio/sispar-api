import bcrypt

def hash_senha(senha):
    """Hashea a senha usando bcrypt."""
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')
    return senha_hash

def checar_senha(senha_texto_plano, senha_hash_armazenado):
    """Verifica se a senha em texto plano corresponde ao hash armazenado."""
    senha_bytes = senha_texto_plano.encode('utf-8')
    senha_hash_bytes = senha_hash_armazenado.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, senha_hash_bytes)