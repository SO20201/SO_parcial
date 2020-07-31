# Importamos todo lo necesario
import os
import csv
from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename


# instancia del objeto Flask
app = Flask(__name__)



@app.route("/",methods=['GET'])
def upload_file():
  # renderiamos la plantilla "formulario.html"
  return "Welcome"



@app.route("/session",methods=['POST'])
def program_open():
  # Generamos el nombre de la carpeta de sesion
  directory = request.json['user'] + request.json['time']
  path = os.path.join(os.getcwd(),'sessions',directory)
  # Creamos el directorio de la sesion
  os.mkdir(path)
  os.chdir(os.path.join('sessions',directory))
  # Generamos el nombre del archivo csv de los datos
  session_file = directory + '.csv'

  with open(session_file,'w') as fd:
    # Escribimos la cabecera del archivo 
    write_header = csv.writer(fd, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_header.writerow(['key','p_down','p_up'])

  os.chdir('../../')
  # Retornamos al usuario el nombre de su directorio 
  return jsonify({"user-session":directory})



@app.route("/upload", methods=['POST'])
def uploader():
  if request.method == 'POST':
    direc = request.form['user']
    # obtenemos el archivo del input "archivo"
    session_file = request.files['file_path']
    # Obtenemos el nombre del archivo de sesion
    file_name = direc + '.csv'
    
    # Leemos el archivo recibido y lo descomponemos las lineas en listas
    fstring = session_file.read()
    csv_list = [row for row in fstring.splitlines()]

    os.chdir(os.path.join('sessions',direc))
    
    with open(file_name,'a') as fd:
      writer = csv.writer(fd,delimiter=',',)
      for row in csv_list:
        # Pasamos el formato byte a string
        row = row.decode("utf-8")
        row = row.split(',')
        # Escribimos linea por linea
        writer.writerow(row)
    
    os.chdir("../../")
    return "Uploaded"
    

if __name__ == '__main__':
 # Iniciamos la aplicación
 app.run(debug=True)



