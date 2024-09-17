#!/usr/bin/env python3
import sys
import numpy as np
 
 
def parse_input(input_file):
    with open(input_file, 'r') as file:
        line1 = file.readline()
        num_customers, num_products = map(int, line1.split())
        customers_lim = []
        customer_prod = []
        for i in range(1, num_customers + 1):
            line = file.readline()
            myline =  line.split()
            customers_lim.append([int(myline[0]), int(myline[1])])
            prod = []
            for j in range(2, len(myline)):
                prod.append(int(myline[j]))
            customer_prod.append(prod)
 
        line = file.readline().split()
        product_reviews = [int(line[i]) for i in range(num_products)]
 
    return num_customers, num_products, customers_lim, customer_prod, product_reviews
 
 
def e_is_forward_arc(e, G):
    return e[0] in G and e[1] in G[e[0]]
 
 
def initialize_flow(G, l):
    f = {(u, v): l[(u, v)] for u, v in G}
    for u, v in G:
        if (v, u) not in G:
            G[v] = []
        if (v, u) not in f:
            f[(v, u)] = 0
    return f
 
 
def find_path(adj, s, t):
    visited = [False]*(len(adj))
    par = [None]*(len(adj))
    q = []
    q.append(s)
    visited[s] = True
    while len(q) != 0:
        curr = q.pop(0)
        for i in range(len(adj)):
            if visited[i] is False and adj[curr][i][1]> -1 and adj[curr][i][2] > adj[curr][i][1]:
                par[i] = curr
                visited[i] = True
                if i == t:
                    break
                q.append(i)
        for j in range(len(adj)):
            if visited[j] is False and adj[j][curr][0] > -1 and adj[j][curr][1] > adj[j][curr][0]:
                par[j] = curr
                visited[j] = True
                if j == t:
                    break
                q.append(j)
    if not visited[t]:
        return False
    else:
        path = []
        curr = t
        while True:
            path.append(curr)
            if curr == s:
                break
            curr = par[curr]
        path.reverse()
        return path
 
 
def ford_fulkerson(adj, s, t):
    while True:
        path_found = find_path(adj, s, t)
        if not path_found:
            break
        minflow = np.inf
        for i in range(len(path_found)-1):
            if adj[path_found[i]][path_found[i+1]][0] > -1:
                if adj[path_found[i]][path_found[i+1]][2] - adj[path_found[i]][path_found[i+1]][1] < minflow:
                    minflow = adj[path_found[i]][path_found[i+1]][2] - adj[path_found[i]][path_found[i+1]][1]
            else:
                if adj[path_found[i+1]][path_found[i]][1] - adj[path_found[i+1]][path_found[i]][0] < minflow:
                    minflow = adj[path_found[i+1]][path_found[i]][1] - adj[path_found[i+1]][path_found[i]][0]
        for i in range(len(path_found) - 1):
            if adj[path_found[i]][path_found[i+1]][0] > -1:
                adj[path_found[i]][path_found[i + 1]][1] = adj[path_found[i]][path_found[i+1]][1] + minflow
            else:
                adj[path_found[i+1]][path_found[i]][1] = adj[path_found[i+1]][path_found[i]][1] - minflow
 
    return adj
 
 
def write_output(output_file, assignments, customers):
    with open(output_file, 'w') as file:
        if assignments is None:
            file.write("-1\n")
            return
        line = []
        for i in range(customers):
            for j in range(len(assignments[i+1])):
                if assignments[i+1][j][1]>0:
                    line.append(j-customers)
            for k in range(len(line)):
                file.write(str(int(line[k])) + " ")
            file.write("\n")
            line.clear()
    return
 
 
def solve_survey_design(input_file, output_file):
    num_customers, num_products, customers_lim, customers_prod, product_reviews = parse_input(input_file)
    mysize = num_customers + num_products +2
    max = 0
    # Construct the graph
    G = {i: [] for i in range(mysize)}  # +2 for source and sink
    l = {}
    adj = np.ones((mysize, mysize, 3))
    bal = np.zeros(mysize)
    adj = adj * -1
    # Add edges from source to customers
    for i in range(0, num_customers):
        bal[0] = bal[0]-customers_lim[i][0]
        bal[i+1] = bal[i+1]+customers_lim[i][0]
        adj[0][i+1] = [customers_lim[i][0], 0, customers_lim[i][1]]
        max = max + customers_lim[i][1]
        for j in range(len(customers_prod[i])):
            adj[i+1][num_customers+customers_prod[i][j]] = [0, 0, 1]
 
    # Add edges from products to sink
    for j in range(num_customers+1, mysize-1):
        G[j].append(num_customers + num_products + 1)
        G[num_customers + num_products + 1] = [j]
        l[(j, num_customers + num_products + 1)] = 0
        myindex = j-num_customers-1
        adj[j][mysize-1] = [product_reviews[myindex], 0, max]
        bal[mysize-1] = bal[mysize-1] + product_reviews[myindex]
        bal[j] = bal[j] - product_reviews[myindex]
 
 
    exp_adj = np.full((mysize+2, mysize+2, 3), -1, dtype=float)
    exp_adj[:adj.shape[0], :adj.shape[1], :adj.shape[2]] = adj
    exp_adj[mysize-1][0] = [0, 0, np.inf]
 
    # Initialize flow
    #f = initialize_flow(G, l, u, num_customers + num_products, num_customers + num_products + 1)
    # Solve using Ford-Fulkerson algorithm
    #f = ford_fulkerson(G, l, u, f, num_customers + num_products, num_customers + num_products + 1)
    for i in range(mysize):
        if bal[i] < 0:
            exp_adj[i][mysize+1] = [0, 0, -1*bal[i]]
        if bal[i] > 0:
            exp_adj[mysize][i] = [0, 0, bal[i]]
        for j in range(mysize):
            if exp_adj[i][j][0] > -1:
                exp_adj[i][j][2] = exp_adj[i][j][2] - exp_adj[i][j][0]
                exp_adj[i][j][0] = 0
 
    newadj = ford_fulkerson(exp_adj, mysize, mysize+1)
    print(newadj)
    result = True
    for i in range(len(newadj[mysize])):
        if newadj[mysize][i][1] != newadj[mysize][i][2]:
            result = False
            break
    out = None
 
    if not result:
        write_output(output_file, out, num_customers)
    else:
        for i in range(len(adj)):
            for j in range(len(adj[i])):
                if adj[i][j][0] > -1:
                    adj[i][j][1] = newadj[i][j][1] + adj[i][j][0]
        out = ford_fulkerson(adj, 0, mysize-1)
 
    # Write output
        write_output(output_file, out, num_customers)
 
 
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import sys
 
    # Load inputs
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    solve_survey_design(input_file, output_file)
