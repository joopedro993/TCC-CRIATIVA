from flask import Flask, jsonify, request
from flask_cors import CORS
from database_atividade import *

app = Flask(__name__)

CORS(app)

criar_banco_atividade()

if __name__ == "__main__":
    app.run(debug=True,port=5005)