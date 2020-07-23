# input : [[title],[author],[source]] 
# output : .json file with title, author, source field
# this module work for preprocessing the input list data

import json
import sys
import os

def Source_handler(result_list):
    toJson = {}
    
    toJson["Title"] = result_list[0]
    #del(result_list[0])
    toJson["Author"] = result_list[1]
    #del(result_list[0])
    toJson["Source"] = result_list[2]


    return toJson
    