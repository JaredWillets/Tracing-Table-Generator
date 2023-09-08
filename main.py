from intermediate_converter import javaToIM
from start_html import run as exportToHTML

def generateHistory(translatedLoop):
    
    splitLoop = translatedLoop.split('\n')
    variableList = []

    startLine = 0
    condition = ""
    initializationStatement = ""
    loopStatement = ""
    for lineNumber, line in enumerate(splitLoop):
        if line.startswith('cond: '):
            condition = line.split('cond: ')[1]
        if line.startswith('var: '):
            exec(line.split('var: ')[1])
            variableList.append(line.split('var: ')[1].split('=')[0].strip())
        if line.startswith('startloop'):
            startLine = lineNumber + 1
        if line.startswith('init: '):
            initializationStatement += line.split('init: ')[1]+";\n"
        if line.startswith('loop: '):
            loopStatement = line.split('loop: ')[1]

    if loopStatement == "":
        loopStatement = f"while ({condition}) "
        loopStatement += "{"

    history = [{} for _ in range(startLine, len(splitLoop)+2)]
    for variable in variableList:
        for document in history:
            document[variable] = [locals()[variable]]
    tracingTable = []

    loopActions = splitLoop[startLine:]
    while eval(condition):
        history[1] = history[-1]
        for lineNumber, line in enumerate(loopActions):
            exec(line)
            for variable in variableList:
                if history[lineNumber + 2][variable][-1] != locals()[variable]:
                    history[lineNumber + 2][variable].append(locals()[variable])
    return history, initializationStatement, loopActions, condition, loopStatement

def getHistoryString(string, final = False):
    finalString = ""
    if not final:
        for varNum, var in enumerate(string):
            finalString += "<strong>"+var +"</strong> = "
            for valNum, val in enumerate(string[var]):
                if valNum != len(string[var])-1:
                    finalString += "<s>"
                else:
                    finalString += "<strong>"
                finalString += f"{round(val,3)}"                    
                if valNum != len(string[var])-1:
                    finalString += "</s>"
                    finalString += " "
                else:
                    finalString += "</strong>"
            if varNum != len(string)-1: finalString += ", "
    else:
        finalString += "<strong>"
        for varNum, var in enumerate(string):
            finalString += var +" = "                
            finalString += f"{round(string[var][-1],3)}"
                
            if varNum != len(string)-1: finalString += ", "
        finalString += "</strong>"
    return finalString

def renderTracingTable(historyTable, initializationStatement, loopActions, condition, loopStatement):
    finalString = """
        <style>
            * {font-family: "Courier New", monospace;}
            td {
            border: 2px solid black;
            padding: 1vh 5vw;
            padding-left: 2vw;
            }
            table {border-collapse:collapse;}
            s {color:#777;}
        </style>
    """
    finalString += "<table>"
    for docNum, document in enumerate(historyTable):
        if docNum == 0:
            finalString += f"<tr><td>{initializationStatement}</td><td></td></tr>"
            finalString += f"<tr><td></td><td>{getHistoryString(document)}</td></tr>"
        elif docNum == 1:
            finalString += f"<tr><td>{loopStatement}</td><td></td></tr>"
            finalString += f"<tr><td></td><td>{getHistoryString(document)}</td></tr>"
        else:
            finalString += f"<tr><td>&emsp;{loopActions[docNum - 2]};</td><td></td></tr>"
            finalString += f"<tr><td></td><td>{getHistoryString(document)}</td></tr>"
    finalString += "<tr><td>}</td><td></td></tr>"
    finalString += f"<tr><td></td><td>{getHistoryString(historyTable[1], final = True)}</td></tr>"
    finalString += "</table>"
    return finalString
        



im = javaToIM(open("code.java",'r').read())
history, initializationStatement, loopActions, condition, loopStatement = generateHistory(im)
html = renderTracingTable(history, initializationStatement, loopActions, condition, loopStatement)
exportToHTML(html)
