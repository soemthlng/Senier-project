from pdfminer.helpers import absolute_sample_path
from pdfminer.layout import LTChar, LTTextBox
from pdfminer.high_level import custom_extract_pages
import re


def font_size(filename):
    #path = absolute_sample_path('IEEE_official_1.pdf')
    #path = absolute_sample_path('b.pdf')
    if filename == None:
        path = absolute_sample_path('IEEE_official_1.pdf')
    else:
        path = absolute_sample_path(filename)
    upper_y = Abstract_finder(path) # find the upper y coordinate
    collecter = []
    ##preface = [] ######################################
    contents_height = [[0,0]]################################################
    index = 0
    
    final_result = []   # for passing the result to txt2json module. format --> [["title"],["author"]]

    #print("upper y : ", upper_y)   # printing Abstract upper y coordinate

    # this if phrase for exception handling.
    # if parsing is incomplete (e.g. scanned copy) than, upper_y value is None.
    if upper_y == None:
        print("Can`t find Abstract-\n")
        return

    for page in custom_extract_pages(path, '', [0]):
        #print('page',page)
        for text_box in page:
            #print('text_box',text_box.bbox)###################################################
            if isinstance(text_box,LTTextBox):
                for line in text_box:
                    line_height=round(line.height,3)
                    #print('line',line,line_height)
                    for x,y in contents_height:
                        #print(x,y,index)
                        if x==line_height:
                            line_height=0
                            break
                        index=index+1
                    
                    if line_height == 0:
                        contents_height[index][1]=contents_height[index][1]+1
                    else :
                        contents_height.append([line_height,1])
                        
                    index = 0
                    if line.y1 > upper_y:   # text line box which is greater than Abstract part == means title and author is here

                        chaser = line.get_text().strip()
                        #print('chaser',chaser,'line.y1',line.y1)
                        collecter.append((line.liner()[0],chaser,line.finder()))###########################3
                    else:
                        continue
                        
    #print('Height',sorted(contents_height, key=lambda contents_height: contents_height[1],reverse=True))     
    Average_height=sorted(contents_height, key=lambda contents_height: contents_height[1],reverse=True)[0][0]
    #print('Average',Average_height)
    #print('collecter',collecter)
    #source = parse_all(path)###########################################################
    
    final_format = []
    
    TnA = extracter(collecter)#############################################################
    #print('TnA',TnA[0])
    #print('h',TnA[1])
    final_format += TnA[0]###########################################
    
    source = parse_all(path,TnA[1],Average_height)########################################
    
    final_format.append(source)
    #print('final',final_format[0],final_format[1],final_format[2])
    
    print("\npreprocess over\n")

    return final_format

# purpose of Abstract_finder is finding Abstract- indicater in Papers
# catch the line and return Abstract line boxes upper y coordinate

def Abstract_finder(path):

    checker = re.compile("(Abstract).*?")   # what i want is finding abstract string
    for page in custom_extract_pages(path,'',[0]):
        for text_box in page:
            if isinstance(text_box, LTTextBox):
                #testing = text_box.get_it()
                #print("stealer work? : ")
                #print(testing[0], testing[1])
                for line in text_box:
                    # chaser is actual line of page. either number nor text
                    chaser = line.get_text().strip()
                    #print(chaser) # print the line of pdf
                    tester = checker.findall(chaser)
                    if tester:                      # means Abstract is found
                        #print("Abstract find!!\n")
                        # just line.y1
                        #is_y = line.finder()#11111111111111111111111111111111111111111111111111
                        is_y = round(line.finder(),3)
                        return is_y

# extracter module for taking title and author of Paper
# compare with upper_y coordinate and return list
# if title or author splited several line, than concatnate it into 1 line

def extracter(collecter):
    a = collecter[0][0]
    b = 0.0
    h = 0.0#########################
    title = []
    author = []
    for cntr in collecter:
        #print('cntr',cntr)
        if a <= cntr[0]:
            a = cntr[0]
            h = cntr[2]###############################################
            #print('H',cntr[2])
    #print("\n",a,"\n") 
    for ctr in collecter:
        if ctr[0] == a:
            title.append(ctr[1])
            continue
        #print("ctr[0] is : ",ctr[0])
        if b < ctr[0]:
            b = ctr[0]
            #print("ctr change occur. b : ctr ",b," : ",ctr[0])
    #print("\n",b,"\n")

    # now here a is size of title and b is size of author
    for taker in collecter:
        if taker[0] == b:
            author.append(taker[1])

    #print("title : ",h)##################################################################
    #print("author : ",author)

    real_title = ' '.join(title)
    real_author = ' '.join(author)

    #print("real_title : ", real_title)
    #print("real_author : ", real_author)

    return ([[real_title],[real_author]],h)############################################

def parse_all(path, hy, Average_height):#############################################################

    text = []
    wordParse = []
    
    for page in custom_extract_pages(path):
        #print('page',page.bbox)
        page_height=(page.bbox[1]+page.bbox[3])/2
        #print('page_height',page_height)
        for text_box in page:
            if isinstance(text_box, LTTextBox):
                #testing = text_box.get_it()
                #print("stealer work? : ")
                #print(testing[0], testing[1])
                if text_box.bbox[1]>hy:################################3
                    continue            ####################################
                for line in text_box:
                    #if line.y1 >= hy:#######################################
                    #    continue #############################
                    # chaser is actual line of page. either number nor text
                    if text_box.bbox[3]<page_height:
                        if round(line.height,3)<Average_height:
                            #print('print',line,line.height)
                            continue
                    chaser = line.get_text().strip()
                    #print('chaser',chaser) # print the line of pdf
                    #wordParse += chaser.split()
                    text.append(chaser)
                    wordParse=" ".join(text)
    #print("wordParse: ",wordParse)
    return wordParse

                    
if __name__ == '__main__':
    font_size()
    print("over")

