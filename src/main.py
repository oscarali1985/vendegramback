"""
Este modulo carga la Base de datos y agrega los endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Producto


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Maneja/sereliza errores como un objeto JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Genera el sitio con todos los endpoints cargados
@app.route('/')
def sitemap():
    return generate_sitemap(app)

###################        CRUD de Vendegram !!!    ######################  
#####  1.-Obtenga una lista de todos los productos GET /producto;                         tambien filtra por nombre si recibe el parametro en la url   #########
    ##########  2.- Crear un nuevo producto POST /producto ########### 

@app.route('/producto', methods=["GET", "POST"])

def todos_productos():
    if request.method == "GET":
        producto = Producto.query.all()
        # verificamos si hay parámetros en la url y filtramos la lista con eso si titulo no esta vacio producto_filtrado busca en producto.titulo si el requerimiento es igual a algun titulo ya creado para filtrarlo.
        titulo = request.args.get("titulo")
        if titulo is not None:
            producto_filtrado = filter(lambda producto: titulo.lower() in producto.titulo, producto) 
        else:
            producto_filtrado = producto
        #   serializar los objetos de la lista - tendría una lista de diccionarios
        producto_lista = list(map(lambda producto: producto.serialize(), producto_filtrado))     
        return jsonify(producto_lista), 200
    ###Validaciones de caracteres y que los campos no esten vacios###
    else:
        insumos_producto = request.json
        if insumos_producto is None:
            return jsonify({
                "resultado": "no envio insumos para crear el producto" 
            }), 400
         # verificar que el diccionario tenga titulo, descripcion, foto,etc
        if (
            "titulo" not in insumos_producto or
            "descripcion" not in insumos_producto or
            "foto" not in insumos_producto
        ):
            return jsonify({
                "resultado": "revise las propiedades de su solicitud"
            }), 400
        #validar que campos no vengan vacíos y que los string tenga sus respectivos caracteres
        if (
            insumos_producto["titulo"] == "" or
            insumos_producto["descripcion"] == "" or
            insumos_producto["foto"] == "" or
            len(str(insumos_producto["titulo"])) > 2 or
            len(str(insumos_producto["descripcion"])) > 2 or
            len(str(insumos_producto["foto"])) > 2 or
            int(insumos_producto["cantidad"]) < 0 or
            float(insumos_producto["precio"]) < 0

        ):
            return jsonify({
                "resultado": "revise los valores de su solicitud"
            }), 400

        # METODO POST: crear una variable y asignarle el nuevo producto con los datos validados
        body = request.get_json()        
        producto = Producto(titulo=body['titulo'], foto=body['foto'], descripcion=body['descripcion'], precio=body['precio'], cantidad=body['cantidad'])
        #   agregar a la sesión de base de datos (sqlalchemy) y hacer commit de la transacción
        db.session.add(producto)
        try:
            db.session.commit()
            # devolvemos el nuevo donante serializado y 201_CREATED
            return jsonify(producto.serialize()), 201
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            # devolvemos "mira, tuvimos este error..."
            return jsonify({
                "resultado": f"{error.args}"
            }), 500

##########  4.- Eliminar un producto DELETE /producto/{producto_id} ########### 

@app.route('/delete/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto is None:
        raise APIException('producto no encontrado', status_code=404)
    else:
        # remover el producto específico de la sesión de base de datos
        db.session.delete(producto)
        # hacer commit y devolver 200
        try:
            db.session.commit()
            response_body = {
           "msg": "El producto a sido eliminado"
           }
            return jsonify(response_body), 200
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado al eliminar un producto": f"{error.args}"
            }), 500


##########  5.- Actualiza el producto UPDATE /producto/{producto_id} ###########     
@app.route('/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    body = request.get_json()
    producto = Producto.query.get(producto_id)
    if producto is None:
        raise APIException('producto no encontrado', status_code=404)

    if "titulo" in body:
        producto.titulo = body["titulo"]
    if "foto" in body:
        producto.foto = body["foto"]
    if "descripcion" in body:
        producto.descripcion = body['descripcion']
    if "precio" in body:
        producto.precio = body['precio']
    if "cantidad" in body:
        producto.cantidad = body['cantidad']
    try:
        db.session.commit()
        # devolvemos el nuevo producto serializado y 200_CREATED
        return jsonify(producto.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presente error al actualizar un producto": f"{error.args}"
        }), 500    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)