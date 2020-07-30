# Importamos todo lo necesario
import os
import csv
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


def read_csv(file):
  filename = secure_filename(file.filename)
  fstring = file.read()
  csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]
  return csv_dicts


# instancia del objeto Flask
app = Flask(__name__)

@app.route("/",methods=['GET'])
def upload_file():
  # renderiamos la plantilla "formulario.html"
  return "<h1>Hello</h1>"

@app.route("/session",methods=['POST'])
def program_open():
  directoty = request.json['user'] + request.json['time']
  path = os.path.join(os.getcwd(),'sessions',directoty)
  os.mkdir(path)
  os.chdir(os.path.join('sessions',directoty))
  session_file = directoty + '.csv'

  with open(session_file,'w') as fd:
    write_header = csv.writer(fd, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_header.writerow(['key','p_down','p_up'])
  return "Directory and file created"


@app.route("/upload", methods=['POST'])
def uploader():
  if request.method == 'POST':
    direc = request.form['user']
    # obtenemos el archivo del input "archivo"
    session_file = request.files['file_path']
    
    ############# TO FIX

    filename = secure_filename(session_file.filename)
    fstring = session_file.read()
    print("--------------------->>>>>>>>>>>>>",fstring)
    csv_dicts = []
    print("--------------------->>>>>>>>>>>>>",csv_dicts)
    dict_data = csv_dicts
    os.chdir(os.path.join('sessions',direc))
    file_path = os.path.join(os.getcwd(),'sessions',direc,direc,'.csv')
    with open(file_path,'a') as fd:
      fields = ['key','p_down','p_up']
      writer = csv.DictWriter(fd, fieldnames=fields)
      for row in dict_data:
        writer.writerow(row)
    return "Uploaded"

if __name__ == '__main__':
 # Iniciamos la aplicación
 app.run(debug=True)



