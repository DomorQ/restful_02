from modelos import *
from flask_restful import Resource, request, abort

db.bind('sqlite','tareas.db',create_db=True) #tareas.db es un archivo, crear la tabla de datos

db.generate_mapping(create_tables=True)#crea las tablas

def poblar_datos():
    with orm.db_session: #se trabaja con una sesion activa del orm
        tarea1= Tarea(
            titulo ='Viajar',
            descripcion ='Visitar Buenos Aires',
            hecho = False
        )
        tarea2= Tarea(
            titulo = 'Entrenar',
            descripcion = 'Mejorar fisicamente para jugar',
            hecho = False
        )
        tarea2= Tarea(
            titulo='Salto',
            descripcion= 'saltar en paracaidas',
            hecho = False
        )

class ListaTareas(Resource):
    def get(self):
        # $ curl -i -X GET http://localhost:5000/api/v2.0/tareas
        with orm.db_session:
            return {
                       item.id: {
                           'titulo': item.titulo,
                           'descripcion': item.descripcion,
                           'hecho': item.hecho
                       }
                       for item in Tarea.select()
                   }, 200

    def post(self):
        # $ curl -i -H "Content-Type: application/json" -X POST -d '{"titulo":"Investigar SOAP","descripcion":"Buscar
        # información sobre esta tecnología"}' http://localhost:5000/api/v2.0/tareas
        if not request.is_json:
            abort(404, message="La petición no se encuentra en formato application/json")

        with orm.db_session:
            item = Tarea(
                titulo=request.json['titulo'],
                descripcion=request.json['descripcion'],
                hecho=False
            )

        return {"tarea": item.to_dict()}, 201

class TareaItem(Resource):
    def get(self, tarea_id):
        # $ curl -i -X GET http://localhost:5000/api/v2.0/tareas/2
        try:
            with orm.db_session:
                tarea = Tarea[tarea_id]
                return {"tarea": tarea.to_dict()}, 200
        except orm.ObjectNotFound:
            abort(404, message="Tarea con id={} no existe".format(tarea_id))

    def put(self, tarea_id):
        # $ curl -i -H "Content-Type: application/json" -X PUT -d '{"titulo":"Desaprender SOAP","descripcion":"Olvidar
        # lo que sabemos de SOAP","hecho":true}' http://localhost:5000/api/v2.0/tareas/4
        if not request.is_json:
            abort(404, message="La petición no se encuentra en formato application/json")
        try:
            with orm.db_session:
                tarea = Tarea[tarea_id]
                tarea.titulo = request.json['titulo']
                tarea.descripcion = request.json['descripcion']
                tarea.hecho = request.json['hecho']
                return {"tarea": tarea.to_dict()}, 200
        except orm.ObjectNotFound:
            abort(404, message="Tarea con id={} no existe".format(tarea_id))

    def delete(self, tarea_id):
        # $ curl -i -X DELETE http://localhost:5000/api/v2.0/tareas/4
        try:
            with orm.db_session:
                tarea = Tarea[tarea_id]
                if tarea:
                    tarea.delete()
        except orm.ObjectNotFound:
            abort(404, message="Tarea con id={} no existe".format(tarea_id))
        return {'message': 'Tarea eliminada exitosamente'}, 200
