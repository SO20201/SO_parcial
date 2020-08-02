# Importamos todo lo necesario
import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from utils import generate_histograma


# instancia del objeto Flask
app = Flask(__name__)



@app.route("/")
def home():
  # renderiamos la plantilla "formulario.html"
  return "Welcome"



@app.route("/session",methods=['POST'])
def program_open():
  # Generamos el nombre de la carpeta de sesion
  os_char = request.files['file']
  os_char_file = secure_filename(os_char.filename)
  os_char_file = os_char_file[:-4]
  path = os.path.join(os.getcwd(),'sessions',os_char_file)
  # Creamos el directorio de la sesion
  os.mkdir(path)
  os.chdir(os.path.join('sessions',os_char_file))

  os_char.save('user_characteristicas.txt')
  # Generamos el nombre del archivo csv de los datos
  session_file = os_char_file + '.csv'

  with open(session_file,'w') as fd:
    # Escribimos la cabecera del archivo 
    write_header = csv.writer(fd, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_header.writerow(['key','p_down','p_up'])

  os.chdir('../../')
  
  # Retornamos al usuario el nombre de su directorio 
  return os_char_file



@app.route("/upload", methods=['POST'])
def uploader():
  if request.method == 'POST':
    # obtenemos el archivo del input "archivo"
    session_file = request.files['file_path']
    direc = secure_filename(session_file.filename)
    
    # Obtenemos el nombre del archivo de sesion
    # Leemos el archivo recibido y lo descomponemos las lineas en listas
    fstring = session_file.read()
    csv_list = [row for row in fstring.splitlines()]

    os.chdir(os.path.join('sessions',direc[:-4]))
    
    file_name = direc
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
    

@app.route("/end", methods=['POST'])
def end_session():
  if request.method == 'POST':
    user = request.json['user']
    os.chdir(os.path.join(os.getcwd(),'sessions',user))
    file_path = user + '.csv'
    key_dur = list()
    lis_hist = list()

    with open(file_path,'r') as fd:
      reader = csv.DictReader(fd)
      
      # Calcular la duracion de cada tecla presionada
      for row in reader:
        start = datetime.strptime(row['p_down'],'%Y-%m-%d %H:%M:%S.%f')
        end = datetime.strptime(row['p_up'],'%Y-%m-%d %H:%M:%S.%f')
        duracion = end - start
        tupp = [row['key'],duracion.total_seconds()*1000]
        key_dur.append(tupp)
    
    items = list(set([x[0] for x in key_dur]))
    
    lis_hist = [[i,0] for i in items]
    # Calcular la duracion total sumada de cada caracter
    for i in range(len(items)):
      for j in key_dur:
        if j[0]==items[i]:
          lis_hist[i][1] += j[1]

    generate_histograma(lis_hist,user)


    os.chdir("../../")
    return "Session finished"


if __name__ == '__main__':
  # Iniciamos la aplicación
  app.run(debug=True)



