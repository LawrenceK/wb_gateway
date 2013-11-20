#  General graph utility functions
#  Andy Harris March 2009
#
from xml.etree.ElementTree import ElementTree
from urllib2 import urlopen

def getData(name):
    #
    #  Return data as xml element blob, or nothing (or should this be an empty list)
    #
    try:
        d = ElementTree(file=urlopen(name))
        return d
    except:
        return "''"

def removeCol(xmlblob,col,ent='entry'):
    #
    #  Remove column from an xml dataset
    #
    newblob =[]
    lines = xmlblob.findall(ent)
    for i in range(0,len(lines)):
        lines[i].remove(lines[i][col])
    return lines

    
def getvals(xmlblob,name):
	vals = []
	for final in xmlblob.findall('entry'):
		for cell in final.findall(name):
			try:
				vals.append(float(str(cell.text)))
			except:
				vals.append(0)
	return str(vals)

def getTimes(xmlblob,name):
	vals = []
	for final in xmlblob.findall('entry'):
		for cell in final.findall(name):
			try:
				vals.append(str(cell.text)[0:5])
			except:
				vals.append("None")
	return str(vals)	
	
def getDate(xmlblob,name):
	for final in xmlblob.findall('entry'):
		for cell in final.findall(name):
			try:
				return (str(cell.text))
			except:
				return ("None")

def getNames(xmlblob, rType='string'):
    # return all the names of the elements in 'entry'
    # except 'date' and 'time' therefore the array is logged entities
    vals = []
    global names
    t = xmlblob.find('entry')
    e = list(t)
    for n in e:
        if (n.tag != 'date') and (n.tag != 'time'):
            vals.append(n.tag)
            names = vals
    if (rType=='string'):
        return str(vals)
    if (rType!='string'):
        return vals

def addUnits(lObj,nList):
    #
    #  Add units of measurement to lObj based on names
    #
    names = {}
    names[0] = ""   # this is an uncomfortable fiddle because some lists might have date and time
    for i in range(0,len(nList)):
        if (nList[i].split('.')[1]):    
            names[i+1] = nList[i].split('.')[1]
            
    for i in range(0,len(lObj)):
        for n in range(0,len(names)):
            lObj[i][n].text = lObj[i][n].text + names[n]
    return lObj

    
def doJSdatasets(lNames,xmlblob):
    #  this function is to deliver a list of datasets to Javascript with all the pointers in place
    #  JS should look like:     dataset[0] = [list of vales]
    jLines = ""
    for i in range(0,len(lNames)):
        jLine = "dataset[%d] = %s ; \n" % (i,getvals(xmlblob,lNames[i]))
        jLines = jLines + jLine
    return jLines