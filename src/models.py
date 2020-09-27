from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float
from datetime import datetime, time, timedelta, timezone
import enum
db = SQLAlchemy()


class Etiqueta(enum.Enum):   
    ALIMENTOS = "alimentos"
    BEBIDAS = "bebidas"
    SALSAS = "salsas"
    REFRESCOS = "refrescos"
    JUGOS = "jugos"

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(2000), nullable=False)
    precio = db.Column(db.Float(10), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    etiqueta_uno = db.Column(db.Enum(Etiqueta), nullable=False)
    etiqueta_dos = db.Column(db.Enum(Etiqueta), nullable=True)
    etiqueta_tres = db.Column(db.Enum(Etiqueta), nullable=True)
   # etiqueta = db.relationship("Etiqueta", backref="producto") 


    def __init__(self, titulo, foto, descripcion, precio, cantidad, etiqueta_uno, etiqueta_dos, etiqueta_tres):
        self.titulo = titulo
        self.foto = foto
        self.descripcion = descripcion
        self.precio = precio 
        self.cantidad = cantidad 
        self.etiqueta_uno = Etiqueta(etiqueta_uno)
        self.etiqueta_dos = Etiqueta(etiqueta_dos) if etiqueta_dos else None
        self.etiqueta_tres = Etiqueta(etiqueta_tres) if etiqueta_tres else None   

    @classmethod
    def nuevo(cls, titulo, foto, descripcion, precio, cantidad, etiqueta_uno, etiqueta_dos, etiqueta_tres):
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
            etiqueta_uno,
            etiqueta_dos,
            etiqueta_tres
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
        if "etiqueta_uno" in diccionario:
            self.etiqueta_uno = diccionario["etiqueta_uno"]  
        if "etiqueta_dos" in diccionario:
            self.etiqueta_dos = diccionario["etiqueta_dos"]  
        if "etiqueta_tres" in diccionario:
            self.etiqueta_tres = diccionario["etiqueta_tres"]                                               
        return True  

    def __repr__(self):
        return '<Producto %r>' % self.titulo
        

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "foto": self.foto,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "etiqueta_uno": self.etiqueta_uno.value,
            "etiqueta_dos": self.etiqueta_dos.value if self.etiqueta_dos else "",         
            "etiqueta_tres": self.etiqueta_tres.value if self.etiqueta_tres else ""
            # "groups": [subscription.group_id for subscription in self.subscriptions] ayuda para etiqueta
            }    

#"etiqueta_dos": self.etiqueta_dos.value if self.etiqueta_dos else "",
                
"""    
   
    else:
            {
            "id": self.id,
            "titulo": self.titulo,
            "foto": self.foto,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "etiqueta_uno": self.etiqueta_uno.value,
            "etiqueta_tres": self.etiqueta_tres.value,
             "etiqueta_dos": self.etiqueta_tres.value}
             """
"""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "foto": self.foto,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "etiqueta_uno": self.etiqueta_uno.value,
            "etiqueta_tres": self.etiqueta_tres.value  
  
                  
           # "groups": [subscription.group_id for subscription in self.subscriptions] ayuda para etiqueta


        } 
        
        
          def serialize(self):
        if "etiqueta_dos" == "":
            return {
            "id": self.id,
            "titulo": self.titulo,
            "foto": self.foto,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "etiqueta_uno": self.etiqueta_uno.value,
            "etiqueta_tres": self.etiqueta_tres.value,
            "etiqueta_dos": self.etiqueta_dos.value}      """


 