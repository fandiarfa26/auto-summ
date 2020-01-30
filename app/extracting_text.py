import PyPDF2

def extracting_text(file):
    
    pdfReader = PyPDF2.PdfFileReader(file)
    pageObj = pdfReader.getPage(0)

    return pageObj.extractText()