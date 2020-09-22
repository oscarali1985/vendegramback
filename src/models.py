from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False, nullable=False)
    apellido = db.Column(db.String(50), unique=False, nullable=False)
    nombre_usuario = db.Column(db.String(20), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.DateTime(timezone=True))
    correo = db.Column(db.String(50), unique=True, nullable=False)
    telefono= db.Column(db.String(20), unique=False, nullable=False)
    clave_hash = db.Column(db.String(80), unique=False, nullable=False)
    foto_perfil = db.Column(db.String(120), unique=False, nullable=False)
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
            nombre.lower().capitalize(),
            apellido.lower().capitalize(),
            nombre_usuario,
            fecha_nacimiento,
            correo.casefold(),
            telefono,
            clave,
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
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido":self.apellido,
            "nombre_usuario":self.nombre_usuario,
            "fecha_nacimiento":self.fecha_nacimiento, 
            "correo":self.correo,
            "telefono":self.telefono,
            #La clave no se serializa,
            "foto_perfil":self.foto_perfil,
            "suscripcion":self.suscripcion 
            "administrador":self.administrador
        }


    def actualizar_usuario(self, diccionario):
        """ actualiza propiedades del usuario según el contenido del diccionario """

        if "email" in diccionario:
            self.email = diccionario["email"]
        if "nombre" in diccionario:
            self.nombre = diccionario["nombre"]
        if "apellido" in diccionario:
            self.apellido = diccionario["apellido"]
        if "nombre_usuario" in diccionario:
            self.nombre_usuario = diccionario["nombre_usuario"]
        if "fecha_nacimiento" in diccionario:
            self.fecha_nacimiento = diccionario["fecha_nacimiento"]
        if "correo" in diccionario:
            self.correo = diccionario["correo"]
        if "telefono" in diccionario:
            self.telefono = diccionario["telefono"]
        if "clave" in diccionario:
            self.clave_hash = diccionario["clave"]
        if "foto_perfil" in diccionario:
            self.foto_perfil = diccionario["foto_perfil"]
        if "suscripcion" in diccionario:
            self.suscripcion = diccionario["suscripcion"]    

        # for (key, value) in diccionario.items():
        #     if hasattr(self, key) and key != "cedula":
        #         self[key] = value
        return True
