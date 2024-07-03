from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__='productos'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer , nullable=False)
    cantidad = db.Column(db.Integer , default=1)
    image = db.Column(db.String(255))
    #me_gusta = db.Column(db.Integer , default=0)
    categoria_id =db.Column(db.Integer,db.ForeignKey('categorias.id'))
    comentarios=db.relationship("Comentario")

class Categoria(db.Model):
    __tablename__='categorias'
    id = db.Column(db.Integer,primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)

class Comentario(db.Model):
    __tablename__='comentarios'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    nombre_usuario = db.Column(db.String(50))
    apellido_usuario = db.Column(db.String(50))
    producto_id=db.Column(db.Integer, db.ForeignKey('productos.id'))
    comentario = db.Column(db.String(255))

class Usuario(db.Model):
    __tablename__='usuarios'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50),nullable=False)
    apellido = db.Column(db.String(50))
