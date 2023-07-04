# Import required libraries
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import csv

# Load ISMRM mapping names from csv file and store it in dictionary
ismrm_map = {}
with open('/home/shailja/ismrmMethodOutput/ismrm_method_mapping_names.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        ismrm_map[row[0]] = row[1]

# Define file paths
path = "/home/shailja/ismrmMethodOutput/"
csvfile = path+'results.csv'

# Initialize variables
metric_dic = {}  # Dictionary to store metrics
methods = []  # List to store methods
bundles = []  # List to store bundles
metric = []  # List to store metrics
file_rows = []  # List to store file rows

# Load csv file and store the rows in 'file_rows' list
with open(csvfile, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        file_rows.append(row)

# Extract data from each row
for row in file_rows:
    methods.append(row[0])
    bundles.append(row[1])
    metric.append(row[2])

# Remove duplicates from methods, bundles and metric lists
methods = list(set(methods))
bundles = list(set(bundles))
metric = list(set(metric))

# Initialize metric_dic with None for each combination of method, bundle and metric
for m in metric:
    metric_dic[m] = {}
    for b in bundles:
        metric_dic[m][b] = {}
        for method in methods:
            metric_dic[m][b][method] = None

# Update metric_dic with data from each row
for row in file_rows:
    metric_dic[row[2]][row[1]][row[0]] = row[3]

print(sorted(metric_dic.keys()))

# For each bundle, process the metrics
for bundle in bundles:
    print("For bundle ", bundle)
    row_list = []  # List to store row data in the format (algorithm, metric_value)
    algorithm_list = [bundle]  # List to store algorithms for each bundle    
    try:
        # Process each metric
        for metric in sorted(metric_dic.keys()):            
            # Reverse the metric if 'F' or 'OR' in metric
            reverse_metric = "F" in metric or "OR" in metric
            for method in methods:
                if metric_dic[metric][bundle][method] is None:
                    del metric_dic[metric][bundle][method]

            # Sort methods based on metric values
            sorted_methods = sorted(metric_dic[metric][bundle].items(), key=lambda kv: float(kv[1]))

            # Select the method based on the metric
            if reverse_metric:
                selected_method = sorted_methods[0]
            else:
                selected_method = sorted_methods[-1]

            # Update the row list and algorithm list with the selected method
            row_list.append(f"({ismrm_map[selected_method[0]]}, {round(float(selected_method[1]), 2)})")
            algorithm_list.append(ismrm_map[selected_method[0]])
    except Exception as e:
        print(f"Error: {e}")
        pass
    print(row_list)
