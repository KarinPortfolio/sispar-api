# Sispar-API

# 1. Introdução:

## Descrição geral do projeto

Este é o projeto final do curso de fullstack da Escola Vai na Web. Consiste num sistema de gerenciamento de reembolsos e tem como objetivo ser uma ferramenta de emissão de reembolsos. O usuário pode registrar e alterar informações referentes a reembolsos e enviar para aprovação.

## Funcionalidades do sistema:

- **Registro de transações**: inserção de dados como número da prescrição, data, valores, descrição e categoria.
- **Categorização**: classificação de despesas em categorias como alimentação, transporte, lazer, etc.

## Tecnologias utilizadas no back-end:

- **Python**
- **MySQL**
- **Flask**

## Objetivo da API:

- Sistema de emissão de reembolso.

# 2. EndPoints da API:

Documentação dos principais endpoints (incluindo método HTTP, URL, parâmetros, e exemplo de resposta).
Sistema de Cadastro de Colaboradores:
| Método | URL | Descrição |
| ------ | ---------------------------------------------------- | ----------------------------- |
| POST | /cadastrar | Cadastra colaboradores |
| GET | /todos-colaboradores | Lista colaboradores |
| PUT | /atualizar/<int:colaborador_id> | Atualiza o colaborador por id |
| DELETE | /deletar/<int:colaborador_id>| Remove o colaborador por id |
| POST | /login | Permite login no sistema |

Sistema de Cadastro de Reembolso:
| Método | URL | Descrição |
| ------ | ---------------------------------------------------- | ----------------------------- |
| POST | /solicitacao | Cadastra solicitação de reembolso |
| GET | /reembolsos | Lista reembolsos |
| GET | /num_prestacao/<int:num_prestacao> | Busca reembolso por número de prestação de serviço |
| DELETE | deletar/<int:id> | Remove o pedido de reembolso por id |

# 3. Autenticação:

# 4. Validação de Dados:

# 5. Como rodar o projeto:

1- Copie o código na máquina local

2- Inicia o ambiente virtual (venv)\
`python3 -m venv venv`

3- Ativa o ambiente virtual\
Linux:\
`source venv/bin/activate`\
Windows:\
`venv/Scripts/activate`

4- Instala as dependências para o projeto\
`pip install -r requirements.txt`

5- Executa o flask\
`python run.py`

7- acesse o link pelo navegador para acessar as rotas do Swegger\
http://127.0.0.1:5000/apidocs
