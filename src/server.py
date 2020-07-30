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
  os.chdir(path)
  session_file = directoty + '.csv'
  
  with open(session_file,'w') as fd:
    write_header = csv.writer(fd, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_header.writerow(['key','p_down','p_up'])
  return "Directory and file created"


@app.route("/upload", methods=['POST'])
def uploader():
  if request.method == 'POST':
    direc = request.json['user']
    session_file = request.json['file_path']
    # obtenemos el archivo del input "archivo"
    f = request.files['archivo']
    
    dict_data = read_csv(f)

    with open(session_file,'a') as fd:
      fields = ['key','p_down','p_up']
      writer = csv.DictWriter(fd, fieldnames=fields)
      for row in dict_data:
        writer.writerow(row)
    return "Uploaded"

if __name__ == '__main__':
 # Iniciamos la aplicación
 app.run(debug=True)




 def read_csv(file):
    filename = secure_filename(file.filename)
    fstring = file.read()
    csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]
    return csv_dicts