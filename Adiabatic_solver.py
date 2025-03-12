import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from symengine import *
from mimiqcircuits import *
from tqdm import tqdm
from scipy.optimize import minimize
from quantanium import *
import classic_qubo_solver
from collections import Counter
import time

sim = Quantanium()

#setting number of nodes
n=10
#setting seed
np.random.seed(1234)
#generate a random adjacency matrix
A = np.triu(np.random.randint(0, 2, (n, n)), 1)
adj_martix=A+A.T
print(adj_martix)
#create the graph object from the matrix
G = nx.Graph(adj_martix)
nx.draw(G, with_labels=True)

#defining cost function
def cost(X,A):
    c=np.sum(A,axis=0)
    return -X.T @ A @ X+c.T @ X

#Build the quantum circuit corresponding to adiabatic computation
def Build_QAOA(B, q, draw=False):
    beta=0
    gamma=0
    n=len(B) #Qubit number

    c=Circuit() #Circuit definition
    c.push(GateH(), range(0, n))
        
    for k in range(0,q):
        dgamma=0.02
        dbeta=0.02
        gamma=k*dgamma
        beta=k*dbeta
        #Block here
        for i in range(0,n) :
            for j in range(i+1,n):
                A_ij = B[i,j]
                if A_ij != 0:
                    c.push(GateRZZ(gamma*A_ij), i, j)    #The Upeer one is ALWAYS the control one

        #Block Here
        
        c.push(GateRX(beta), range(0,n))
        
    if draw:
        c.draw()

    return c

#running the circuit
def Run_QAOA(circuit):
   res = sim.execute(circuit,nsamples=30001)
   #res = connect.get_result(job_id)
   print(res)
   return res

#start the simulation
begin=time.time()
circuit=Build_QAOA(adj_martix, q=100, draw=False)
res=Run_QAOA(circuit)
counter = Counter(res.cstates)

most_common_state, frequency = counter.most_common(1)[0]
end=time.time()

#print all results
print("annealer time:", end-begin)
print(f"Most frequent state: {most_common_state}, with frequency: {frequency}")

costo = cost(np.array(most_common_state.tolist()),adj_martix)
print("Cost annealer: ", costo)

#use classical algorithms
begin=time.time()
res=classic_qubo_solver.first_method(C)
end=time.time()
print("metod 1 solution:", res)
print("method 1 solution time:", end-begin)
begin=time.time()
res=classic_qubo_solver.second_method(adj_matrix=adj_martix)
end=time.time()
print("metod 2 solution:", res)
print("metod 2 solution time:", end-begin)
