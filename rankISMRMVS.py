import json
import os
import numpy as np
import matplotlib.pyplot as plt
import csv

# Define file paths
path = "/home/shailja/ismrmMethodOutput/"
csvfile = path + 'retrace.csv'

# Initialize dictionaries and lists
metric_dic = {}
methods = []
bundles = []
metric = ["topological_distance", "number_of_nodes", "number_of_edges", "average_degree", 
               "diameter"]

# Load csv file and store the rows
file_rows = []
with open(csvfile, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        file_rows.append(row)
        methods.append(row[0])
        bundles.append(row[1])

# Remove duplicates from methods and bundles lists
methods = list(set(methods))
bundles = list(set(bundles))

# Initialize metric_dic with None for each combination of method, bundle, and metric
for m in metric:
    metric_dic[m] = {}
    for b in bundles:
        metric_dic[m][b] = {}
        for method in methods:
            metric_dic[m][b][method] = None

# Update metric_dic with data from each row
for row in file_rows:
    for i, m in enumerate(metric):
        metric_dic[m][row[1]][row[0]] = row[i+2]

# Load ISMRM mapping names from csv file
ismrm_map = {}
with open(path + 'ismrm_method_mapping_names.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        ismrm_map[row[0]] = row[1]

# Process each bundle
for bundle in bundles:    
    for metric in list(metric_dic.keys()):  # Loop through metrics (only the first one in this case)
        print("For bundle: ", bundle, " and metric: ", metric)
        keys = []
        values = []
        # Remove methods that have None
        for method in methods:
            if metric_dic[metric][bundle][method] is None:
                del metric_dic[metric][bundle][method]
        
        # Sort methods based on metric values
        sorted_methods = sorted(metric_dic[metric][bundle].items(), key=lambda kv: float(kv[1]))
        
        # Store sorted method names and corresponding values
        for method in sorted_methods:
            keys.append(ismrm_map[str(method[0])])
            values.append(float(method[1]))
        print(keys, values)
