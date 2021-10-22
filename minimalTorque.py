from numpy import array, linspace, arctan, tan, sin, cos
from matplotlib import pyplot as plt
from math import pi#, tan, atan, sin, cos




class graphVar():
    COLORS = ['#007f00', '#dc0000', '#000000', '#00007f', '#dbdb00', '#00c8c8', '#00c800', '#0000fa', '#ff9900',
              '#00ff7f', '#009e4e', '#00fef2', '#00a39a', '#ff00ff']

    def __init__(self, Dv, Dk, kn, k, minForce=1000):
        self.variable = {}
        self.variable['M'] = linspace(7, 18, 100)  # moment privitja [Nm]
        self.variable['Dv'] = Dv  # nazivni premer vijaka [mm]
        self.variable['Dk'] = Dk  # testni premer konusa [mm]
        self.variable['kn'] = kn  # korak navoja [mm]
        self.variable['kf'] = 0.2  # koeficient trenja [/]
        self.variable['T'] = 22  # maximalna temperatura [°C]
        self.variable['F'] = 1000  # sila privitja [N]
        self.units = {"M": "Nm",
                      "Dv": "mm",
                      "Dk": "mm",
                      "kn": "mm",
                      "kf": "",
                      "T": "°C",
                      "F": "N",
                      }
        self.cont = 'M'
        self.disc = 'kf'
        self.dicsVar = array([0.15, 0.2, 0.25, 0.3])
        self.k = k  #VW 414: 69.2  #PSA 166: 43.56;41.592 #[N/K]
        self.Tok = 22  # [C]
        self.minForce = minForce  # [N]

    def setCont(self, var, low, high):
        self.variable[var] = linspace(low, high, 100)
        self.cont = var

    def setDisc(self, var, val):
        self.dicsVar = array(val)
        self.disc = var

    def set(self, var, val):
        self.variable[var] = val

    def calculateF(self):
        self.variable["F"] = Graph.variable['M'] / (
                Graph.variable['Dv'] / 2 * tan(sin(Graph.variable['kn'] / (pi * Graph.variable['Dv'])) +
                                               arctan(2 * Graph.variable['kf'] / (3 ** (1 / 2)))) +
                Graph.variable['kf'] * Graph.variable['Dk'] / 2) * 1000

    def calculateM(self):
        self.variable["M"] = Graph.variable['F'] * (
                    Graph.variable['Dv'] / 2 * tan(sin(Graph.variable['kn'] / (pi * Graph.variable['Dv'])) +
                                                   arctan(2 * Graph.variable['kf'] / (3 ** (1 / 2)))) +
                    Graph.variable['kf'] * Graph.variable['Dk'] / 2) / 1000

    def calculateT(self):
        self.variable["T"] = (self.variable["F"] - self.minForce) / self.k + self.Tok

    def updateVariables(self, variable):
        if variable == "M":
            self.calculateM()
        elif variable == "F":
            self.calculateF()
        elif variable == "T":
            if self.disc != "M" and self.cont != "M":
                return None
            elif self.disc != "F" and self.cont != "F":
                self.calculateF()
            self.calculateT()
        return self.variable[variable]

    def plotVariable(self, var, title=None):
        graph, ax1 = plt.subplots(figsize=(8, 5))  # figure()
        if title is not None:
            plt.title(title)
        xLabel = "{0} [{1}]".format(self.cont, self.units[self.cont])
        yLabel = "{0} [{1}]".format(var, self.units[var])
        ax1.set_xlabel(xLabel)
        ax1.set_ylabel(yLabel)
        plt.grid(which='major')
        for i in range(len(Graph.dicsVar)):
            self.variable[self.disc] = self.dicsVar[i]
            if self.updateVariables(var) is not None:
                ax1.plot(Graph.variable[Graph.cont], Graph.variable[var], color=Graph.COLORS[1 - i],
                         label=Graph.disc + '=' + str(Graph.variable[Graph.disc]) + self.units[Graph.disc])
        ax1.legend(loc=1)
        plt.show()






if __name__ == "__main__":
    Graph = graphVar(Dv=10, Dk=7, kn=1, k=69.2, minForce=1000)
    Graph.setCont('kf', 0.2, 0.3)
    Graph.setDisc('F', [7500, 10000])  #
    Graph.plotVariable("M", "lala")

# graph, ax1 = plt.subplots(figsize=(8, 5))  # figure()
# # plt.hold(True)
# plt.title('Minimum sealing force curve')#'Bolt pretension curve') #
# # plt.title('F(' + Graph.cont + ')')
# ax1.set_xlabel('coefficient of friction [/]')
# ax1.set_ylabel('T [°C]')#'F [N]')  #
# plt.grid(which='major')
# # print(len(Graph.variable['M']))
# for i in range(len(Graph.dicsVar)):
#     Graph.variable[Graph.disc] = Graph.dicsVar[i]
#     # force2 = Graph.variable['M'] / (Graph.variable['Dv'] / 2 * (
#     #             Graph.variable['kn'] + 2 * Graph.variable['kf'] * pi * Graph.variable['Dv'] / (3 ** (1 / 2))) / (
#     #                                            pi * Graph.variable['Dv'] - 2 * Graph.variable['kf'] * Graph.variable[
#     #                                        'kn'] / (3 ** (1 / 2)))) * 1000
#     force = Graph.variable['M']/(Graph.variable['Dv']/2*tan(sin(Graph.variable['kn']/(pi*Graph.variable['Dv']))+
#                                 arctan(2*Graph.variable['kf']/(3 ** (1 / 2)))) +
#                                  Graph.variable['kf']*Graph.variable['Dk']/2)*1000
#     # print(len(force))
#     # print(force)
#     Tmax = (force - minForce) / k + Tok
#     ax1.plot(Graph.variable[Graph.cont], Tmax, color=Graph.COLORS[1 - i],
#              label=Graph.disc + '=' + str(Graph.variable[Graph.disc]) + 'Nm')
#
#
# ax1.legend(loc=1)
#
# # /(3**(1/2))
# plt.show()
#plt.savefig('F(' + Graph.cont + '-' + Graph.disc + ')' + '.pdf', format='pdf')