from xml.dom import minidom
import urllib.request
# import urllib

# usage: python gettingMyCorpus.py

# en el corpus que baje, guarde 350 de los 9158 articulos de la query por que
# ya pesa 14M el archivo


def PmcCorpusGenerator(query, outFile="myCorpus.txt"):
    """
    Downloads scientific papers from PubMedCentral.

    query -- Query to filter papers.
    outFile -- File path to save results file (will be appended if exists).
    """
    queryUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"  # api de ncbi
    database = "pmc"  # quiero articulos cientificos de PubMed Central

    completeUrl = queryUrl + "esearch.fcgi?db=" + database + "&term=" + query
    completeUrl += "&retmax=40000"
    xmlStr = urllib.request.urlopen(completeUrl).read()
    xmlDoc = minidom.parseString(xmlStr)
    ids = xmlDoc.getElementsByTagName('Id')
    i = 0
    total = len(ids)
    f = open(outFile, 'a')  # append papers to our outFile
    for actId in ids:
        i += 1
        actPaper = getPaper(actId.childNodes[0].data)
        f.write(actPaper)
        print(str(i) + " from " + str(total))
    f.close()


def getText(nodelist):
    """
    Gets all text from a nodelist object

    nodelist -- nodelist object to get the text
    """
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        else:
            rc.append(getText(node.childNodes))
    return ''.join(rc)


def getPaper(actId):
    downloadUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    downloadUrl = downloadUrl + "efetch.fcgi?db=pmc&id=" + actId
    xmlStr = urllib.request.urlopen(downloadUrl).read()
    xmlDoc = minidom.parseString(xmlStr)

    fullArticle = ""

    abstract = xmlDoc.getElementsByTagName('abstract')
    if (len(abstract) > 0):
        fullArticle += getText(abstract[0].childNodes)

    body = xmlDoc.getElementsByTagName('body')
    if (len(body) > 0):
        fullArticle += getText(body[0].childNodes)
    return fullArticle


PmcCorpusGenerator("\"breast+cancer\"AND\"gene+ontology\"")
