import topologicalDistance as sn
from functools import partial
import networkx as nx
import numpy as np
import os
import pickle
import csv
import nibabel as nib
def compare_graphs(G1, G2):
    metrics = ["number_of_nodes", "number_of_edges", "average_degree", 
               "diameter"]
    
    differences = {}

    for metric in metrics:
        if metric == "number_of_nodes":
            val1, val2 = G1.number_of_nodes(), G2.number_of_nodes()
        elif metric == "number_of_edges":
            val1, val2 = G1.number_of_edges(), G2.number_of_edges()
        elif metric == "average_degree":
            val1, val2 = sum(dict(G1.degree()).values())/G1.number_of_nodes(), sum(dict(G2.degree()).values())/G2.number_of_nodes()
        elif metric == "diameter":
            if nx.is_connected(G1) and nx.is_connected(G2):
                val1, val2 = nx.diameter(G1), nx.diameter(G2)
            else:
                val1, val2 = None, None       
        
        differences[metric] = abs(val1 - val2) if val1 is not None and val2 is not None else None
    
    return differences

def annotate_graph(graph, node_positions, len_str):
    """
    Intakes a graph and a dictionary of node positions. The node positions are added to the graph as node attributes. Returns the graph.
    """
    for e in graph.edges:
        n1, n2 = e
        pos1, pos2 = np.array(node_positions[n1]), np.array(node_positions[n2])
        graph.nodes[n1]["position"] = pos1
        graph.nodes[n2]["position"] = pos2
        graph.edges[e]["weight"] = graph.edges[e]["weight"]*len_str
        graph.edges[e]["distance"] = np.linalg.norm(pos1 - pos2)
        
def merge_equivalent(graph, node_annotations):
    """
    Intakes a graph and its associated node annotations where some nodes may have the same annotation (spatial position). 
    Those equivalent nodes will be merged into the same node, and edges involving these equivalent nodes will be inherited 
    by the final node. Returns the graph with merged nodes.
    """
    
    equivalences = dict()
    
    for pos, node in node_annotations.items():
        if pos not in equivalences:
            equivalences[pos] = []
        
        equivalences[pos].append(node)
        
    for eq_group in equivalences.values():
        if len(eq_group) == 1: # nothing to merge
            continue
            
        head, tail = eq_group[0], eq_group[1:]
        for n in tail:
            nx.contracted_nodes(graph, head, n, copy=False)



def my_node_scoring_fn(node_score, edge_weight_score, edge_dist_score, gcmp, gref, eps, alpha, delta):
    """
    Intakes the node score, edge weight score, and edge distance score for a node in the comparison graph.
    Returns the final score for the node.
    """
    return node_score


#SCP_righ_VS
eps =5
alpha = 3
delta = 5
method_path = "/home/shailja/ismrmMethodOutput/"
methods = os.listdir(method_path)
csvfile = open(method_path+'retrace_rest.csv','w')
# bundles = ["CP","CA","SCP_right","SCP_left","ICP_right","Fornix","ICP_left","UF_left","UF_right","UF_left","UF_right","OR_left","OR_right","ILF_right","BPS_left","ILF_left", "SLF_right"]
# bundles_2 = ["UF_left","UF_right"]
bundles = ["SCP_left"]
for bundle in bundles:
    
    print(bundle, "node_distance", "number_of_nodes", "number_of_edges", "average_degree", 
               "diameter", "average_clustering")
    for method in methods:
        try:
            
            file = method_path+method+"/segmented_VB/"+str(bundle) + "_VSeps5thr2.5np50."

            with open(file+"gpickle", 'rb') as handle1:
                    H1 = pickle.load(handle1) 
            
            if len(H1.nodes()) >1:                    
                with open(file+"pickle", 'rb') as handle1:
                    node_loc_all = pickle.load(handle1)
                merge_equivalent(H1, node_loc_all)
                trkfile = "/home/shailja/ismrmMethodOutput/"+method+"/segmented_VB/"+bundle +"_VS.trk"
                bundle_streamlines =  nib.streamlines.load(trkfile)
                n1 = len(bundle_streamlines.streamlines)
                annotate_graph(H1, node_loc_all,len(bundle_streamlines.streamlines))
                node_list = H1.nodes()
                node_loc = {}
                for node_key in node_loc_all.keys():
                    if node_key in node_list:
                        node_loc[node_key] = node_loc_all[node_key]
                x_c1 = sum([list(node_loc.values())[idx][0] for idx in range(len(node_loc.values()))])/len(node_loc.values())
                y_c1 = sum([list(node_loc.values())[idx][1] for idx in range(len(node_loc.values()))])/len(node_loc.values())
                z_c1 = sum([list(node_loc.values())[idx][2] for idx in range(len(node_loc.values()))])/len(node_loc.values())

                with open("/media/hdd2/shailja/ismrm_tractogram_comparison/gt_bundles/"+str(bundle)+"eps5thr2.5np50"+".gpickle", 'rb') as handle1:
                    H2 = pickle.load(handle1)                     
                with open("/media/hdd2/shailja/ismrm_tractogram_comparison/gt_bundles/"+str(bundle)+"eps5thr2.5np50"+".pickle", 'rb') as handle1:
                    node_loc_all = pickle.load(handle1)
                merge_equivalent(H2, node_loc_all)
                trkfile = "/media/hdd2/shailja/ismrm_tractogram_comparison/gt_bundles/"+str(bundle) +".trk"
                bundle_streamlines =  nib.streamlines.load(trkfile)
                n2 = len(bundle_streamlines.streamlines)
                annotate_graph(H2, node_loc_all, len(bundle_streamlines.streamlines))
                node_list = H2.nodes()
            #                         print(node_list, node_loc_all.keys())
                node_loc = {}
                for node_key in node_loc_all.keys():
                    if node_key in node_list:
                        node_loc[node_key] = node_loc_all[node_key]
                x_c2 = sum([list(node_loc.values())[idx][0] for idx in range(len(node_loc.values()))])/len(node_loc.values())
                y_c2 = sum([list(node_loc.values())[idx][1] for idx in range(len(node_loc.values()))])/len(node_loc.values())
                z_c2 = sum([list(node_loc.values())[idx][2] for idx in range(len(node_loc.values()))])/len(node_loc.values())

                sub_r = np.linalg.norm(np.array([x_c1,y_c1,z_c1]) - np.array([x_c2,y_c2,z_c2]))
          
                dist_node = partial(sn.distance, eps=eps, alpha=alpha, delta=delta, scoring_func=my_node_scoring_fn,ins_cost = 2*eps*(1+sub_r/30))
                #dist = partial(sn.distance, eps=eps, alpha=alpha, delta=delta, scoring_func=sn.max_cost_score)
                dist_node = 0.5*(dist_node(H1, H2)+dist_node(H2, H1))
                dist_nm = compare_graphs(H1, H2)
                print(dist_nm["number_of_nodes"], dist_nm["number_of_edges"], dist_nm["average_degree"],dist_nm["diameter"])
                print(bundle,method,round(dist_node,1),len(H1.nodes()),len(H2.nodes()),len(H1.edges()),len(H2.edges()))
                csvfile.write(method+","+bundle+","+ str(round(dist_node,1))+","+str(round(dist_nm["number_of_nodes"],1))+","+str(round(dist_nm["number_of_edges"],1))+"\n")
        #just for file not found error        
        except:
            # print("File not found for",bundle,method)
            pass



