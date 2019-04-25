import matplotlib.pyplot as plt
import numpy as np
import math
from LuminatorsLab5Energy import EnergyLevels

# Initializing lists containing fluorimeter data
lam_Eu, abs_Eu = zip(*np.genfromtxt("Report5_Eu.txt", skip_header=4, usecols=(4, 5)))
lam_Tb, abs_Tb = zip(*np.genfromtxt("Report5_Tb.txt", skip_header=4, usecols=(4, 5)))


def graph_fluor(lam, absor, title, fname):

    """
    This function takes in the data produced by the fluorimeter and saves a graph of the data.

    :param lam: List containing wavelengths of the data points output by the fluorimeter
    :param absor: List containing intensity values of the data corresponding to the wavelengths
    :param title: String that is the title of the graph
    :param fname: String that is the name the graph file is to be saved as
    :return: No return value, plot is saved the name 'fname'
    """

    plt.plot(lam, absor)
    plt.title(title)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    # Inserted bbox parameter to fix strange cutting off of the graph
    plt.savefig(fname, dpi=500, bbox_inches="tight")
    plt.clf()


def savgol(data, res=5, degree=3, h=1, der=0):

    """
    This is a function for smoothing a dataset where the x values of the data points are separated by a constant value.

    :param data: A list containing the data to find local maxima
    :param res: An integer representing the resolution of the smoothing function
    :param degree: An integer representing the degree of the fitting polynomial
    :param h: A float representing the separation of the x values of the data
    :param der: An integer representing the derivative
    :return: A tuple of lists containing the smoothed data points and the smoothed data points of the derivative.
    """

    if res > len(data):
        raise ValueError("Not enough data points for resolution")

    if (res % 2 == 0) and (res > 0):
        raise ValueError("The resolution must be a positive odd number")

    if res < degree + 2:
        raise ValueError("The resolution must be greater than the degree plus two")

    if int(der) != der or der > degree:
        raise ValueError("The derivative must be an integer greater than the degree of the polynomial")

    def j_calc(resolution, poly_degree):

        """
        This function returns the J matrix to calculate the convolution coefficients for the Savtizky-Golay method.

        :param resolution: The resolution of the procedure (how many data points are used for fitting a polynomial)
        :param poly_degree: The degree of the polynomial for the fit
        :return: The J matrix used for calculating the convolution coefficients.
        """

        # Calculates the z values for the fit.
        # For resolution 5, coeff = [-2, -1, 0, 1, 2] and so on.
        coeff = [(1-resolution)/2 + m for m in range(resolution)]
        j_matrix = np.zeros((resolution, poly_degree+1))

        for row, n in enumerate(coeff):
            for m in range(poly_degree+1):
                j_matrix[row, m] = n**m

        return j_matrix

    j = j_calc(res, degree)
    c = np.linalg.inv((j.transpose()).dot(j)).dot(j.transpose())

    new_data = [0]*len(data)
    for i in range(int(res/2), len(data)-int(res/2)):
        findex = i - int(res/2)
        eindex = i + int(res/2) + 1
        sub_data = data[findex:eindex]
        new_data[i] = c.dot(sub_data)[der] * math.factorial(der)/(h**der)

    return new_data


def interp(pt1, pt2, x):

    """
    This function linearly interpolates two points.

    :param pt1: Tuple of the coordinates of point 1
    :param pt2: Tuple of the coordinates of point 2
    :param x: point to interpolate to
    :return: The y values of the interpolation point
    """

    slope = (pt2[1]-pt1[1]) / (pt2[0]-pt1[0])
    y = slope*(x-pt1[0]) + pt1[1]
    return y


def local_max(datax, datay, derivative, minheight=100, minx=0):

    """
    This function finds the local maxima of a set of data using its derivative.

    :param datax: A list of the x values of a set of data.
    :param datay: A list of the y values of a set of data.
    :param derivative: A list of the y values of the derivative of a set of data
    :param minheight: The minimum height of a maximum.
    :param minx: The minimum x value for the maxima.
    :return: A list containing the local maxima of a set of data.
    """

    maxima = []
    x1, y1 = datax[0], derivative[0]
    datay = dict(zip(datax, datay))
    for x, y in zip(datax, derivative):
        if y1 > 0 and y < 0 and datay[x] > minheight and x > minx:
            maximum = interp((y1, x1), (y, x), 0)
            maxima.append(maximum)
        x1, y1 = x, y
    return maxima


# Using the function to graph the data from the Europium and Terbium complexes
graph_fluor(lam_Eu, abs_Eu, r"Emittance of the Eu(tmh)$_3$bpy Complex", "Report5_EuGraph.png")
graph_fluor(lam_Tb, abs_Tb, r"Emittance of the Tb(tmh)$_3$bpy Complex", "Report5_TbGraph.png")
graph_fluor(lam_Eu, savgol(abs_Eu, 31, 5, der = 1), r"Derivative of Emittance of the Eu(tmh)$_3$bpy Complex", "Report5_EuGraphDer.png")
graph_fluor(lam_Tb, savgol(abs_Tb, 31, 5, der = 1), r"Derivative of Emittance of the Tb(tmh)$_3$bpy Complex", "Report5_TbGraphDer.png")

# Using the Energy class to create energy level diagrams
Eu_Nrg = EnergyLevels(298, 469, 1.73*(10**4), local_max(lam_Eu, abs_Eu, savgol(abs_Eu, 11, 5, der=1), minheight=7000, minx=576.7))
Eu_Nrg.generate_names(r'$^5D_0$', 5)
Eu_Nrg.display('Europium Complex', 'Report5_EuNrg.png')
Tb_Nrg = EnergyLevels(295, 469, 2.10*(10**4), local_max(lam_Tb, abs_Tb, savgol(abs_Tb, 31, 5, der=1), minheight=50000, minx=476.2))
Tb_Nrg.generate_names(r'$^5D_4$', 6)
Tb_Nrg.display('Terbium Complex', 'Report5_TbNrg.png')