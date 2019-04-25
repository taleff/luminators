import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#Importing IR Data and Data from Labquest
diamineIR = np.genfromtxt('Ni(en).csv', skip_header = 0, delimiter = ',',
                       dtype = [('wave', 'f8'), ('abs', 'f8')])
complexIR = np.genfromtxt('Ni(en)3.csv', skip_header = 0, delimiter = ',',
                       dtype = [('wave', 'f8'), ('abs', 'f8')])
uv_vis = np.genfromtxt('TaleffCuENPartB.csv', skip_header = 1, delimiter = ',',
                       dtype = [('wave', 'f8'), ('abs', 'f8')])

def absGraph(data, name, title = '', xtitle = '', ytitle = '', invert = False, ybound = (0,0)):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    independentVar = data['wave']
    dependentVar = data['abs']
    ax.plot(independentVar, dependentVar)

    ax.set_ylabel(ytitle)
    if ybound != (0,0):
        ax.set_ylim(ybound[0], ybound[1])
    ax.set_xlabel(xtitle)
    if invert != False:
        plt.gca().invert_xaxis()
    ax.set_title(title)

    plt.savefig(name, dpi = 500)

absGraph(uv_vis, 'test')

def beerGraph(name, title = ''):
    molarity = [0.01668, 0.01336, 0.01070, 0.008771, 0.007017, 0.005620]
    abs = [0.141, 0.111, 0.090, 0.076, 0.067, 0.042]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    independentVar = molarity
    dependentVar = abs
    ax.plot(independentVar, dependentVar, marker = '.', markersize = 8, linewidth = 0)

    fit = curve_fit(lambda x, a: a*x, molarity, abs)
    xtrend = np.linspace(0.005620, 0.01668, num = 10)
    ytrend = fit[0][0]*xtrend
    ax.plot(xtrend, ytrend, linestyle = '--', color = 'b')

    r_square = 0.984
    ax.annotate('Equation: {0:.3f}x \nR-Squared: {1}'.format(fit[0][0], r_square), xy = (0.007017,0.111))

    ax.set_ylabel('Absorbance')
    ax.set_xlabel('Molarity (mol/L)')
    ax.set_title(title)

    plt.savefig(name, dpi=500)

absGraph(uv_vis, 'NickelDiamineAbsorbance', title = 'UV VIS Nickel Diamine Absorbance',
         xtitle = 'Wavelength (nm)', ytitle = 'Absorbance')
absGraph(diamineIR, 'DiamineIR2.svg', title = 'Diamine (en) IR Spectrum',
         xtitle = 'Wavenumber (1/cm)', ytitle = 'Transmittance', invert = True, ybound = (0, 100))
absGraph(complexIR, 'ComplexIR.svg', title = 'Nickel (en) Diamine Complex IR Spectrum',
         xtitle = 'Wavenumber (1/cm)', ytitle = 'Transmittance', invert = True, ybound = (0, 100))
beerGraph('BeerGraph', 'Beer-Lambert Calibration Curve for Nickel (en) Diamine Complex')