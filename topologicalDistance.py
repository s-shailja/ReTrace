#!/bin/python3

# Implementation of Siminet algorithm in Python

import networkx as nx
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from functools import wraps
import networkx as nx

def compute_node_features(G):
    # Calculate degree centrality for each node
    degree_centrality = nx.degree_centrality(G)
    
    # Calculate closeness centrality for each node
    closeness_centrality = nx.closeness_centrality(G)
    
    # Calculate betweenness centrality for each node
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Calculate eigenvector centrality for each node
    eigenvector_centrality = nx.eigenvector_centrality(G)
    
    # Calculate clustering coefficient for each node
    clustering_coefficient = nx.clustering(G)
    
    # Create a dictionary to hold features for each node
    features = {}

    for node in G.nodes:
        features[node] = [degree_centrality[node],
            closeness_centrality[node],
             betweenness_centrality[node],
             eigenvector_centrality[node],
             clustering_coefficient[node]
        ]

    return features

def annotate_graph(graph, node_positions):
    for e in graph.edges:
        n1, n2 = e
        pos1, pos2 = np.array(node_positions[n1]), np.array(node_positions[n2])
        graph.nodes[n1]["position"] = pos1
        graph.nodes[n2]["position"] = pos2
        graph.edges[e]["distance"] = np.linalg.norm(pos1 - pos2)
        
def merge_equivalent(graph, node_annotations):
    """
    Intakes a graph and its associated node annotations where some nodes may have the same annotation (spatial position). 
    Those equivalent nodes will be merged into the same node, and edges involving these equivalent nodes will be inherited 
    by the final node.
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

def annotate_merge(fn):
    @wraps(fn)
    def wrapped(gcmp, gcmp_pos, gref, gref_pos, *args, **kwargs):
        merge_equivalent(gcmp, gcmp_pos)
        annotate_graph(gcmp, gcmp_pos)
        
        merge_equivalent(gref, gref_pos)
        annotate_graph(gref, gref_pos)
        
        return distance(gcmp, gref, *args, **kwargs)
    return wrapped
            

def max_cost_score(node_score, edge_weight_score, edge_dist_score, gcmp, gref, eps, alpha, delta):
    """
    Scoring function that normalizes the sum of the node score and edge score with
    the maximum possible such score  -- which is the sum of maximum insertion cost and maximum deletion cost
    for both nodes and edges.
    """
    #print(max_cost_score.__name__)
    sub_rad = 2*eps
    # Maximum node costs
    max_node_ins_cost = sub_rad*len(gref.nodes)
    max_node_del_cost = sub_rad*len(gcmp.nodes)

    # Maximum edge costs
    max_edge_ins_cost = sum(attrs["weight"] for (_,_,attrs) in gref.edges(data=True))
    max_edge_del_cost = sum(attrs["weight"] for (_,_,attrs) in gcmp.edges(data=True))
    #max_edge_ins_cost = 2*(alpha+delta)*len(gref.edges)
    #max_edge_del_cost = 2*(alpha+delta)*len(gcmp.edges)


    max_score   = max_node_ins_cost + max_node_del_cost + max_edge_ins_cost + max_edge_del_cost
    given_score = node_score + edge_dist_score + edge_weight_score

    #print(f"{max_score=}")
    return given_score / max_score

#@annotate_merge
def distance(gcmp, gref, eps, alpha, delta, sub_rad=None , scoring_func=None, transform=False, ins_cost = None):
    """
    Intakes two graphs, gcmp and gref, and computes the node and edge distances b/w them as per the Siminet algorithm.
    The graph is expected to be labeled, with the nodes having an attribute 'position' (corresponds to spatial position)
    and the edges having an attribute 'weight'. The computed node and edge distances, as well as the two graphs,
    will be given to a scoring function, which will (usually) yield some scalar -- this will be returned as the final result. 
    
    The scoring function is a function which intakes the node score, the edge score, the comparision graph (gcmp) 
    and the reference graph (gref). If scoring_func is set to None, then the returned value is a tuple of the node score and edge score.
    
    The transform boolean flag will transform a copy of gcmp during the course of the function if set to true 
    (for testing purposes).
    """
    feature_ref = compute_node_features(gref)
    feature_cmp = compute_node_features(gcmp)
    # print("feature_ref",feature_ref)
    network_score = 0
    #computed euclidean distance between features


    if scoring_func is None: # scoring function, using the node/edge scores and the two graphs
        scoring_func = lambda n,ew, ed, gc, gr, eps, alpha, delta: (n,ew, ed) # default just returns back the node and edge scores

    if sub_rad is None:
        sub_rad = 2*eps
        #sub_rad = 5*eps
    
    assert eps < sub_rad
        
    copy = nx.empty_graph()
    
    if transform: 
        copy = deepcopy(gcmp) # ensures that we don't mutate what was passed in
    
    dist = lambda p,q: np.linalg.norm(p[1]["position"] - q[1]["position"]) # compute the Euclidean distance b/w nodes

    equivalency_mapping = dict() # maps nodes in Gref to nodes in Gcmp, representing equality b/w them
    counterpart_nodes   = set() # set of all nodes in Gref with counterparts in Gcmp (through substitution or equality)
    
    node_score = 0
    if ins_cost is None:
        ins_cost = sub_rad
    
    freq_table = {'equivalency'  : 0,
                  'substitution' : 0,
                  'deletion'     : 0,
                 }
    
    avg_del_dist = 0
    distances = []
    
    valid_cand = lambda nde: nde[0] not in counterpart_nodes # condition to ensure that candidate node is new, hasn't been seen before

    # NODE SCORE
    
    gcmp_attrs_sorted = sorted(gcmp.nodes(data=True), key=lambda n: n[0])
    gref_attrs_sorted = sorted(gref.nodes(data=True), key=lambda n: n[0])
        
    for n in gcmp_attrs_sorted:
        
        #valid_cand = lambda nde: nde[0] not in counterpart_nodes # condition to ensure that candidate node is new, hasn't been seen before
        closest = min(filter(valid_cand, gref_attrs_sorted), 
                      key     = lambda m: dist(m, n),
                      default = (None, {"position": np.array([np.inf,np.inf,np.inf])})) 
        # if gref is empty, default value returned is node at infinity
       
        d = dist(n, closest)
        #node_network_score is the euclidean distances between all node features of the node in the graph
        # print(feature_cmp[n[0]])
        d_nm = np.linalg.norm(np.array(feature_cmp[n[0]]) - np.array(feature_ref[closest[0]]))


        #if d != np.inf:
        #    distances.append(d)

        if d <= eps: # Equivalency
            #print("Equivalency")
            freq_table['equivalency'] += 1
            equivalency_mapping[closest[0]] = n[0]
            counterpart_nodes.add(closest[0])
            
            if transform:
                copy.nodes[n[0]]["position"] = closest[1]["position"]
        
        elif d <= sub_rad: # Substitution
            #print(f"Substitution, {d}")
            freq_table['substitution'] += 1
            #equivalency_mapping[closest[0]] = n[0]
            # equivalency_mapping[n] = closest
            counterpart_nodes.add(closest[0])
            node_score += d
            network_score += d_nm
            if transform:
                copy.nodes[n[0]]["position"] = closest[1]["position"]
        
        else: # Deletion
            #print("Deletion")
            freq_table['deletion'] += 1
            avg_del_dist += d
            node_score += ins_cost
            d_mean = np.mean(np.array(feature_cmp[n[0]]))
            network_score += d_mean
            if transform:
                copy.remove_node(n[0])
        #print(f"\t{d=}, {eps=}, {sub_rad=}")

    not_found   = gref.nodes - counterpart_nodes # nodes in Gref that had no counterpart (equivalency or substitution) in Gcmp
    #print(f"Insertion: {len(not_found)}")
    freq_table['insertion'] = len(not_found)
    node_score += ins_cost * len(not_found) # total insertion cost for nodes not found
    for nf in not_found:
        network_score += np.mean(np.array(feature_ref[nf]))

    if transform: # Node Insertion, if we are transforming the copy of Gcmp
        for n in not_found:
            copy.add_node(n, **gref.nodes[n])
    edge_weight_score = None
    edge_dist_score = network_score
    node_score = node_score/len(gref.nodes())+ network_score

    
    final_score = scoring_func(node_score, edge_weight_score, edge_dist_score, gcmp, gref, eps, alpha, delta)

    return final_score