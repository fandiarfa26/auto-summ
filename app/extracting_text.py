import PyPDF2

def extracting_text(file):
    
    pdfReader = PyPDF2.PdfFileReader(file)
    fulltext = ''

    for p in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(p)
        fulltext += pageObj.extractText()

    return fulltext