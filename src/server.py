# Importamos todo lo necesario
import os
import csv
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# instancia del objeto Flask
app = Flask(__name__)

@app.route("/",methods=['GET'])
def upload_file():
  # renderiamos la plantilla "formulario.html"
  return "<h1>Hello</h1>"

@app.route("/session",methods=['POST'])
def program_open():
  directoty = request.json['user'] + request.json['time']
  path = os.path.join(os.getcwd(),directoty)
  os.mkdir(path)
  return "Directory created"


@app.route("/upload", methods=['POST'])
def uploader():
  if request.method == 'POST':
    direc = request.json['user']

    # obtenemos el archivo del input "archivo"
    f = request.files['archivo']
    filename = secure_filename(f.filename)

    fstring = f.read()

    csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]
    
    

    return "<h1>Archivo subido exitosamente</h1>"

if __name__ == '__main__':
 # Iniciamos la aplicación
 app.run(debug=True)