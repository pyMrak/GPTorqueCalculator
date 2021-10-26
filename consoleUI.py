import minimalTorque

errFloatMsg = "Napaka: Vnešena vrednost ni številska."
errContPck = "Napaka: Izbrana možnost ni veljavna."

print("Program za izračun potrebnega momenta privitja ohišja čepne svečke.")
print("Izdelal Andrej M. (C)")
print("Za podrobnejša navodila glej 'Navodila.pdf'")
print("\n")


varDict = {
    "kF": {"value": None,
           "input": "Koeficient padanja sile s temperaturo (v N/°C): ",
           "blank": False
           },
    "Dv": {"value": None,
           "input": "Imenski premer navoja (v mm): ",
           "blank": False
           },
    "kn": {"value": None,
           "input": "Korak navoja (v mm): ",
           "blank": False
           },
    "Dk": {"value": None,
           "input": "Testni premer konusa (v mm): ",
           "blank": False
           },
    "minF": {"value": None,
           "input": "Minimalna sila tesnenja (v N) - lahko prazno: ",
           "blank": True
           },
}

minMaxDict = {
    "min": {"value": None,
           "input": "Vpiši minimalno vrednost [{}]: ",
           },
    "max": {"value": None,
           "input": "Vpiši maksimalno vrednost [{}]: ",
           },
}

for varName in varDict:
    while True:
        var = input(varDict[varName]["input"])
        if varDict[varName]["blank"]:
            if var == "":
                varDict[varName]["value"] = None
                break
        try:
            varDict[varName]["value"] = float(var)
            break
        except ValueError:
            print(errFloatMsg)

Graph = minimalTorque.graphVar(Dv=varDict["Dv"]["value"],
                               Dk=varDict["Dk"]["value"],
                               kn=varDict["kn"]["value"],
                               kF=varDict["kF"]["value"],
                               minForce=varDict["minF"]["value"])

exit = ""
while exit != 'e':
    while True:
        cont = input("Izberi količino na X osi (možnosti: 'kf', 'F', 'M' in 'T'): ")
        if cont in ["kf", "F", "M", "T"]:
            break
        else:
            print(errContPck)
    for varName in minMaxDict:
        while True:
            var = input(minMaxDict[varName]["input"].format(Graph.units[cont]))
            try:
                minMaxDict[varName]["value"] = float(var)
                break
            except ValueError:
                print(errFloatMsg)
    Graph.setCont(cont, minMaxDict["min"]["value"], minMaxDict["max"]["value"])

    inputOpt = []
    inputText = "Izberi diskretno količino (možnosti:"
    for var in ["kf", "F", "M", "T"]:
        if var != Graph.cont:
            inputOpt.append(var)
            inputText += " " + var
    inputText += "): "
    while True:
        disc = input(inputText)
        if disc in inputOpt:
            break
        else:
            print(errContPck)
    discVals = []
    add = ""
    while True:
        while True:
            val = input("Izberi vrednost diskretne količine '{0}' [{1}]{2}: ".format(disc, Graph.units[disc], add))
            if len(discVals) and val == "":
                break
            try:
                discVals.append(float(val))
                add = " (pusti prazno za prekinitev)"
                break
            except ValueError:
                print(errFloatMsg)

        if val == "":
            break
    Graph.setDisc(disc, discVals)

    specialPair1 = ("T", "F")
    allowed = ('F', 'M', 'T')
    if Graph.cont in specialPair1 and Graph.disc in specialPair1:
        graph = "M"
    elif Graph.cont in "kf" and Graph.disc in "F":
        graph = "M"
    else:
        Yvar = []
        inputText = "Izberi količino na Y osi (možnost"
        for var in allowed:
            if var != Graph.disc and var != Graph.cont:
                if False:#var == "T":
                    if "F" != Graph.disc and "F" != Graph.cont:
                        Yvar.append(var)
                        inputText += " " + var
                else:
                    Yvar.append(var)
                    inputText += " " + var
        inputText += "): "
        if len(Yvar) == 1:
            graph = Yvar[0]
        else:
            while True:
                graph = input(inputText)
                if graph in Yvar:
                    break
                else:
                    print(errContPck)
    Graph.setVar(graph)
    missDict = {"M": "Izberi vrednost momenta v Nm:",
                "kf": "Izberi vrednost koeficienta trenja: ",
    }
    if graph not in specialPair1 or Graph.cont not in specialPair1:
        missingVar = Graph.getMissingVar()
        if missingVar is not None:
            while True:
                val = input(missDict[missingVar])
                try:
                    val = float(val)
                    Graph.set(missingVar, val)
                    break
                except ValueError:
                    print(errFloatMsg)

    title = input("Vnesi naslov grafa (lahko prazno): ")
    if title == "":
        title = None

    print("Zapri graf za nadaljevanje...")
    Graph.plotVariable(title)

    exit = input("Vnesi 'e' za izhod ali 'Enter' za nadaljevanje: ")
    print("------------------------------------------------\n\n")
