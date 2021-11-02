from numpy import array, linspace, arctan, tan, sin, cos
from matplotlib import pyplot as plt
from math import pi#, tan, atan, sin, cos




class graphVar():
    COLORS = ['#007f00', '#dc0000', '#000000', '#00007f', '#dbdb00', '#00c8c8', '#00c800', '#0000fa', '#ff9900',
              '#00ff7f', '#009e4e', '#00fef2', '#00a39a', '#ff00ff']

    def __init__(self, Dv, Dk, kn, kF, minForce=None):
        self.variable = {}
        self.defaultVal = {}
        self.variable['M'] = linspace(7, 18, 100)  # moment privitja [Nm]
        self.variable['Dv'] = Dv  # nazivni premer vijaka [mm]
        self.variable['Dk'] = Dk  # testni premer konusa [mm]
        self.variable['kn'] = kn  # korak navoja [mm]
        self.variable['kf'] = 0.25  # koeficient trenja [/]
        self.variable['T'] = 22  # maximalna temperatura [°C]
        self.variable['F'] = 0  # sila privitja [N]
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
        self.kF = kF  #[N/K] #VW 414: 69.2  #PSA 166: 43.56;41.592
        self.Tok = 22  # [C]
        if minForce is None:
            self.minForce = Dk**2*pi*7
        else:
            self.minForce = minForce  # [N]
        self.defaultVal['M'] = 15  # moment privitja [Nm]
        self.defaultVal['Dv'] = Dv  # nazivni premer vijaka [mm]
        self.defaultVal['Dk'] = Dk  # testni premer konusa [mm]
        self.defaultVal['kn'] = kn  # korak navoja [mm]
        self.defaultVal['kf'] = 0.25  # koeficient trenja [/]
        self.defaultVal['T'] = 22  # maximalna temperatura [°C]
        self.defaultVal['F'] = 0#self.minForce  # sila privitja [N]

    def setCont(self, var, low, high):
        if self.disc != self.cont:
            self.variable[self.cont] = self.defaultVal[self.cont]
        self.variable[var] = linspace(low, high, 100)
        self.cont = var



    def setDisc(self, var, val):
        if self.disc != self.cont:
            self.variable[self.disc] = self.defaultVal[self.disc]
        self.dicsVar = array(val)
        self.disc = var


    def setVar(self, var):
        self.var = var

    def set(self, var, val):
        self.variable[var] = val

    def getMissingVar(self):
        if self.cont != "M" and self.disc != "M" and self.var != "M":
            return "M"
        elif self.cont != "kf" and self.disc != "kf" and self.var != "kf":
            return "kf"

    def calculateF(self, includeT=False, minF=0):
        if includeT:
            TF = (self.variable['T']-self.Tok)*self.kF
        else:
            TF = 0
        self.variable["F"] = self.variable['M'] / (
                self.variable['Dv'] / 2 * tan(sin(self.variable['kn'] / (pi * self.variable['Dv'])) +
                                               arctan(2 * self.variable['kf'] / (3 ** (1 / 2)))) +
                self.variable['kf'] * self.variable['Dk'] / 2) * 1000 - TF - minF

    def calculateM(self, Fmin=None):
        if Fmin:
            minF = Fmin
        else:
            minF = 0
        #print(minF, self.variable['F'])
        self.variable["M"] = (self.variable['F'] + minF + (self.variable['T']-self.Tok)*self.kF) * (
                    self.variable['Dv'] / 2 * tan(sin(self.variable['kn'] / (pi * self.variable['Dv'])) +
                                                   arctan(2 * self.variable['kf'] / (3 ** (1 / 2)))) +
                    self.variable['kf'] * self.variable['Dk'] / 2) / 1000

    def calculateT(self, includeFmin=False):
        if includeFmin:
            minF = self.minForce
        else:
            minF = 0
        self.variable["T"] = (self.variable["F"] - minF) / self.kF + self.Tok

    def calculateFfromT(self):
         self.variable["F"] = (self.variable["T"] - self.Tok)*self.kF



    def updateVariables(self, variable, minF):
        if variable == "M":
            if self.disc != "F" and self.cont != "F":
                self.calculateM(Fmin=self.minForce)
            else:
                self.calculateM()
        elif variable == "F":
            if self.cont == "T":
                self.calculateFfromT()
            elif self.disc == "T":
                self.calculateF(True)
            else:
                self.calculateF()
        elif variable == "T":
            if self.disc != "F" and self.cont != "F":
                self.calculateF(includeT=False)
            if self.cont == "M":
                self.calculateF(minF=minF)
            if self.cont == "F":
                self.calculateT(False)
            else:
                self.calculateT(True)
        return self.variable[variable]

    def plotVariable(self, title=None, includeFmin=False):
        graph, ax1 = plt.subplots(figsize=(8, 5))  # figure()
        if title is not None:
            plt.title(title)
        xLabel = "{0} [{1}]".format(self.cont, self.units[self.cont])
        yLabel = "{0} [{1}]".format(self.var, self.units[self.var])
        ax1.set_xlabel(xLabel)
        ax1.set_ylabel(yLabel)
        plt.grid(which='major')
        for i in range(len(self.dicsVar)):
            if self.cont == "M" and self.disc == "F":
                minF = self.dicsVar[i]
                lab = str(self.dicsVar[i])
            else:
                self.variable[self.disc] = self.dicsVar[i]
                minF = 0
                lab = str(self.variable[self.disc])
            if self.updateVariables(self.var, minF=minF) is not None:
                ax1.plot(self.variable[self.cont], self.variable[self.var], color=self.COLORS[1 - i],
                         label=self.disc + '=' + lab + self.units[self.disc])
        specialPair = ("T", "F")
        if self.var not in specialPair or self.cont not in specialPair:
            ax1.legend(loc=1)
        plt.show()






if __name__ == "__main__":
    # tests
    testDict = {"T": {"cont": [22, 150], "disc": [22, 100, 150]},
                "F": {"cont": [0, 10000], "disc": [7000, 10000, 14000]},
                "M": {"cont": [0, 20], "disc": [10, 15, 20]},
                "kf": {"cont": [0.1, 0.5], "disc": [0.1, 0.3, 0.5]},
                }
    testGroups = {"T": {"kf": ["M", "F"], "F": ["M"], "M": ["F"]},
                  "F": {"kf": ["M", "T"], "T": ["M"], "M": ["T"]},
                  "kf": {"F": ["M"], "T": ["F", "M"], "M": ["F", "T"]},
                  "M": {"kf": ["T", "F"], "F": ["T"], "T": ["F"]},
                  }
    #testGroups = {"kf": {"T": ["M"]}}
    for cont in testGroups:
        for disc in testGroups[cont]:
            for var in testGroups[cont][disc]:
                print("Ploting\tcont: {0}\n\t\tdiscr: {1}\n\t\tvar: {2}".format(cont, disc, var))
                Graph = graphVar(Dv=10, Dk=7, kn=1, kF=69.2, minForce=1000)
                Graph.setCont(cont, *testDict[cont]["cont"])
                Graph.setDisc(disc, testDict[disc]["disc"])  #
                Graph.setVar(var)
                Graph.plotVariable("{0}({1}, {2})".format(var, cont, disc))
                print("---------------------------\n\n")

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
#     Tmax = (force - minForce) / kF + Tok
#     ax1.plot(Graph.variable[Graph.cont], Tmax, color=Graph.COLORS[1 - i],
#              label=Graph.disc + '=' + str(Graph.variable[Graph.disc]) + 'Nm')
#
#
# ax1.legend(loc=1)
#
# # /(3**(1/2))
# plt.show()
#plt.savefig('F(' + Graph.cont + '-' + Graph.disc + ')' + '.pdf', format='pdf')