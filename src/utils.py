from random import randint
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import squarify
import os


def generate_histograma(list_key_dur, user):

    tiempos_totales = [x[1] for x in list_key_dur]
    print('----------',tiempos_totales)
    labels = [x[0] for x in list_key_dur]
    print('----------',labels)

    plt.rc('font', size=9)
    squarify.plot(sizes=tiempos_totales,label=labels, alpha=0.9)
    
    plt.axis('off')
    # Guardando el gráfico en foto
    plt.savefig('resultado.png')
    