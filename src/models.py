from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timezone
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float
import enum
import json, os
from base64 import b64encode
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


########################15
#
#    Usuarios
#
########################
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False, nullable=False)
    apellido = db.Column(db.String(50), unique=False, nullable=False)
    nombre_usuario = db.Column(db.String(20), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date())
    correo = db.Column(db.String(50), unique=True, nullable=False)
    telefono= db.Column(db.String(20), unique=False, nullable=False)
    clave_hash = db.Column(db.String(250), nullable=False)
    salt = db.Column(db.String(16), nullable=False)
    foto_perfil = db.Column(db.String(50), unique=False, nullable=True)
    administrador = db.Column(db.Boolean(), unique=False, nullable=False)
    suscripcion = db.Column(db.Integer, unique=False, nullable=True)
    suscripciones = db.relationship("Suscripcion", backref="usuario") 
    fecha_registro = db.Column(db.Date())

    #usuario_id = db.relationship("Tienda", backref="usuario", uselist=False)
    #usuario_id = db.relationship("Suscripcion", backref="usuario", uselist=False)
    #usuario_id = db.relationship("Calificacion", backref="usuario", uselist=False)

    #usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    def __init__(self, nombre, apellido, nombre_usuario, fecha_nacimiento, correo, telefono, clave, foto_perfil, administrador, suscripcion):
        """ crea y devuelve una instancia de esta clase """
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.fecha_nacimiento = fecha_nacimiento
        self.correo = correo
        self.telefono = telefono
        self.salt = b64encode(os.urandom(4)).decode("utf-8")
        self.set_password(clave)
        self.foto_perfil = foto_perfil
        self.administrador = administrador
        self.suscripcion = suscripcion
        self.fecha_registro = date.today()


    def set_password(self, clave):

        """
        hash y guarda
        """
        self.clave_hash = generate_password_hash(f"{clave}{self.salt}")

    def check_password(self, clave):
        """ Se verifica si clave coincide """
        return check_password_hash(self.clave_hash, f"{clave}{self.salt}")

    def __str__(self):
        return f"\t{self.id} ->  {self.nombre_completo}"


    def __repr__(self):
        return '<Usuario %r>' % self.correo


    @classmethod
    def cargar(cls):
        """
            abre el archivo usuario.json y carga en la 
            variable usuarios objetos usuario para cada
            uno de los diccionarios de la lista
        """
        usuario = []
        try:
            with open("./usuario.json", "r") as usuario_archivo:
                usuario_diccionarios = json.load(usuario_archivo)
                for usuario in usuario_diccionarios:
                    nuevo_usuario = cls.registrarse(
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
                    usuario.append(nuevo_usuario)
        except:
            with open("./usuario.json", "w") as usuario_archivo:
                pass
        return usuario

    @staticmethod
    def salvar(usuarios):
        """
            guarda usuario en formato json en el archivo
            correspondiente
        """
        with open("./usuario.json", "w") as usuario_archivo:
            usuarios_serializados = []
            for usuario in usuarios:
                usuarios_serializados.append(Usuario.serializar())
            json.dump(usuarios_serializados, usuario_archivo)





    @classmethod
    def registrarse(cls, nombre, apellido, nombre_usuario, fecha_nacimiento, correo, telefono, clave, foto_perfil, administrador, suscripcion):
        """
            normaliza insumos nombre y apellido,
            crea un objeto de la clase Donante con
            esos insumos y devuelve la instancia creada.
        """
        nuevo_usuario = cls(
            nombre.title().strip(),
            apellido.title().strip(),
            nombre_usuario.strip(),
            fecha_nacimiento,
            correo.casefold().strip(),
            telefono,
            clave.strip(),
            foto_perfil,
            administrador,
            suscripcion,
        )
        return nuevo_usuario

    @property
    def nombre_completo(self):
        """ devuelve nombre + ' ' apellido """
        return f"{self.nombre} {self.apellido}"

    def serializar(self):

        date_str = str(self.fecha_nacimiento)
        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()

        datereg_str = str(self.fecha_registro)
        date_object = datetime.strptime(datereg_str, '%Y-%m-%d').date()
        #print(type(date_object))
        #print(date_object) 
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido":self.apellido,
            "nombre_usuario":self.nombre_usuario,
            "fecha_nacimiento":date_str, 
            "correo":self.correo,
            "telefono":self.telefono,
            "foto_perfil":self.foto_perfil,
            "suscripcion":self.suscripcion, 
            "administrador":self.administrador,
            "fecha_registro":datereg_str
        }


    def actualizar_usuario(self, diccionario):
        """ actualiza propiedades del usuario según el contenido del diccionario """

        if "nombre" in diccionario:
            self.nombre = diccionario["nombre"].title().strip()
        if "apellido" in diccionario:
            self.apellido = diccionario["apellido"].title().strip()
        if "nombre_usuario" in diccionario:
            self.nombre_usuario = diccionario["nombre_usuario"].strip()
        if "fecha_nacimiento" in diccionario:
            self.fecha_nacimiento = diccionario["fecha_nacimiento"]
        if "correo" in diccionario:
            self.correo = diccionario["correo"].casefold().strip()
        if "telefono" in diccionario:
            self.telefono = diccionario["telefono"].strip()
        if "foto_perfil" in diccionario:
            self.foto_perfil = diccionario["foto_perfil"].strip()
        if "suscripcion" in diccionario:
            self.suscripcion = diccionario["suscripcion"]   
        if "administrador" in diccionario:
            self.administrador = diccionario["administrador"]        

        # for (key, value) in diccionario.items():
        #     if hasattr(self, key) and key != "cedula":
        #         self[key] = value
        return True

    def actualizar_clave(self, diccionario):
        """ actualiza propiedades del usuario según el contenido del diccionario """
        print("Actualizando clave")
        if "clave" in diccionario:
            nclave = diccionario["clave"].strip()
            print(nclave)
            self.clave_hash = generate_password_hash(f"{nclave}{self.salt}")
            print(self.clave_hash)
        return True

    def actualizar_clavealeatoria(self, nuevaclave):
        """ actualiza propiedades del usuario según el contenido del diccionario """
        print("Actualizando clave")
        self.clave_hash = generate_password_hash(f"{nuevaclave}{self.salt}")
        print(self.clave_hash)
        return True



















    

########################159
#
#    Suscripcion
#
########################



class Planes(enum.Enum):   
    BASICO = "basico"
   
class Suscripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan = db.Column(db.Enum(Planes), nullable=False)
    fecha_registro = db.Column(db.Date())
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))


    def __init__(self, plan, nombre_tienda):
        self.plan = Planes(plan),
        self.fecha_registro = date.today()
        # self.nombre_tienda = Tienda(nombre_tienda)


    @classmethod
    def nuevo_sub(cls, plan):
        """
            normalizacion de nombre foto, etc...
            crea un objeto de la clase Suscripcion con
            esa normalizacion y devuelve la instancia creada.
        """
        nuevo_suscriptor = cls(
            plan
        )
        return nuevo_suscriptor 

    def update(self, diccionario):
        """Actualizacion de Suscripcion"""
        if "plan" in diccionario:
            self.plan = Planes(diccionario["plan"]) if diccionario["plan"] else None
        return True  

    def __repr__(self):
        return '<Suscripcion %r>' % self.plan       
        

    def serialize(self):

        datereg_str = str(self.fecha_registro)
        date_object = datetime.strptime(datereg_str, '%Y-%m-%d').date()
        return {
            "id": self.id,
            "plan": self.plan.value,
            "fecha_registro":datereg_str
            # 'tienda': self.tienda.nombre_tienda
            # "tienda": [self.tienda.nombre_tienda]
        }

















































        # """
        #     normalizacion de nombre foto, etc...
        #     crea un objeto de la clase tienda con
        #     esa normalizacion y devuelve la instancia creada.
        # """
        # nuevo_tienda = cls(
        #     nombre_tienda,
        #     correo_tienda,
        #     telefono_tienda,
        #     foto_tienda,
        #     facebook_tienda,
        #     instagram_tienda,
        #     twitter_tienda,
        #     zona_general,
        #     zona_uno,
        #     zona_dos,
        #     zona_tres
        # )
        # return nuevo_tienda 

########################191
#
#    Tienda
#
########################
class Zona_general(enum.Enum):
    DISTRITO_CAPITAL = "Distrito Capital"
    MIRANDA = "Miranda"

class Zona(enum.Enum):   
  
    ALTAGRACIA = "Altagracia"
    ANTÍMANO = "Antimano"
    CANDELARIA = "Candelaria"
    CARICUAO = "Caricuao"
    CATEDRAL = "Catedral"
    CATIA = "Catia"
    CAUCAGÜITA = "Caucagüita"
    CHACAO = "Chacao"
    COCHE = "Coche"
    EL_CAFETAL = "El Cafetal"
    EL_JUNQUITO = "El Junquito"
    EL_PARAÍSO = "El Paraíso"
    EL_RECREO = "El Recreo"
    EL_VALLE = "El Valle"
    FILA_DE_MARICHES = "Fila De Mariches"
    LA_DOLORITA = "La Dolorita"
    LA_PASTORA = "La Pastora"
    LA_VEGA = "La Vega"
    LAS_MINAS = "Las Minas"
    LEONCIO_MARTÍNEZ = "Leoncio Martínez"
    MACARAO = "Macarao"
    NUESTRA_SEÑORA_DEL_ROSARIO = "Nuestra Señora Del Rosario"
    PETARE = "Petare"
    SAN_AGUSTÍN = "San Agustín"
    SAN_BERNARDINO = "San Bernardino"
    SAN_JOSÉ = "San José"
    SAN_JUAN = "San Juan"
    SAN_PEDRO = "San Pedro"
    SANTA_ROSALÍA = "Santa Rosalía"
    SANTA_ROSALÍA_DE_PALERMO = "Santa Rosalía De Palermo"
    SANTA_TERESA = "Santa Teresa"
    VEINTITRÉS_DE_ENERO = "veintitrés De Enero"  

   
class Tienda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_tienda = db.Column(db.String(40), unique=True, nullable=False)
    correo_tienda = db.Column(db.String(30), unique=True, nullable=False)
    telefono_tienda = db.Column(db.String(30), nullable=True)
    foto_tienda = db.Column(db.String(200), nullable=True)
    facebook_tienda = db.Column(db.String(30), nullable=True)
    instagram_tienda = db.Column(db.String(30), nullable=True)
    twitter_tienda = db.Column(db.String(30), nullable=True)
    zona_general = db.Column(db.Enum(Zona_general), nullable=False)
    zona_uno = db.Column(db.Enum(Zona), nullable=True)
    zona_dos = db.Column(db.Enum(Zona), nullable=True)
    zona_tres = db.Column(db.Enum(Zona), nullable=True) 
    productos = db.relationship("Producto", backref="tienda") 



    def __init__(self, nombre_tienda, correo_tienda, telefono_tienda, foto_tienda, facebook_tienda, 
    instagram_tienda, twitter_tienda, zona_general, zona_uno, zona_dos, zona_tres):
        self.nombre_tienda = nombre_tienda
        self.correo_tienda = correo_tienda
        self.telefono_tienda = telefono_tienda
        self.foto_tienda = foto_tienda 
        self.facebook_tienda = facebook_tienda 
        self.instagram_tienda = instagram_tienda
        self.twitter_tienda = twitter_tienda
        self.zona_general = Zona_general(zona_general)
        self.zona_uno = Zona(zona_uno) if zona_uno else None
        self.zona_dos = Zona(zona_dos) if zona_dos else None
        self.zona_tres = Zona(zona_tres) if zona_tres else None 


    @classmethod
    def cargar(cls):
        """
            abre el archivo donante.json y carga en la 
            variable donantes objetos donante para cada
            uno de los diccionarios de la lista
        """
        tienda = []
        try:
            with open("./tienda.json", "r") as tienda_archivo:
                tiendas_diccionarios = json.load(tienda_archivo)
                for tienda in tiendas_diccionarios:
                    nuevo_tienda = cls.nuevo(
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
                    tienda.append(nuevo_tienda)
        except:
            with open("./tienda.json", "w") as tienda_archivo:
                pass
        return tienda

    @staticmethod
    def salvar(tiendas):
        """
            guarda tienda en formato json en el archivo
            correspondiente
        """
        with open("./tienda.json", "w") as tienda_archivo:
            tiendas_serializados = []
            for tienda in tiendas:
                tiendas_serializados.append(Tienda.serialize())
            json.dump(tiendas_serializados, tienda_archivo)


    @classmethod
    def nuevo(cls, nombre_tienda, correo_tienda, telefono_tienda, foto_tienda, facebook_tienda, 
    instagram_tienda, twitter_tienda, zona_general, zona_uno, zona_dos, zona_tres):

        """
            normalizacion de nombre foto, etc...
            crea un objeto de la clase tienda con
            esa normalizacion y devuelve la instancia creada.
        """
        nuevo_tienda = cls(
            nombre_tienda,
            correo_tienda,
            telefono_tienda,
            foto_tienda,
            facebook_tienda,
            instagram_tienda,
            twitter_tienda,
            zona_general,
            zona_uno,
            zona_dos,
            zona_tres
        )
        return nuevo_tienda 

    def update(self, diccionario):
        """Actualizacion de producto"""
        if "nombre_tienda" in diccionario:
            self.nombre_tienda = diccionario["nombre_tienda"]
        if "correo_tienda" in diccionario:
            self.correo_tienda = diccionario["correo_tienda"]
        if "telefono_tienda" in diccionario:
            self.telefono_tienda = diccionario["telefono_tienda"]
        if "foto_tienda" in diccionario:
            self.foto_tienda = diccionario["foto_tienda"]
        if "facebook_tienda" in diccionario:
            self.facebook_tienda = diccionario["facebook_tienda"]   
        if "instagram_tienda" in diccionario:
            self.instagram_tienda = diccionario["instagram_tienda"] 
        if "twitter_tienda" in diccionario:
            self.twitter_tienda = diccionario["twitter_tienda"] 
        if "zona_general" in diccionario and diccionario ["zona_general"] != "":
            self.zona_general = Zona_general(diccionario["zona_general"])
        if "zona_uno" in diccionario:
            self.zona_uno = Zona(diccionario["zona_uno"]) if diccionario["zona_uno"] else None
        if "zona_dos" in diccionario:
            self.zona_dos = Zona(diccionario["zona_dos"]) if diccionario["zona_dos"] else None
        if "zona_tres" in diccionario:
            self.zona_tres = Zona(diccionario["zona_tres"]) if diccionario["zona_tres"] else None                                                                                
        return True  
 
    def __repr__(self):
        return '<Tienda %r>' % self.nombre_tienda
        

    def serialize(self):

        producto_list = self.productos
        lista_id = []
        for producto in producto_list:
            lista_id.append(producto.titulo)

        return {
            "id": self.id,
            "nombre_tienda": self.nombre_tienda,
            "correo_tienda": self.correo_tienda,
            "telefono_tienda": self.telefono_tienda,
            "foto_tienda": self.foto_tienda,
            "facebook_tienda": self.facebook_tienda,
            "instagram_tienda": self.instagram_tienda,
            "twitter_tienda": self.twitter_tienda,
            "zona_general": self.zona_general.value,
            "zona_uno": self.zona_uno.value if self.zona_uno else "",
            "zona_dos": self.zona_dos.value if self.zona_dos else "",
            "zona_tres": self.zona_tres.value if self.zona_tres else "",
            "productos": lista_id
            # "groups": [subscription.group_id for subscription in self.subscriptions] ayuda para etiqueta
            }    
             


########################136
#
#    Productos
#
########################

class Etiqueta_general(enum.Enum):
    PRODUCTOS = "productos"
    SERVICIOS = "servicios"

class Etiqueta(enum.Enum):   
    ALIMENTOS = "alimentos"
    BEBIDAS = "bebidas"
    CEREALES = "cereales"
    DECORACIONES = "decoraciones"
    DETERGENTES = "detergentes"
    ENLATADOS = "enlatados"
    JABONES = "jabones"
    MANTENIMIENTOS = "mantenimientos"
    MAQUILLAJES = "maquillajes"
    MEDICAMENTOS = "medicamentos"
    PELUQUERIA = "peluqueria"
    PELUQUERIA_VETERINARIA = "peliqueria_veterinaria"
    PLOMERIA = "plomeria"
    REPARACIONES = "reparaciones"
    ROPA = "ropa"
    SALSAS = "salsas"
   
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), unique=True, nullable=False)
    foto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(2000), nullable=False)
    precio = db.Column(db.Float(10), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    etiqueta_general = db.Column(db.Enum(Etiqueta_general), nullable=False)
    etiqueta_uno = db.Column(db.Enum(Etiqueta), nullable=False)
    etiqueta_dos = db.Column(db.Enum(Etiqueta), nullable=True)
    etiqueta_tres = db.Column(db.Enum(Etiqueta), nullable=True)
    tienda_id = db.Column(db.Integer, ForeignKey('tienda.id'))


    def __init__(self, titulo, foto, descripcion, precio, cantidad, etiqueta_general, etiqueta_uno, etiqueta_dos, etiqueta_tres, tienda_id):
        self.titulo = titulo
        self.foto = foto
        self.descripcion = descripcion
        self.precio = precio 
        self.cantidad = cantidad 
        self.etiqueta_general = Etiqueta_general(etiqueta_general)
        self.etiqueta_uno = Etiqueta(etiqueta_uno)
        self.etiqueta_dos = Etiqueta(etiqueta_dos) if etiqueta_dos else None
        self.etiqueta_tres = Etiqueta(etiqueta_tres) if etiqueta_tres else None 
        self.tienda_id = tienda_id  


    @classmethod
    def cargar(cls):
        """
            abre el archivo producto.json y carga en la 
            variable productos objetos producto para cada
            uno de los diccionarios de la lista
        """
        producto = []
        try:
            with open("./producto.json", "r") as producto_archivo:
                producto_diccionarios = json.load(producto_archivo)
                for producto in producto_diccionarios:
                    nuevo_producto = cls.nuevo(
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
                    producto.append(nuevo_producto)
        except:
            with open("./producto.json", "w") as producto_archivo:
                pass
        return producto

    @staticmethod
    def salvar(productos):
        """
            guarda producto en formato json en el archivo
            correspondiente
        """
        with open("./producto.json", "w") as producto_archivo:
            productos_serializados = []
            for producto in productos:
                productos_serializados.append(Producto.serialize())
            json.dump(productos_serializados, producto_archivo)


    @classmethod
    def nuevo(cls, titulo, foto, descripcion, precio, cantidad, etiqueta_general, etiqueta_uno, etiqueta_dos, etiqueta_tres, tienda_id):
        """
            normalizacion de nombre foto, etc...
            crea un objeto de la clase producto con
            esa normalizacion y devuelve la instancia creada.
        """
        nuevo_producto = cls(
            titulo,
            foto,
            descripcion,
            precio,
            cantidad,
            etiqueta_general,
            etiqueta_uno,
            etiqueta_dos,
            etiqueta_tres,
            tienda_id            
        )
        return nuevo_producto 

    def update(self, diccionario):
        """Actualizacion de producto"""
        if "foto" in diccionario:
            self.foto = diccionario["foto"]
        if "titulo" in diccionario:
            self.titulo = diccionario["titulo"]
        if "descripcion" in diccionario:
            self.descripcion = diccionario["descripcion"]
        if "precio" in diccionario:
            self.precio = diccionario["precio"]
        if "cantidad" in diccionario:
            self.cantidad = diccionario["cantidad"]   
        if "etiqueta_general" in diccionario and diccionario["etiqueta_general"] != "": 
            self.etiqueta_general = Etiqueta_general(diccionario["etiqueta_general"])  
        if "etiqueta_uno" in diccionario and diccionario["etiqueta_uno"] != "": 
            self.etiqueta_uno = Etiqueta(diccionario["etiqueta_uno"])  
        if "etiqueta_dos" in diccionario:
            self.etiqueta_dos = Etiqueta(diccionario["etiqueta_dos"]) if diccionario["etiqueta_dos"] else None
        if "etiqueta_tres" in diccionario:
            self.etiqueta_tres = Etiqueta(diccionario["etiqueta_tres"]) if diccionario["etiqueta_tres"] else None                                               
        return True  

    def __repr__(self):
        return '<Producto %r>' % self.titulo       
        

    def serializer(self):

        # tienda_list = [self.tienda]
        # lista_id = []
        # for tienda in tienda_list:
        #     lista_id.append(tienda.nombre_tienda)

        return {
            "id": self.id,
            "titulo": self.titulo,
            "foto": self.foto,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "etiqueta_general": self.etiqueta_general.value,
            "etiqueta_uno": self.etiqueta_uno.value,
            "etiqueta_dos": self.etiqueta_dos.value if self.etiqueta_dos else "",         
            "etiqueta_tres": self.etiqueta_tres.value if self.etiqueta_tres else "",
            "tienda": self.tienda_id            
            # "tienda": 
            # aqui en tienda serializo el nombre de la tienda osea de la tabla tienda nono yo le quito list
            #si debe ser uno si lo intente, pero me daba el mismo error ya te lo enseño

            # exacto pero como hago para a la hora de crear un producto en post, este conectado a la tienda
            #si tengo la tienda, mmm como agrego su id
            # entonces conectariamos el id de usuario con id de tienda y llegaria al post del producto cierto
            # es 1 a 1 y de tienda a producto es 1 a muchos

            # ahhh okok intentaremos eso

            # "nombre_tienda": [productos.tienda_id for productos in self.tienda_id]
            # "groups": [subscription.group_id for subscription in self.subscriptions] ayuda para etiqueta
            }

    def serialize(self):
    
        # tienda_list = [self.tienda]
        # lista_id = []
        # for tienda in tienda_list:
        #     lista_id.append(tienda.nombre_tienda)

        return {
            "id": self.id,
            "titulo": self.titulo,
            "foto": self.foto,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "etiqueta_general": self.etiqueta_general.value,
            "etiqueta_uno": self.etiqueta_uno.value,
            "etiqueta_dos": self.etiqueta_dos.value if self.etiqueta_dos else "",         
            "etiqueta_tres": self.etiqueta_tres.value if self.etiqueta_tres else "",
            "tienda": self.tienda.nombre_tienda
        }          
            # "tienda": 
            # aqui en tienda serializo el nombre de la tienda osea de la tabla tienda nono yo le quito list
            #si debe ser uno si lo intente, pero me daba el mismo error ya te lo enseño

            # exacto pero como hago para a la hora de crear un producto en post, este conectado a la tienda
            #si tengo la tienda, mmm como agrego su id
            # entonces conectariamos el id de usuario con id de tienda y llegaria al post del producto cierto
            # es 1 a 1 y de tienda a producto es 1 a muchos

            # ahhh okok intentaremos eso

            # "nombre_tienda": [productos.tienda_id for productos in self.tienda_id]
            # "groups": [subscription.group_id for subscription in self.subscriptions] ayuda para etiqueta

#"etiqueta_dos": self.etiqueta_dos.value if self.etiqueta_dos else "",
                
















########################
#
#    Calificacion
#
########################