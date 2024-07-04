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
            productos_data.append(producto_data)
        return jsonify(productos_data)
    except:
        return jsonify({"mensaje":"no hay ningun producto."})

#------------endpoint para agregar un producto
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/agregar" , methods=["POST"])
def agregar_producto_POST(id_usuario):
    try:
        if id_usuario == "1":
            data = request.json
            nuevo_nombre = data.get('nombre')
            nuevo_precio =data.get('precio')
            nueva_cantidad = data.get('cantidad')
            nueva_imagen= data.get('imagen')
            nueva_categoria_id=data.get('categoria_id')
            
            nuevo_producto=Producto(nombre=nuevo_nombre,precio=nuevo_precio,cantidad=nueva_cantidad,imagen=nueva_imagen,categoria_id=nueva_categoria_id)
        
            db.session.add(nuevo_producto)
            db.session.commit()
            return jsonify({"id":nuevo_producto.id,"nombre":nuevo_producto.nombre,"precio":nuevo_producto.precio,"cantidad":nuevo_producto.cantidad,"imagen":nuevo_producto.imagen,"categoria_id":nuevo_producto.categoria_id})
        else:
            return jsonify({"mensaje":"eeey, tu no puedes crear un producto"})
    except:
        return jsonify({"mensaje":"no se pudo agregar el producto."})

#------------endpoint para ver un producto especifico
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/<id_producto>" , methods=["GET"])
def ver_producto(id_usuario,id_producto):
    
    
    try:
        producto = Producto.query.get(id_producto)
        
        categoria=Categoria.query.get(producto.categoria_id)
        
        producto_data={
            "nombre":producto.nombre,
            "precio":producto.precio,
            "cantidad":producto.cantidad,
            "imagen":producto.imagen,
            "categoria":categoria.categoria,
            "comentarios":[]
        }
        for comentario in producto.comentarios:
            comentario_data={
                "id":comentario.id,
                "user_id":comentario.user_id,
                "nombre":comentario.nombre_usuario,
                "apellido":comentario.apellido_usuario,
                "producto_id":comentario.producto_id,
                "comentario":comentario.comentario,
            }
            producto_data['comentarios'].append(comentario_data)
        
        return jsonify(producto_data)
    except:
        return jsonify({"mensaje":"no se pudo obtener el producto especifico"})

#------------endpoint agregar un comentario en el producto
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/<id_producto>" , methods=["POST"])
def agregar_comentario(id_usuario,id_producto):
    try:
        usuario=Usuario.query.get(id_usuario)
        data=request.json
        comentario=data.get('comentario')
        nuevo_comentario=Comentario(user_id=id_usuario,nombre_usuario=usuario.nombre,apellido_usuario=usuario.apellido,producto_id=id_producto,comentario=comentario)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify({"id":nuevo_comentario.id,"user_id":nuevo_comentario.user_id,"nombre_usuario":nuevo_comentario.nombre_usuario,"apellido_usuario":nuevo_comentario.apellido_usuario,"producto_id":nuevo_comentario.producto_id,"comentario":comentario})
    except:
        return jsonify({"mensaje":"no se pudo subir el comentario"})


#------------endpoint borrar un producto
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/<id_producto>" , methods=["DELETE"])
def eliminar_producto(id_usuario,id_producto):
    try:
        if id_usuario == "1":
            producto = Producto.query.get(id_producto)
            db.session.delete(producto)
            db.session.commit()


            return jsonify({"mensaje":"eliminado con exito"})
        else:
            return jsonify({"mensaje":"Ey, tu no puedes hacer esto"})
    except:
        return jsonify({"mensaje":"error al querer eliminar el producto"})

        


#------------endpoint para comprar un producto y que me de la info de ese producto
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/<id_producto>/comprar" , methods=["GET"])
def comprar_GET(id_usuario,id_producto):
    try:
        producto = Producto.query.get(id_producto)
        
        categoria=Categoria.query.get(producto.categoria_id)
        
        producto_data={
            "nombre":producto.nombre,
            "precio":producto.precio,
            "cantidad":producto.cantidad,
            "imagen":producto.imagen,
            "categoria":categoria.categoria
        }
        
        return jsonify(producto_data)
    except:
        return jsonify({"mensaje":"no se pudo obtener el producto especifico"})

#------------endpoint para comprar un producto y actualizar en la base de datos la cantidad del producto que queda
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/<id_producto>/comprar" , methods=["PUT"])
def comprar_PUT(id_usuario,id_producto):
    try:
        producto=Producto.query.get(id_producto)
        data= request.json
        cantidad_comprada=data.get('cantidad')
        producto.cantidad -= cantidad_comprada
        db.session.commit()
        
        
        return jsonify({"comentario":"Compra exitosa"})
    except:
        return jsonify({"comentario":"Compra fallida"})


#------------endpoint para obtener los datos del producto a editar
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/<id_producto>/editar" , methods=["GET"])
def editar_GET(id_usuario,id_producto):
    try:
        if id_usuario=="1":
            producto = Producto.query.get(id_producto)
            categoria_id_producto=Categoria.query.get(producto.categoria_id)

            producto_data={
                "nombre":producto.nombre,
                "precio":producto.precio,
                "cantidad":producto.cantidad,
                "imagen":producto.imagen,
                "categoria_id":producto.categoria_id,
                "categoria":categoria_id_producto.categoria,
            }
            categorias = Categoria.query.all()
            categorias_data=[]
            for categoria in categorias:
                categoria_data={
                    "id":categoria.id,
                    "categoria":categoria.categoria
                }
                categorias_data.append(categoria_data)
            return jsonify(producto_data,categorias_data)
        else:
            return jsonify({"mensaje":"eeeey, tu no tienes acceso a editar el producto"})
    except:
        return jsonify({"mensaje":"error en editar GET"})

#------------endpoint para editar los datos de un producto
@cross_origin
@app.route("/usuarios/<id_usuario>/productos/<id_producto>/editar" , methods=["PUT"])
def editar_PUT(id_usuario,id_producto):
    try:
        if id_usuario == "1":
            producto=Producto.query.get(id_producto)

            data=request.json
            nombre=data.get('nombre')
            precio=data.get('precio')
            cantidad=data.get('cantidad')
            imagen=data.get('imagen')
            categoria_id=data.get('categoria_id')

            producto.nombre=nombre
            producto.precio=precio
            producto.cantidad=cantidad
            producto.imagen=imagen
            producto.categoria_id=categoria_id

            db.session.commit()
            return jsonify({"comentario":"Exito al editar el producto"})
        else:
            return jsonify({"comentario":"eeey, tu no puedes editar el producto"})
    except:
        return jsonify({"mensaje":"error al editar el producto"})



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)