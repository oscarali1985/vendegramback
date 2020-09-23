import os
from flask_admin import Admin
from models import db, Producto
#from models import db, User, Contact
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Agrega tus modelos aqui, por ejemplo esto es como nosotros añadimos a un producto a el admin
    admin.add_view(ModelView(Producto, db.session))
    # Pueden duplicar esta linea de abajo para agregar nuevos modelos
    # admin.add_view(ModelView(YourModelName, db.session))