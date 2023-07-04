#write a function to load json files and parse them
import json
import os
import numpy as np
import matplotlib.pyplot as plt

path = "/home/shailja/ismrmMethodOutput/"
methods = os.listdir(path)
csvfile = open(path+'results.csv', 'w')
for method in methods:
    #read json file
    try:
        with open(path+method+"/results.json") as f:        
            data = json.load(f)
            bundles = data['bundle_wise'].keys()
            for bundle in bundles:
                for metric in data['bundle_wise'][bundle].keys():               
                    print(bundle,metric,data['bundle_wise'][bundle][metric])
                    #save as a row in csv file csvfile
                    csvfile.write(method+","+bundle+","+metric+","+str(data['bundle_wise'][bundle][metric])+"\n")
    except:
        print("error in reading file",method)
        continue            