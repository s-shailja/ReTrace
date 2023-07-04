#parameters
#eps: for connect disconnect
#tau: for interruption
import numpy as np
import pdb

class Event:
    def __init__(self, event, trajectory = None, t = None):
        self.event = event
        self.trajectory = trajectory
        self.t = t


def checkEpsilonDistance(p1, p2, eps):
	return (np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)) <= eps

def findConnectDisconnectEvents(t1_id, t2_id, t1, t2, eps,alpha):
	dic_t1 = {}
	dic_t2 = {}
	ti = 0
	flag_t1 = [False]*len(t1)
	flag_t2 = [False]*len(t2)
	while ti < (len(t1)):
		tj = 0 
		while tj < (len(t2)):
			if not flag_t1[ti] and not flag_t2[tj] and checkEpsilonDistance(t1[ti], t2[tj], eps):
				# print(ti,"Start",tj)
				flag_t1[ti] = True
				flag_t2[tj] = True
				flag_insert = True
				first_i = ti
				last_i = ti
				first_j = tj
				last_j = tj
				while(flag_insert and last_j<len(t2) and first_j>=0):
					# print("flag_t1",flag_t1)
					# print("flag_t2", flag_t2)
					# print("(" ,first_i, " " , last_i , ") (" , first_j ,  " " , last_j ,")")
					flag_insert = False
					#case first_i - 1 insert:
					if (first_i - 1 >=0) and not flag_t1[first_i - 1 ]:
						if first_j - 1 >= 0 and not flag_t2[first_j - 1] and checkEpsilonDistance(t1[first_i - 1], t2[first_j - 1], eps):
							first_i = first_i - 1
							first_j = first_j - 1
							flag_t1[first_i ] = True
							flag_t2[first_j ] = True
							flag_insert = True
						elif last_j + 1 < len(t2) and not flag_t2[last_j + 1] and checkEpsilonDistance(t1[first_i - 1], t2[last_j + 1], eps):
							first_i = first_i - 1
							last_j = last_j + 1
							flag_t1[first_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						elif first_j + 1 < len(t2) and not flag_t2[first_j + 1] and checkEpsilonDistance(t1[first_i - 1], t2[first_j + 1], eps):
							first_i = first_i - 1
							first_j = first_j + 1
							flag_t1[first_i ] = True
							flag_t2[first_j ] = True
							flag_insert = True
						elif last_j - 1 >= 0 and not flag_t2[last_j - 1] and checkEpsilonDistance(t1[first_i - 1], t2[last_j - 1], eps):
							first_i = first_i - 1
							last_j = last_j - 1
							flag_t1[first_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						else:
							for each_j in range(first_j, last_j + 1):
								if checkEpsilonDistance(t1[first_i - 1], t2[each_j], eps):
									first_i = first_i - 1
									flag_t1[first_i ] = True
									flag_t2[each_j] = True
									flag_insert = True
									break


									
					#case last_i + 1 insert:
					if (last_i + 1 < len(t1)) and not flag_t1[last_i + 1]:
						if first_j - 1 > 0 and  not flag_t2[first_j - 1] and checkEpsilonDistance(t1[last_i + 1], t2[first_j - 1], eps):
							last_i = last_i + 1
							first_j = first_j - 1
							flag_t1[last_i ] = True
							flag_t2[first_j ] = True 
							flag_insert = True
						elif last_j + 1 < len(t2) and not flag_t2[last_j + 1] and checkEpsilonDistance(t1[last_i + 1], t2[last_j + 1], eps):
							last_i = last_i + 1
							last_j = last_j + 1
							flag_t1[last_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						elif first_j + 1 < len(t2) and not flag_t2[first_j + 1] and checkEpsilonDistance(t1[last_i + 1], t2[first_j + 1], eps):
							last_i = last_i + 1
							first_j = first_j + 1
							flag_t1[last_i ] = True
							flag_t2[first_j] = True
							flag_insert = True
						elif last_j - 1 > 0 and not flag_t2[last_j -1] and checkEpsilonDistance(t1[last_i + 1], t2[last_j - 1], eps):
							last_i = last_i + 1
							last_j = last_j - 1
							flag_t1[last_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						else:
							for each_j in range(first_j, last_j + 1):
								if checkEpsilonDistance(t1[last_i + 1], t2[each_j], eps):
									last_i = last_i + 1
									flag_t1[last_i ] = True
									flag_t2[each_j] = True
									flag_insert = True
									break
						


									
					#case first_j - 1 insert:
					if (first_j - 1 >= 0 ) and not flag_t2[first_j - 1]:
						if first_i - 1 >= 0 and not flag_t1[first_i - 1 ] and checkEpsilonDistance(t2[first_j - 1], t1[first_i - 1], eps):
							first_j = first_j - 1
							first_i = first_i - 1
							flag_t1[first_i ] = True
							flag_t2[first_j] = True
							flag_insert = True
						elif last_i + 1 < len(t1) and not flag_t1[last_i + 1] and checkEpsilonDistance(t2[first_j - 1], t1[last_i + 1], eps):
							first_j = first_j - 1
							last_i = last_i + 1
							flag_t1[last_i ] = True
							flag_t2[first_j ] = True
							flag_insert = True
						elif first_i + 1 < len(t1) and not flag_t1[first_i + 1] and checkEpsilonDistance(t2[first_j - 1], t1[first_i + 1], eps):
							first_j = first_j - 1
							first_i = first_i + 1
							flag_t2[first_j ] = True
							flag_t1[first_i ] = True
							flag_insert = True
						elif last_i - 1 >= 0 and not flag_t1[last_i - 1] and checkEpsilonDistance(t2[first_j - 1], t1[last_i - 1], eps):
							first_j = first_j - 1
							last_i = last_i - 1
							flag_t1[last_i ] = True
							flag_t2[first_j] = True
							flag_insert = True

						else:
							for each_i in range(first_i, last_i + 1):
								if checkEpsilonDistance(t2[first_j - 1], t1[each_i], eps):
									first_j = first_j - 1
									flag_t2[first_j] = True
									flag_t1[each_i] = True
									flag_insert = True
									break
						
									

					#case last_j + 1 insert:
					if (last_j + 1 < len(t2)) and not flag_t2[last_j + 1]:
						if  first_i - 1 >= 0 and not flag_t1[first_i - 1] and checkEpsilonDistance(t2[last_j + 1], t1[first_i - 1], eps):
							last_j = last_j + 1
							first_i = first_i - 1
							flag_t1[first_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						elif last_i + 1 < len(t1) and not flag_t1[last_i + 1] and checkEpsilonDistance(t2[last_j + 1], t1[last_i + 1], eps):
							last_j = last_j + 1
							last_i = last_i + 1
							flag_t1[last_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						elif  first_i + 1 <len(t1) and not flag_t1[first_i + 1] and checkEpsilonDistance(t2[last_j + 1], t1[first_i + 1], eps):
							last_j = last_j + 1
							first_i = first_i + 1
							flag_t1[first_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						elif last_i - 1 >= 0 and not flag_t1[last_i - 1] and checkEpsilonDistance(t2[last_j + 1], t1[last_i - 1], eps):
							last_j = last_j + 1
							last_i = last_i - 1
							flag_t1[last_i ] = True
							flag_t2[last_j ] = True
							flag_insert = True
						else:
							for each_i in range(first_i, last_i + 1):
								if checkEpsilonDistance(t2[last_j + 1], t1[each_i], eps):
									last_j = last_j + 1
									flag_t2[last_j] = True
									flag_t1[each_i] = True									
									flag_insert = True
									break
# 				print("Connected segment t1 and t2 at (" ,first_i, " " , last_i , ") (" , first_j ,  " " , last_j ,")", t1_id, t2_id)						
				# print("Connected segment t1 and t2 at (" first_i " " last_i ") (" first_j  " " last_j ")", ti, tj)
				#connect event
				if dic_t1.get(first_i):
					dic_t1 [first_i].append(Event("connect", t2_id, first_j))
				else:
					dic_t1 [first_i] = [Event("connect", t2_id, first_j)]

				if dic_t2.get(first_j):
					dic_t2 [first_j].append(Event("connect", t1_id, first_i))
				else:
					dic_t2 [first_j] = [Event("connect", t1_id, first_i)]
				#disconnect event
				if last_i + 1 < len(t1): #beacuse it gets disconnected later
					if dic_t1.get(last_i + 1):
						dic_t1 [last_i + 1].append(Event("disconnect", t2_id, last_j + 1))
					else:
						dic_t1 [last_i + 1] = [Event("disconnect", t2_id, last_j + 1)]
				if  last_j + 1 < len(t2):
					if dic_t2.get(last_j + 1):
						dic_t2 [last_j + 1].append(Event("disconnect", t1_id, last_i + 1))
					else:
						dic_t2 [last_j + 1] = [Event("disconnect", t1_id, last_i + 1)]

					




				ti = last_i				
				break
			else:
				tj += 1		
		ti += 1
    #code to take care of alpha parameter
	keys_to_remove1 = []
	keys_to_remove2 = []
	event_pos1 = [t1[key] for key in dic_t1.keys()]
	event_pos2 = [t2[key] for key in dic_t2.keys()]
	for i in range(len(event_pos1)): #check epsilon distance from consecutive points, if less than alpha then remove
		if i + 1 < len(event_pos1) and checkEpsilonDistance(event_pos1[i], event_pos1[i + 1], alpha):
			keys_to_remove1.append(list(dic_t1.keys())[i])
			keys_to_remove1.append(list(dic_t1.keys())[i + 1])
	for i in range(len(event_pos2)):
		if i + 1 < len(event_pos2) and checkEpsilonDistance(event_pos2[i], event_pos2[i + 1], alpha):
			keys_to_remove2.append(list(dic_t2.keys())[i])
			keys_to_remove2.append(list(dic_t2.keys())[i + 1])
    #  remove all the keys in dic_t1 and dic_t2 which are in keys_to_remove1 and keys_to_remove2 respectively
	for key in list(set(keys_to_remove1)):
		del dic_t1[key]
	for key in list(set(keys_to_remove2)):
		del dic_t2[key]
	return dic_t1, dic_t2
	# for a given two trajectories if connect disconnect distance is less than alpha then delete both the events
		
	# if any of the above takes place repeat
	#nothing happened then terminate







