import numpy as np
import time

def first_method(adj_matrix):

    # Function to calculate the cut value between two sets
    def calculate_cut_value(graph, set1, set2):
        cut_value = 0
        for i in set1:
            for j in set2:
                cut_value += graph[i, j]
        return cut_value

    # Function to perform the local search algorithm
    def local_search_max_cut(graph):
        num_nodes = len(graph)
        
        # Step 1: Start with a random partition of the vertices into two sets
        set1 = set(np.random.choice(num_nodes, num_nodes // 2, replace=False))
        set2 = set(range(num_nodes)) - set1
        
        # Step 2: Evaluate the initial cut value
        best_cut_value = calculate_cut_value(graph, set1, set2)
        best_set1, best_set2 = set1.copy(), set2.copy()

        # Step 3: Local search: try moving vertices between sets to improve the cut
        for iteration in range(1000):  # Max iterations to avoid infinite loops
            improved = False
            
            # Try moving vertices from set1 to set2
            for node in list(set1):
                new_set1 = set1.copy()
                new_set2 = set2.copy()
                new_set1.remove(node)
                new_set2.add(node)
                new_cut_value = calculate_cut_value(graph, new_set1, new_set2)

                # If the cut improves, accept the move
                if new_cut_value > best_cut_value:
                    set1, set2 = new_set1, new_set2
                    best_cut_value = new_cut_value
                    best_set1, best_set2 = set1.copy(), set2.copy()
                    improved = True
                    break
            
            # Try moving vertices from set2 to set1
            if not improved:  # Only try moving from set2 if no improvement was found yet
                for node in list(set2):
                    new_set1 = set1.copy()
                    new_set2 = set2.copy()
                    new_set2.remove(node)
                    new_set1.add(node)
                    new_cut_value = calculate_cut_value(graph, new_set1, new_set2)

                    # If the cut improves, accept the move
                    if new_cut_value > best_cut_value:
                        set1, set2 = new_set1, new_set2
                        best_cut_value = new_cut_value
                        best_set1, best_set2 = set1.copy(), set2.copy()
                        improved = True
                        break
            
            # If no improvement was made, terminate the search
            if not improved:
                break

        return best_set1, best_set2, best_cut_value


    start_time=time.time()
    best_cut=0
    best_group1=0
    best_group2=0
    for i in range(0, 100):
        set1, set2, cut_value = local_search_max_cut(adj_matrix)
        print(cut_value)
        if cut_value>best_cut:
            best_cut=cut_value
            print("best", best_cut)
            best_group1=set1
            best_group2=set2

    end_time=time.time()
    print("Set 1:", best_group1)
    print("Set 2:", best_group2)
    print("First method Max Cut Value:", best_cut)
    print("First Method Time: ", end_time-start_time)
################################################

####SECONDO METODO

def second_method(adj_matrix):
    # Function to calculate the cut value between two sets
    def calculate_cut_value(graph, set1, set2):
        cut_value = 0
        for i in set1:
            for j in set2:
                cut_value += graph[i, j]
        return cut_value

    # Function to perform the Kernighan-Lin algorithm for Max Cut
    def kernighan_lin_max_cut(graph):
        num_nodes = len(graph)
        
        # Step 1: Start with a random partition of the vertices into two sets
        set1 = set(np.random.choice(num_nodes, num_nodes // 2, replace=False))
        set2 = set(range(num_nodes)) - set1
        
        # Step 2: Initialize variables for storing the best cut value and sets
        best_cut_value = calculate_cut_value(graph, set1, set2)
        best_set1, best_set2 = set1.copy(), set2.copy()

        # Step 3: Kernighan-Lin algorithm - Refinement process
        for iteration in range(100):  # Max iterations to avoid infinite loops
            improvement = False
            # Consider all possible swaps
            candidates = []
            for i in list(set1):
                for j in list(set2):
                    # Swap i from set1 with j from set2
                    new_set1 = set1.copy()
                    new_set2 = set2.copy()
                    new_set1.remove(i)
                    new_set2.add(i)
                    new_set2.remove(j)
                    new_set1.add(j)
                    
                    # Calculate the new cut value
                    new_cut_value = calculate_cut_value(graph, new_set1, new_set2)
                    candidates.append((new_cut_value, new_set1, new_set2, i, j))
            
            # Sort candidates by the best cut value
            candidates.sort(reverse=True, key=lambda x: x[0])

            # Apply the best swap (i, j) if the cut improves
            if candidates:
                best_candidate = candidates[0]
                new_cut_value, new_set1, new_set2, i, j = best_candidate
                if new_cut_value > best_cut_value:
                    set1, set2 = new_set1, new_set2
                    best_cut_value = new_cut_value
                    best_set1, best_set2 = new_set1, new_set2
                    improvement = True

            # If no improvement, break out of the loop
            if not improvement:
                break

        return best_set1, best_set2, best_cut_value

    # Example: Create a sample adjacency matrix for testing

    time2=time.time()
    set1, set2, cut_value = kernighan_lin_max_cut(adj_matrix)
    time2stop=time.time()
    print("Set 1:", set1)
    print("Set 2:", set2)
    print("Second Method Max Cut Value :", cut_value)
    print("Second method time:", time2stop-time2)
