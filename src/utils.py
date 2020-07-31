from random import randint
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import squarify


def generate_histograma(list_key_dur, user):

    print(list_key_dur)
    tiempos_totales = [x[1] for x in list_key_dur]

    labels = [x[0] for x in list_key_dur]
    color_list = ['#'+format(randint(0,0xFFFFFF),'x') for i in range(len(labels))]
    print(color_list)

    plt.rc('font', size=9)
    squarify.plot(sizes=tiempos_totales,color= color_list,label=labels, alpha=0.7) 

    plt.axis('off')
    # Guardando el gráfico en foto
    print("--------> Antes de guaradr")
    plt.savefig('resultado.png')
    print("--------< Despues de guaradr")