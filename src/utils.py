import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib import cm
import platform as pl
import os


def generate_histograma(list_key_dur, user):

    matplotlib.use('Agg') # pylint: disable=multiple-statements
    print('----------------> ',list_key_dur)
    matplotlib.rcParams.update({'font.size': 12})
    ax=plt.gca()
    a=np.array(list_key_dur)
    tecla=np.array([x[0] for x in a])
    tiempo=np.array([float(y[1]) for y in a])
    colors = cm.hsv(tiempo/float(max(tiempo)))
    plt.xticks(range(len(tecla)),tecla,rotation=60)
    plt.bar(range(len(tiempo)),tiempo,edgecolor='black',color=colors)
    plt.title("HISTOGRAMA DE TECLAS PRESIONADAS")
        
    plt.ylabel('Tiempo presionado')
    plt.xlabel('Tecla')
    plt.ylim(min(tiempo)-1.0,max(tiempo)+1.0)
    plt.savefig("resultado.png",bbox_inches='tight')
    plt.clf()
    

    
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
  	
	file_name = str(getattr(pl,'node')()) + '.txt'
	file_path = os.path.join('sessions',file_name)
	with open(file_path,'w') as fd:
		for line in listaCaracteristicas:
			fd.write("{}\n".format(line))
	
    
