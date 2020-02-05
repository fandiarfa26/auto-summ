import PyPDF2

def extracting_text(file):

    # create a pdf reader
    pdfReader = PyPDF2.PdfFileReader(file)

    # get total pdf page number
    totalPageNumber = pdfReader.numPages
    fulltext = ''

    for p in range(0, totalPageNumber):
        pageObj = pdfReader.getPage(p)
        fulltext += pageObj.extractText()
    
    #print(fulltext)

    return fulltext.replace('\n', '').replace('  ',' ')