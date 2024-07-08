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

#-------------------------------------------------------------------------------------
#------------endpoint para obtener lista de los usuarios 
@cross_origin
@app.route("/usuarios" , methods=["GET"])
def listar_usuarios():
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
@app.route("/usuarios" , methods=["POST"])
def crear_usuario():
    try:
        data = request.json
        nuevo_nombre = data.get('nombre')
        nuevo_apellido =data.get('apellido')
        nuevo_usuario = Usuario(nombre = nuevo_nombre, apellido = nuevo_apellido)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje":"Usuario creado correctamente"})
    except:
        return jsonify({"mensaje":"No se puedo crear el usuario."})

#-------------------------------------------------------------------------------------

#------------endpoint para obtener la lista de los productos 
@cross_origin
@app.route("/productos/" , methods=["GET"])
def listar_productos():
    try:
        productos = Producto.query.all()
        productos_data=[]
        for producto in productos:
            producto_data={
                "id":producto.id,
                "nombre":producto.nombre,
                "precio":producto.precio,
                "cantidad":producto.cantidad,
                "imagen":producto.imagen,
            }
            productos_data.append(producto_data)
        return jsonify(productos_data)
    except:
        return jsonify({"mensaje":"no hay ningun producto."})

#-------------------------------------------------------------------------------------

#------------endpoint para ver un producto especifico
@cross_origin
@app.route("/productos/<id_producto>" , methods=["GET"])
def ver_producto(id_producto):
    
    
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
        return jsonify({"mensaje":"No se pudo obtener el producto especifico"})

#------------endpoint agregar un comentario en el producto
@cross_origin
@app.route("/productos/<id_producto>" , methods=["POST"])
def agregar_comentario(id_producto):
    try:
        id_usuario=request.args.get('id_usuario')

        usuario=Usuario.query.get(id_usuario)
        data=request.json
        comentario=data.get('comentario')
        nuevo_comentario=Comentario(user_id=id_usuario,nombre_usuario=usuario.nombre,apellido_usuario=usuario.apellido,producto_id=id_producto,comentario=comentario)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify({"mensaje":"Comentario agregado exitosamente"})
    except:
        return jsonify({"mensaje":"no se pudo subir el comentario"})

#-------------------------------------------------------------------------------------

#------------endpoint para obtener las categorias de productos
@cross_origin
@app.route("/productos/crear" , methods=["GET"])
def obtener_categorias():
    try:
        categorias=Categoria.query.all()

        categorias_data=[]
        for categoria in categorias:
            categoria_data={
                "id":categoria.id,
                "categoria":categoria.categoria
            }
            categorias_data.append(categoria_data)

        return jsonify(categorias_data)
    except:
        return

#------------endpoint para agregar un producto
@cross_origin
@app.route("/productos/crear" , methods=["POST"])
def agregar_producto():
    try:
        
        data = request.json

        nuevo_nombre = data.get('nombre')
        nuevo_precio =data.get('precio')
        nueva_cantidad = data.get('cantidad')
        nueva_imagen= data.get('imagen')
        nueva_categoria_id=data.get('categoria_id')
        
        nuevo_producto=Producto(nombre=nuevo_nombre,precio=nuevo_precio,cantidad=nueva_cantidad,imagen=nueva_imagen,categoria_id=nueva_categoria_id)
    
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({"mensaje":"Producto agregado correctamente"})

    except:
        return jsonify({"mensaje":"no se pudo agregar el producto."})

#-------------------------------------------------------------------------------------

#------------endpoint borrar un producto
@cross_origin
@app.route("/productos/<id_producto>" , methods=["DELETE"])
def eliminar_producto(id_producto):
    try:
        
        producto = Producto.query.get(id_producto)
        db.session.delete(producto)
        db.session.commit()


        return jsonify({"mensaje":"eliminado con exito"})
    except:
        return jsonify({"mensaje":"error al querer eliminar el producto"})

        
#-------------------------------------------------------------------------------------

#------------endpoint para comprar un producto y que me de la info de ese producto
@cross_origin
@app.route("/productos/comprar/<id_producto>" , methods=["GET"])
def comprar_GET(id_producto):
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
@app.route("/productos/comprar/<id_producto>" , methods=["PUT"])
def comprar_PUT(id_producto):
    try:
        id_usuario=request.args.get('id_usuario')

        usuario=Usuario.query.get(id_usuario)

        producto=Producto.query.get(id_producto)

        data= request.json
        cantidad_comprada=int(data.get('cantidad'))
        
        producto.cantidad-=cantidad_comprada
        db.session.commit()
        
        
        info_usuario={
            "id":usuario.id,
            "nombre":usuario.nombre,
            "apellido":usuario.apellido
        }
        
        return jsonify(info_usuario)
    except:
        return jsonify({"comentario":"Compra fallida"}),404


#-------------------------------------------------------------------------------------
#------------endpoint para obtener los datos del producto a editar y todas las categorias que hay
@cross_origin
@app.route("/productos/editar/<id_producto>" , methods=["GET"])
def editar_GET(id_producto):
    try:
            

            producto = Producto.query.get(id_producto)
            
            producto_data={
                "nombre":producto.nombre,
                "precio":producto.precio,
                "cantidad":producto.cantidad,
                "imagen":producto.imagen,
                "categoria_id":producto.categoria_id
                
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
        
    except:
        return jsonify({"mensaje":"error en editar GET"})

#------------endpoint para editar los datos de un producto
@cross_origin
@app.route("/productos/editar/<id_producto>" , methods=["PUT"])
def editar_PUT(id_producto):
    try:
            id_usuario=request.args.get('id_usuario')
        
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
        
    except:
        return jsonify({"mensaje":"error al editar el producto"})



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)