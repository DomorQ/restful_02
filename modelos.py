#aqui se van a crear las clases para manejar los datos

from pony import orm

db = orm.Database()


#creamos una clase llamada tarea que hereda de db.Entity
class Tarea(db.Entity):
    _table_ = 'tarea'
    #orm crear el atributo id
    titulo = orm.Required(str)
    descripcion = orm.Required(str)
    hecho = orm.Required(bool)

    def __str__(self):
        return self.titulo
