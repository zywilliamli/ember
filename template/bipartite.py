import pulp
import networkx as nx

M = 16
L = 4

# Clique graph as input
# G = nx.generators.complete_graph(M * L)
# G = nx.generators.gnp_random_graph(80, 0.3, seed=10)
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)])

K = [1, 2]
I = range(len(G))

model = pulp.LpProblem("MIP_Model", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", (I, K), cat="Binary")
y_prime = pulp.LpVariable.dict("y_prime", I, cat="Binary")

# Objective
model += pulp.lpSum(y_prime)

# Constraints
for i in I:
    model += y_prime[i] <= y[i][1] + y[i][2]

for k in K:
    model += pulp.lpSum([y[i][k] for i in I]) <= M * L

for i, j in G.edges:
    model += y[i][1] + y[j][1] - y[i][2] - y[j][2] <= 1
    model += y[i][2] + y[j][2] - y[i][1] - y[j][1] <= 1

gurobi = pulp.apis.GUROBI()

if gurobi.available():
    model.solve(solver=gurobi)
else:
    model.solve()

print(model.objective)

# Check embedding found
if model.objective.value() == len(G):
    print("Found valid embedding")
else:
    print("Valid embedding not found")