import numpy as np
import qubovert as qv
import time

#Q = np.array([[0, 1,1,0], [0,0,1,0], [1,0,0,0], [0,0,0,0]])
#A = np.triu(np.random.randint(0, 2, (20, 20)), 1)
#Q=A+A.T
# Convert NumPy matrix to QUBO dictionary format (upper triangle only)
def classic_solver(Q):
  Q_dict = {(i, j): Q[i, j] for i in range(Q.shape[0]) for j in range(i, Q.shape[1]) if Q[i, j] != 0}
  # Solve the QUBO problem using qubovert
  start_time = time.time()
  solution = qv.sim.anneal_qubo(Q_dict)  # Simulated annealing solver
  end_time = time.time()
  

  # Step 4: Print results
  print("QUBO Matrix:\n", Q)
  #print("QUBO Dictionary:", Q_dict)
  print("Best Solution:", solution)
  print("Execution Time:", end_time - start_time, "seconds")
  return solution
