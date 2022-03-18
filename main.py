from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
from functools import wraps
import jwt
import os
import datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'user.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "RAHASIA"

class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(15))
db.create_all()

class RegisterUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        if dataUsername and dataPassword:
            dataModel = AuthModel(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"Berhasil"}), 200)
        return jsonify({"msg":"Username/Password tidak boleh KOSONG"})

class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:

            token = jwt.encode(
                {
                    "username":queryUsername, 
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return make_response(jsonify({"msg":"succes", "token":token}), 200)
        return jsonify({"msg":""})

api.add_resource(RegisterUser, "/reg", methods=["POST"])
api.add_resource(LoginUser, "/log", methods=["POST"])

if __name__ == "_main_":
    app.run(debug=True, port=4000)