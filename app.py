from flask import Flask
from flask_restful import Api
from servicios import poblar_datos, ListaTareas, TareaItem

app = Flask(__name__)
api = Api(app)

api.add_resource(ListaTareas, '/api/v2.0/tareas')
api.add_resource(TareaItem, '/api/v2.0/tareas/<int:tarea_id>') #recibe como parametro un entero

@app.route('/')
def index() -> str:
    return "Hola mundo"

@app.route('/poblar')
def poblar() -> str:
    poblar_datos()
    return "datos poblados en la base con éxito"

if __name__ == "__main__":
    app.run(debug = True)

    # el @ es un decorador osea agrega una funcionalidad extra
