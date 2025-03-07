import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def xy_plotting(x, y, x_label, y_label, title):
    plt.plot(x, y, label=title, color='blue', marker='o', linestyle='-', linewidth=2)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()

def graph_draw(adj_matrix, cut):
    assert(adj_matrix.shape[0]==len(cut))
    G = nx.from_numpy_array(adj_matrix)
    node_colors = ['blue' if cut[i] == 1 else 'red' for i in range(len(cut))]
    link = []
    for i in range(0,len(cut)):
        #print("i:",i)
        for j in range(0,len(cut)):
            #print("j:",j)
            if cut[i] != cut[j] and adj_matrix[i,j] !=0:
                link.append((i,j))

    edge_colors = ['blue' if edge in link else 'lightgray' for edge in G.edges()]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=300, font_size=12, font_weight='bold',
            edge_color=edge_colors, node_color=node_colors)

    # Optional: Customize the plot appearance
    plt.title('Graph with Custom Node Colors', fontsize=16)
    plt.axis('off')  # Turn off the axis
    plt.show()
