# main of Parser module

from Rss.first      import font_size
from Rss.JsonConv   import Source_handler
import sys
import os
import json





def main():
    
    if len(sys.argv) == 1:
        print("Input PDF file position")
        return
    if len(sys.argv) > 2:
        print("Too many Input")
        return

    fname, ext = os.path.splitext(sys.argv[1])
    filepath = "./"+fname+".json"
    if ext != ".pdf":
        print("Not PDF File\n")
        return

    filename = sys.argv[1]
    pdfRes = font_size(filename)
    ConvRes = Source_handler(pdfRes)
    

    #return JsonRes
    with open(filepath,'w') as fp:
        fp.write(json.dumps(ConvRes))

    print("final over")
    
        



if __name__ == '__main__':
    
    main()