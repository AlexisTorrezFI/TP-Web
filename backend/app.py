from flask import Flask,request,jsonify,render_template
from flask_cors import CORS,cross_origin
from models import db, Producto,Categoria,Comentario


app = Flask(__name__)
CORS(app)


port= 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://alexis:password@localhost:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@cross_origin
@app.route("/")
def nada():
    return 


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)