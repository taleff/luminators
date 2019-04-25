import matplotlib.pyplot as plt


class EnergyLevels:
    """
    Class representing the energy levels of a lanthanide complex
    """

    def __init__(self, s1=0, t1=0, di=0, f=(), names = (r"S_0", r"S_1", r"T_1", r"D_i", r"F_i", r"F_i",
                                                        r"F_i", r"F_i", r"F_i", r"F_i", r"F_i")):
        """
        Initialization of the energy levels class.

        :param s1: Float representing the fluorescence wavelength (nm) of the ligand (tmh).
        :param t1: Float representing the phosphorescent wavelength (nm) of the ligand (tmh).
        :param di: Float representing the "energy transfer" of the lanthanide complex (cm^-1).
        :param f: Tuple of floats representing the luminescent wavelengths (nm) of the lanthanide complex.
        :param names: Tuple of strings containing the names of the energy levels
        """

        self.s0 = 0
        self.s1 = s1
        self.t1 = t1
        self.di = di
        self.f = f
        self.names = names

    def convert(self):
        """
        Converts the wavelengths of the energy levels from nm to cm^-1 and corrects the emission values.

        :return: Returns a tuple containing the converted values.
        """

        converted_s0 = self.s0
        converted_s1 = 1 / (self.s1 / (10**7))
        converted_t1 = 1 / (self.t1 / (10**7))
        converted_f = tuple([self.di - (1/(lam/(10**7))) for lam in self.f])

        return (converted_s0, converted_s1, converted_t1, self.di, converted_f)

    def generate_names(self, excited, levels):
        """

        :param excited: String representing the excited state
        :param levels: Number of energy levels
        :return: Returns the names of the energy levels
        """
        names = [r'$^7F_{}$'.format(x) for x in range(levels)]
        names = tuple([r"S_0", r"S_1", r"T_1"] + [excited] + names[::-1])
        self.names = names
        return names

    def display(self, title='', fname='test.png', xsep=0.1, size=400, names=()):
        """
        Creates an energy level diagram and saves it as a file.

        :param title: String that is the title of the energy level diagram.
        :param fname: String that is the file name of the figure.
        :param xsep: Float representing the separation of the two energy values.
        :param size: Float representing the size of the horizontal lines marking the energy levels.
        :param names: Tuple of names of the energy levels.
        :return: Saves a file of the energy level diagram as an svg.
        """
        if names == ():
            names = self.names

        fig = plt.figure(figsize=(2.7, 5))
        ax = fig.add_subplot(111)

        yvalues = self.convert()
        yvalues = yvalues[0:-1] + yvalues[-1]
        xvalues = tuple([0, 0, 0]+[xsep for x in range(len(yvalues)-3)])

        ax.scatter(xvalues, yvalues, s=size, marker='_')
        ax.set_ylabel('Energy (1/cm)')
        ax.set_title(title)
        ax.get_xaxis().set_ticks([])

        xoffset = 1
        for x,y,name in zip(xvalues, yvalues, names):
            xoffset = -1 * xoffset
            ax.annotate(name, xy=(x,y), xytext=(x-xsep/10 + xoffset*xsep/3.8, y), fontsize='x-small')

        fig.savefig(fname, dpi=500, bbox_inches='tight')