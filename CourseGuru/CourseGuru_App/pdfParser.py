import nltk
import re

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator

from nltk.corpus import stopwords
from nltk.tokenize.moses import MosesDetokenizer

from CourseGuru_App.models import keywords
from CourseGuru_App.models import botanswers
from pip._vendor.html5lib.treewalkers.base import DOCTYPE

#testing PRP
#def restructForDB (text): 
def restructForDB (text, cid, catID, fileid): 
    detokenizer = MosesDetokenizer() 
    botSearch = text.replace('<br>', '')
    rgx = re.compile('[^a-zA-Z0-9 \n\.]')
    
    botSearch = rgx.sub('', botSearch)
    searchList = nltk.word_tokenize(botSearch, 'english')
    
    botSearch = [word for word in searchList if word not in stopwords.words('english')]
    
    detokenizer.detokenize(botSearch, return_str=True)
    botSearch = ' '.join(botSearch)
    botSearch = botSearch.lower()
    
    botanswers.objects.create(answer = text, rating = 0, category_id = catID.id, entities = botSearch, course_id = cid, file_id = fileid)
#testing PRP    
#    print(botSearch)
#    print(text)
    
def restructString(text):
    #change \n to <br>
    filtText = re.sub('\\n', '<br>', text)
    #getting rid of non ASCII unicode characters which cause errors
    filtText= ''.join(i for i in filtText if ord(i)<128)
    #getting rid on any unnecessary extra spaces or <br> tags 
    filtText = re.sub(' +', ' ', filtText)
    filtText = re.sub('<br>\ ', '<br>', filtText)
    filtText = re.sub('(<br>)+', '<br>', filtText)
    #get rid of first character in the string if its a space 
    if filtText[0] == ' ': 
        filtText=filtText[1:]
    
    return filtText

def pdfToText(file, cid, catID, fileid, docType):
    #Create empty string for text to be extracted into
    keyWordObj = keywords.objects.exclude(categoryKeyWords=None)
      
    keyWords = []
    for n in keyWordObj:
        keyWords.append(n.categoryKeyWords)
    extracted_text = '' 
  
    #Sets the cursor back to 0 in f to be parsed and sets the documents and parser
    file.seek(0)
    parser = PDFParser(file)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
   # doc.encode('utf-8')
    rsrcmgr = PDFResourceManager()
    #sets parameters for analysis 
    laparams = LAParams()
            
    #Required to define separation of text within pdf
    laparams.char_margin = 1
    laparams.word_margin = 1
            
    #Device takes LAPrams and uses them to parse individual pdf objects
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
      
    dataArray = []     
       
#testing PRP
#    botSearchArray = []
    if docType == 'Syllabus':    
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                #if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                if isinstance(lt_obj, LTTextBoxHorizontal):
                    extracted_text = lt_obj.get_text()
                    filtText = restructString(extracted_text)                  
                    added = False
                        
                    for n in keyWords:
                        if (n.lower() in filtText.lower()) and (added == False) and (len(n) > 2 ):
                            dataArray.append(filtText)
                            keyWords.remove(n)
                            added=True
                        elif (len(n) < 3) and (re.match(('[a-zA-Z]*' + re.escape(n) +'[a-zA-Z]*'), filtText) != None):
                            if (n in filtText) and (added == False):
                                dataArray.append(filtText)
                                keyWords.remove(n)
                                added=True
      
                        elif(n.lower() in filtText.lower()) and (added == True):
                            keyWords.remove(n)
                              
                    if (len(dataArray) > 0) and (added == False):
                        #checking for empty lines or lines with just a page number
                        if (filtText != ' <br>') and (re.match('[0-9]* <br>', filtText) == None) and (filtText != '<br>'):
                            dataArray[-1] += ' ' + filtText
                          
                    elif len(dataArray)==0: 
                        dataArray.append('Course Information: ' + filtText)
    elif docType == 'Lectures':      
        for page in doc.get_pages():
            dataArray.append('')
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                #if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                if isinstance(lt_obj, LTTextBoxHorizontal):
                    extracted_text = lt_obj.get_text()
                    filtText = restructString(extracted_text)    
                    #checking for empty lines or lines with just a page number
                    if (filtText != ' <br>') and (re.match('[0-9]* <br>', filtText) == None) and (filtText != '<br>'):
                        dataArray[-1] +='' + filtText
    
    for n in dataArray: 
        restructForDB(n, cid, catID, fileid)
#        botSearchArray.append(restructForDB(n))                      
    file.close()
    #return textFile




