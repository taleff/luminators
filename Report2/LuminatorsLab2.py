import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

#Importing Data from each Labquest Data Set
buffer = np.genfromtxt('HsiehTaleffBuffer.csv', skip_header = 1, delimiter = ',',
                       dtype = [('vol', 'f8'), ('pH', 'f8'), ('actVol', 'f8'), ('der', 'f8')])
trial1 = np.genfromtxt('HsiehTaleffDerivative1.csv', skip_header = 1, delimiter = ',',
                       dtype = [('vol', 'f8'), ('pH', 'f8'), ('actVol', 'f8'), ('der', 'f8')])
trial2 = np.genfromtxt('HsiehTaleffDerivative2.csv', skip_header = 1, delimiter = ',',
                       dtype = [('vol', 'f8'), ('pH', 'f8'), ('actVol', 'f8'), ('der', 'f8')])
trial3 = np.genfromtxt('HsiehTaleffDerivative3.csv', skip_header = 1, delimiter = ',',
                       dtype = [('vol', 'f8'), ('pH', 'f8'), ('actVol', 'f8'), ('der', 'f8')])

def graph(data_set, title = 'Titration', name = 'test', depVar = 'pH',
          annotate = (0,0)):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    independentVar = data_set['actVol']
    dependentVar = data_set[depVar]
    ax.plot(independentVar, dependentVar, marker = '.', markersize = 6)

    ax.set_ylabel(depVar)
    ax.set_xlabel('Volume (mL)')
    ax.set_title(title)

    if annotate != (0,0):
        ax.annotate('Half Equivalence Point: ({0}, {1})'.format(annotate[0], annotate[1]), xy = annotate,
                    xytext = (annotate[0]-11.5, annotate[1]+2), arrowprops = dict(arrowstyle = '->'))

    plt.savefig(name, dpi = 500)

sets = [buffer, trial1, trial2, trial3]
names = ['buffer', 'trial1', 'trial2', 'trial3']
titles = ['Titration of Unknown Buffer', 'Titration of an Unknown:Trial 1',
          'Titration of an Unknown:Trial 2', 'Titration of an Unknown:Trial 3']
annotations = [(19.04, 4.70), (10.24, 5.12), (9.76, 5.15), (10.24, 5.16)]


for i, set in enumerate(sets):
    graph(set, titles[i], names[i], annotate = annotations[i])

def buffer_graph(data_set, title = 'Titration', name = 'test', depVar = 'pH'):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    independentVar = data_set['actVol']
    dependentVar = data_set[depVar]
    ax.plot(independentVar, dependentVar, marker = '.', markersize = 6)

    ax.set_ylabel(depVar)
    ax.set_xlabel('Volume (mL)')
    ax.set_title(title)

    rect = Rectangle((0, 3.28), 34.84, 5.76-3.28, edgecolor='k', alpha=0.1)
    ax.add_artist(rect)

    ax.annotate('Equivalence Point', xy = (37.81, 8.20), xytext = (20, 10), arrowprops = dict(arrowstyle = '->'))
    ax.annotate('Buffer Region', xy = (13.5,6))

    plt.savefig(name, dpi = 500)

buffer_graph(buffer, "Titration of Unknown Buffer", "buffer")





