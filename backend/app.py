from flask import Flask,request,jsonify
from flask_cors import CORS,cross_origin
from models import db, Producto,Categoria,Comentario,Usuario


app = Flask(__name__)
CORS(app)


port= 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://alexis:password@localhost:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@cross_origin
@app.route("/")
def nada():
    return 


#------------endpoint para obtener lista de los usuarios 
@cross_origin
@app.route("/usuarios" , methods=["GET"])
def login_usuario():
    try:
        usuarios = Usuario.query.all()
        usuarios_data=[]
        for usuario in usuarios:
            usuario_data={
                'id':usuario.id,
                'nombre':usuario.nombre,
                'apellido':usuario.apellido
            }
            usuarios_data.append(usuario_data)

        return jsonify(usuarios_data)
    except:
        return jsonify({"mensaje":"No hay usuarios."})

#------------endpoint para crear un usuario
@cross_origin
@app.route("/usuarios/crear" , methods=["POST"])
def crear_usuario():
    try:
        data = request.json
        nuevo_nombre = data.get('nombre')
        nuevo_apellido =data.get('apellido')
        nuevo_usuario = Usuario(nombre = nuevo_nombre, apellido = nuevo_apellido)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"id":nuevo_usuario.id,"nombre":nuevo_usuario.nombre,"apellido":nuevo_usuario.apellido})
    except:
        return jsonify({"mensaje":"no se puedo crear el usuario."})

#------------endpoint para obtener la lista de los productos 
@cross_origin
@app.route("/usuarios/<id_usuario>/productos" , methods=["GET"])
def listar_productos(id_usuario):
    try:
        productos = Producto.query.all()
        productos_data=[]
        for producto in productos:
            producto_data={
                "nombre":producto.nombre,
                "precio":producto.precio,
                "cantidad":producto.cantidad,
                "imagen":producto.imagen,
            }
            productos_data.append(producto.data)
        return jsonify(productos_data)
    except:
        return jsonify({"mensaje":"no hay ningun producto."})




if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)