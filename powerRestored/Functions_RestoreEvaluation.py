"""
This file contains the functions to evaluate the circuit with line failures and further restoration
"""
import os
from DSS_CircuitSetup import*


### For now if we donot consider the task 1 has changed the network, then the grid forming capability doesnot matter
#-- Define the network with additions of DER, BESS and switches 


#-- Function to evaluate the energy served
def Peval(DSSCktobj):
    Ptot_served = 0    
    load_dict = []
    i= DSSCktobj.dss.Loads.First()
    while i>0:
          elemName = f'Load.{DSSCktobj.dss.Loads.Name()}'
          DSSCktobj.dss.Circuit.SetActiveElement(elemName)
          bus_connectn = DSSCktobj.dss.CktElement.BusNames()[0].split('.')[0]
          S = np.array(DSSCktobj.dss.CktElement.Powers())
          ctidx = 2 * np.array(range(0, min(int(S.size/ 2), 3)))
          P = S[ctidx] #active power in KW #get the active power array of the load
          #Q =S[ctidx + 1] #angle in KVAr
          Power_supplied = sum(P) #get the total active power served for the load
          loadname = DSSCktobj.dss.Loads.Name()
          Power_demand = DSSCktobj.dss.Loads.kW()
          load_dict.append({'Load Name': loadname, 'Bus': bus_connectn, 'Power Supply': Power_supplied, 'Power Demand': Power_demand})
          Ptot_served = Ptot_served + Power_supplied # total load
    
          i = DSSCktobj.dss.Loads.Next()
    return  Ptot_served 

def GraphRestore_Eval(G, substation_id):
    Components = list(nx.connected_components(G)) #connected components in the graph
    restored_component = [node_c  for C in Components if substation_id in C for node_c in C]
    Power_restored = 0
    for n in restored_component:
        Power_restored += G.nodes[n]['active power']
    return restored_component, Power_restored

