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


#------------endpoint para crear entrar con un usuario
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




if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)