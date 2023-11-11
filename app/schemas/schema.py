from app import ma
from marshmallow import fields, validate

class UsuarioSchema(ma.Schema):
    id = fields.Integer()
    nombre = fields.String()
    apellido = fields.String()
    contraseña = fields.String(validate=validate.Length(min=3, max=50))
    email = fields.String()
    activo = fields.Boolean()

class EntradaSchema(ma.Schema):
    id = fields.Integer()
    titulo = fields.String()
    post = fields.String()
    fecha = fields.String()
    usuario_id = fields.Integer()

    #representa la relación entre una entrada y un usuario en el JSON
    usuario = ma.Nested(UsuarioSchema)
    categorias = ma.Nested("CategoriaSchema", many=True)

class CategoriaSchema(ma.Schema):
    id = fields.Integer()
    nombre = fields.String()

class ComentarioSchema(ma.Schema):
    id = fields.Integer()
    contenido = fields.String()
    fecha = fields.String()
    usuario_id = fields.Integer()
    entrada_id = fields.Integer()

    #representa la relación entre una entrada y un usuario en el JSON
    usuario = ma.Nested(UsuarioSchema)
    entrada = ma.Nested(EntradaSchema)

