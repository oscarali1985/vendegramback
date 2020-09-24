from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timezone

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False, nullable=False)
    apellido = db.Column(db.String(50), unique=False, nullable=False)
    nombre_usuario = db.Column(db.String(20), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date())
    correo = db.Column(db.String(50), unique=True, nullable=False)
    telefono= db.Column(db.String(20), unique=False, nullable=False)
    clave_hash = db.Column(db.String(50), unique=False, nullable=False)
    foto_perfil = db.Column(db.String(50), unique=False, nullable=True)
    administrador = db.Column(db.Boolean(), unique=False, nullable=False)
    suscripcion = db.Column(db.Integer, unique=False, nullable=True)

    def __init__(self, nombre, apellido, nombre_usuario, fecha_nacimiento, correo, telefono, clave_hash, foto_perfil, administrador, suscripcion):
        """ crea y devuelve una instancia de esta clase """
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.fecha_nacimiento = fecha_nacimiento
        self.correo = correo
        self.telefono = telefono
        self.clave_hash = clave_hash
        self.foto_perfil = foto_perfil
        self.administrador = administrador
        self.suscripcion = suscripcion

    def __str__(self):
        return f"\t{self.id} ->  {self.nombre_completo}"


    def __repr__(self):
        return '<Usuario %r>' % self.correo

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
            suscripcion
        )
        return nuevo_usuario

    @property
    def nombre_completo(self):
        """ devuelve nombre + ' ' apellido """
        return f"{self.nombre} {self.apellido}"

    def serializar(self):

        date_str = str(self.fecha_nacimiento)
        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
        print(type(date_object))
        print(date_object) 
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
            "administrador":self.administrador
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
        if "clave" in diccionario:
            self.clave_hash = diccionario["clave"].strip()
        if "foto_perfil" in diccionario:
            self.foto_perfil = diccionario["foto_perfil"].strip()
        if "suscripcion" in diccionario:
            self.suscripcion = diccionario["suscripcion"]    

        # for (key, value) in diccionario.items():
        #     if hasattr(self, key) and key != "cedula":
        #         self[key] = value
        return True
