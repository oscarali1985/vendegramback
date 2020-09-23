"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario
from smail import sendEmail
from stele import sendTelegram
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/usuario", methods=["GET", "POST"])
def cr_usuario():
    """
        "GET": devolver lista de todos los donantes
        "POST": crear un donante y devolver su información
    """
    # averiguar si es GET o POST
    if request.method == "GET":
        #   seleccionar todos los registros de la tabla donantes - usando flask-sqlalchemy
        #   crear una variable lista y asignarle todos los donantes que devuelva la consulta
        usuarios = Usuario.query.all()
        # verificamos si hay parámetros en la url y filtramos la lista con eso
        nombre = request.args.get("nombre")
        if nombre is not None:
            usuarios_filtrados = filter(lambda usuario: nombre.lower() in usuario.nombre_completo.lower(), usuarios)
        else:
            usuarios_filtrados = usuarios
        #   serializar los objetos de la lista - tendría una lista de diccionarios
        usuarios_serializados = list(map(lambda usuario: usuario.serializar(), usuarios_filtrados))
        print(usuarios_serializados)
        #   devolver la lista jsonificada y 200_OK
        return jsonify(usuarios_serializados), 200
    else:
        #   crear una variable y asignarle diccionario con datos para crear donante
        dato_reg = request.json # request.get_json()
        if dato_reg is None:
            return jsonify({
                "resultado": "no envió la informacion para crear el usuario..."
            }), 400
        #   verificar que el diccionario tenga cedula, nombre, apellido
        if (
            "nombre" not in dato_reg or
            "apellido" not in  dato_reg or
            "nombre_usuario" not in dato_reg or
            #"fecha_nacimiento"not in dato_reg or
            "correo" not in dato_reg or
            "telefono" not in dato_reg or
            "clave" not in dato_reg
        ):
            return jsonify({
                "resultado": "Favor verifique la informacion enviada faltan algunos campos obligatorios"
            }), 400
        #   validar que campos no vengan vacíos y que cédula tenga menos de 14 caracteres
        if (
            dato_reg["nombre"] == "" or
            dato_reg["apellido"] == "" or
            dato_reg["nombre_usuario"] == ""
            #len(str(insumos_donante["cedula"])) > 14
        ):
            return jsonify({
                "resultado": "revise los valores de su solicitud"
            }), 400
        #   crear una variable y asignarle el nuevo donante con los datos validados
        
        nuevo_usuario = Usuario.registrarse(
            dato_reg["nombre"],
            dato_reg["apellido"],
            dato_reg["nombre_usuario"],
            dato_reg["fecha_nacimiento"],
            dato_reg["correo"],
            dato_reg["telefono"],
            dato_reg["clave"],
            dato_reg["foto_perfil"],
            dato_reg["administrador"],
            dato_reg["suscripcion"]
        )
        
        #   agregar a la sesión de base de datos (sqlalchemy) y hacer commit de la transacción
        db.session.add(nuevo_usuario)
        try:
            db.session.commit()
            # devolvemos el nuevo donante serializado y 201_CREATED
            return jsonify(nuevo_usuario.serializar()), 201
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            # devolvemos "mira, tuvimos este error..."
            return jsonify({
                "resultado": f"{error.args}"
            }), 500


@app.route("/SendCorreo", methods = ['POST'])
def SendCorreo():

    # Verificamos el método
    if (request.method == 'POST'):

        # Obtenemos los datos de la forma
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']
        respuesta = sendEmail(nombre,correo,mensaje)
        #flash(respuesta, 'alert-success')
        #print(respuesta)
        # Redirigimos a mensaje
        return jsonify(respuesta), 200

# Para enviar Telegram
@app.route("/SendTelegram", methods = ['POST'])
def SendTelegram():

    # Verificamos el método
    if (request.method == 'POST'):

        # Obtenemos los datos de la forma
        nombre = request.form['nombre']
        telegram = request.form['telegram']
        mensaje = request.form['mensaje']

        #idTelegram = " {} "+telegram
        response = sendTelegram(nombre,telegram, mensaje)
        
        return response


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
