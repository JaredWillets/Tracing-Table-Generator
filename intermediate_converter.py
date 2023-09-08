def javaToIM(javaString):
    imString = ""
    finalArray = []
    javaSplit = javaString.split('\n')
    for newLineSplit in javaSplit:
        split = newLineSplit.split(';')
        for el in split:
            el = el.strip();
            el = el.replace('\t','')
            if el.strip() != "":finalArray.append(el)
    finalArray.remove('}')
    for lineNumber, line in enumerate(finalArray):
        if line.startswith('int '):
            imString += "var: "
            imString += line.split('int ')[1]
            imString += "\n"
            imString += "init: "
            imString += line
        elif line.startswith('double '):
            imString += "var: "
            imString += line.split('double ')[1]
            imString += "\n"
            imString += "init: "
            imString += line
        elif line.startswith('while'):
            imString += 'cond: '
            imString += line.split('(')[1].split(')')[0]+"\n"
            imString += "startloop"
        else:
            imString += line
        if lineNumber != len(finalArray)-1:imString += "\n"
            
    return imString
