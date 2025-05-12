from flask import Flask
import yaml
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso

app = Flask(__name__)
app.register_blueprint(bp_colaborador)
app.register_blueprint(bp_reembolso)

def generate_routes_yaml(app):
    routes_data = {}
    for rule in app.url_map.iter_rules():
        endpoint = rule.endpoint
        path = rule.rule
        methods = sorted(list(rule.methods))
        if methods and 'OPTIONS' in methods:
            methods.remove('OPTIONS')  # Remover o método OPTIONS para clareza

        if path not in ('/static/<path:filename>', '/'): # Omitir rotas estáticas e raiz simples
            routes_data[path] = {
                'endpoint': endpoint,
                'methods': methods
            }
    return routes_data

if __name__ == '__main__':
    routes = generate_routes_yaml(app)
    with open('routes.yaml', 'w') as outfile:
        yaml.dump(routes, outfile, sort_keys=True, indent=2)
    print("Arquivo routes.yaml gerado com sucesso.")

    # Para executar a aplicação normalmente:
    # app.run(debug=True)