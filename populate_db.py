from flask import Flask
from flask_migrate import Migrate
from src.models import db, Usuario, Producto, Tienda, Suscripcion
import json
import os

# iniciar la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# iniciar la sesión de sqlalchemy - mysql
MIGRATE = Migrate(app, db)
db.init_app(app)
with app.app_context():
    # cargar data de un archivo .json con la información de los objetos a crear
    with open("./baseline_data.json") as data_file:
        data = json.load(data_file)
        # crear esos objetos y guardar en bdd
        for tienda in data["tienda"]:
            nuevo_tienda = Tienda.nuevo(
                tienda["nombre_tienda"],
                tienda["correo_tienda"],
                tienda["telefono_tienda"],
                tienda["foto_tienda"],
                tienda["facebook_tienda"],
                tienda["instagram_tienda"],
                tienda["twitter_tienda"],
                tienda["zona_general"],
                tienda["zona_uno"],
                tienda["zona_dos"],
                tienda["zona_tres"]
            )
            db.session.add(nuevo_tienda)
            db.session.commit()

        for producto in data["producto"]:
            nuevo_producto = Producto.nuevo(
                producto["titulo"],
                producto["foto"],
                producto["descripcion"],
                producto["precio"],
                producto["cantidad"],
                producto["etiqueta_general"],
                producto["etiqueta_uno"],
                producto["etiqueta_dos"],
                producto["etiqueta_tres"],
                producto["tienda_id"]
            )
            db.session.add(nuevo_producto)
            db.session.commit()

        for usuario in data["usuario"]:
            nuevo_usuario = Usuario.registrarse(
                usuario["nombre"],
                usuario["apellido"],
                usuario["nombre_usuario"],
                usuario["fecha_nacimiento"],
                usuario["correo"],
                usuario["telefono"],
                usuario["clave"],
                usuario["foto_perfil"],
                usuario["administrador"],
                usuario["suscripcion"]
            )
            db.session.add(nuevo_usuario)
            db.session.commit()            