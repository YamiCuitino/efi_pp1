# Imports que son nativos del Framework y Librerias
from app import app, db
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.views import MethodView

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
# Imports de variables generadas por nosotros
from app.models.models import (
    Usuario,
    Entrada,
    Comentario,
    Categoria,
)
from app.schemas.schema import (
    UsuarioSchema,
    EntradaSchema,
    ComentarioSchema,
    CategoriaSchema
)


class UsuarioView(MethodView):
    def get(self, usuario_id=None):
        if usuario_id is not None:
            usuario = Usuario.query.get(usuario_id)
            if usuario:
                usuario_schema = UsuarioSchema().dump(usuario)
                return jsonify(usuario_schema)
            else:
                return jsonify(MENSAJE="No se encontro el usuario, por favor ingrese un usuario valido"), 404
        else:
            usuarios = Usuario.query.all()
            allUsuarios = UsuarioSchema(many=True).dump(usuarios)
            return jsonify(allUsuarios)

    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('nombre')
        email = data.get('email')
        contraseña = data.get('contraseña')

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            contraseña=contraseña,
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(MENSAJE=f"El usuario {nombre} {apellido} se creo correctamente")

    def put(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify(MENSAJE="Usuario no encontrado"), 404

        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email  = data.get('email')
        contraseña = data.get('contraseña')
        #reemplaza por los nuevos datos
        usuario.nombre = nombre
        usuairo.apellido= apellido
        usuario.email = email
        usuario.contraseña = contraseña
       #sube los cambios a la bd
        db.session.commit()
        return jsonify(MENSAJE=f"El usuario {nombre} {apellido} se actualizo correctamente")

    def delete(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify(MENSAJE="Usuario no encontrado"), 404

        db.session.delete(usuario)
        db.session.commit()
        return jsonify(MENSAJE=f"El usuario {nombre} {apellido} elimino correctamente")

usuario_view = UsuarioView.as_view('usuario_view')
app.add_url_rule('/usuario/', view_func=usuario_view, methods=['GET', 'POST'])
app.add_url_rule('/usuario/<int:usuario_id>', view_func=usuario_view, methods=['GET', 'PUT', 'DELETE'])

class EntradaView(MethodView):
    def get(self, entrada_id=None):
        if entrada_id is not None:
            entrada = Entrada.query.get(entrada_id)
            if entrada:
                entrada_schema = PostSchema().dump(entrada)
                return jsonify(entrada_schema)
            else:
                return jsonify(MENSAJE="Post no encontrado"), 404
        else:
            entradas = Entrada.query.all()
            entradas_schema = PostSchema(many=True).dump(entradas)
            return jsonify(entradas_schema)

    def post(self):
        data = request.get_json()
        titulo = data.get("titulo")
        post = data.get("post")
        fecha = data.get("fecha")
        usuario_id = data.get("usuario_id")
        categorias = data.get("categorias")

        nueva_entrada = Post(
            titulo=titulo,
            post=post,
            fecha=fecha,
            usuario_id=usuario_id
        )

        if categorias:
            for categoria_id in categorias:
                categoria = Categoria.query.get(categoria_id)
                if categoria:
                    nueva_entrada.categorias.append(categoria)

        db.session.add(nueva_entrada)
        db.session.commit()

        return jsonify(MENSAJE="La nueva entrada se creo correctamente")

    def put(self, entrada_id):
        entrada = Entrada.query.get(entrada_id)
        if not entrada:
            return jsonify(MENSAJE="Entrada no encontrada"), 404

        data = request.get_json()
        titulo = data.get("titulo")
        post = data.get("post")
        fecha = data.get("fecha")
        usuario_id = data.get("usuario_id")
        categorias = data.get("categorias")
        #remplaza por los nuevos datos
        entrada.titulo = titulo
        entrada.post = post
        entrada.fecha = fecha
        entrada.usuario_id = usuario_id

        
        entrada.categorias.clear() # Elimina 

        if categorias:
            for categoria_id in categorias:
                categoria = Categoria.query.get(categoria_id)
                if categoria:
                    entrada.categorias.append(categoria)

        db.session.commit()
        return jsonify(MENSAJE=f"La entrada se actualizo correctamente")

    def delete(self, entrada_id):
        entrada = Entrada.query.get(entrada_id)
        if not entrada:
            return jsonify(MENSAJE="Entrada no encontrada"), 404

        db.session.delete(entrada)
        db.session.commit()
        return jsonify(MENSAJE="La entrada se elimino correctamente")

entrada_view = EntradaView.as_view('entrada_view')
app.add_url_rule('/entrada/', view_func=entrada_view, methods=['GET', 'POST'])
app.add_url_rule('/entrada/<int:entrada_id>', view_func=entrada_view, methods=['GET', 'PUT', 'DELETE'])

class CategoriaView(MethodView):
    def get(self, categoria_id=None):
        if categoria_id is not None:
            categoria = Categoria.query.get(categoria_id)
            if categoria:
                categoria_schema = CategoriaSchema().dump(categoria)
                return jsonify(categoria_schema)
            else:
                return jsonify(MENSAJE="Categoria no encontrada"), 404
        else:
            categorias = Categoria.query.all()
            categorias_schema = CategoriaSchema(many=True).dump(categorias)
            return jsonify(categorias_schema)

    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')

        nueva_categoria = Categoria(
            nombre=nombre
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return jsonify(MENSAJE=f"la categoria {nombre}  se creo correctamente")

    def put(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify(MENSAJE="Categoría no encontrada"), 404

        data = request.get_json()
        nombre = data.get('nombre')
        #reemplaza los datos
        categoria.nombre = nombre
        #sube a la bd
        db.session.commit()
        return jsonify(MENSAJE=f"La categoría {nombre} se actualizo correctamente")

    def delete(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify(MENSAJE="Categoría no encontrada"), 404

        db.session.delete(categoria)
        db.session.commit()
        return jsonify(MENSAJE=f"la categoría {nombre} se elimino correctamente")

categoria_view = CategoriaView.as_view('categoria_view')
app.add_url_rule('/categoria/', view_func=categoria_view, methods=['GET', 'POST'])
app.add_url_rule('/categoria/<int:categoria_id>', view_func=categoria_view, methods=['GET', 'PUT', 'DELETE'])

class ComentarioView(MethodView):
    def get(self, comentario_id=None):
        if comentario_id is not None:
            comentario = Comentario.query.get(comentario_id)
            if comentario:
                comentario_schema = ComentarioSchema().dump(comentario)
                return jsonify(comentario_schema)
            else:
                return jsonify(MENSAJE="Comentario no encontrado"), 404
        else:
            comentarios = Comentario.query.all()
            comentarios_schema = ComentarioSchema(many=True).dump(comentarios)
            return jsonify(comentarios_schema)

    def post(self):
        data = request.get_json()
        contenido = data.get("contenido")
        fecha = data.get("fecha")
        usuario_id = data.get("usuario_id")
        entrada_id = data.get("entrada_id")

        comentario_nuevo = Comentario(
            contenido=contenido,
            fecha=fecha,
            usuario_id=usuario_id,
            entrada_id=entrada_id
        )
        db.session.add(comentario_comentario)
        db.session.commit()
        return jsonify(MENSAJE="El comentario se creo correctamente")

    def put(self, comentario_id):
        comentario = Comentario.query.get(comentario_id)
        if not comentario:
            return jsonify(MENSAJE="Comentario no encontrado"), 404

        data = request.get_json()
        contenido = data.get("contenido")

        comentario.contenido = contenido

        db.session.commit()
        return jsonify(MENSAJE="Comentario actualizado correctamente")

    def delete(self, comentario_id):
        comentario = Comentario.query.get(comentario_id)
        if not comentario:
            return jsonify(MENSAJE="Comentario no encontrado"), 404

        db.session.delete(comentario)
        db.session.commit()
        return jsonify(MENSAJE="El comentario se elimino correctamente")

comentario_view = ComentarioView.as_view('comentario_view')
app.add_url_rule('/comentario/', view_func=comentario_view, methods=['GET', 'POST'])
app.add_url_rule('/comentario/<int:comentario_id>', view_func=comentario_view, methods=['GET', 'PUT', 'DELETE'])


if  __name__=="__main__":
    app.run(host="0.0.0.6", port=5005, debug=True)
