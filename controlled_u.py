from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit.circuit.library import ZGate, Diagonal
# from qiskit.circuit.library import cz
from qiskit.circuit.library import IntegerComparator
# from qiskit_ibm_runtime.fake_provider import FakeCairoV2
import qiskit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import GroverOperator
import networkx as nx
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
import numpy as np

def get_complete_adjacencies(cities):
    adjacencies = []
    for i in range(cities):
        adjacencies.append([x for x in range(cities) if x != i])
    return adjacencies

def generate_tsp_instance(num_cities):
    G = nx.erdos_renyi_graph(num_cities, 0.8)
    for e in G.edges():
        G.add_edge(e[0], e[1], weight=np.round(np.abs(np.random.normal(0,2)),3))
    return G


def get_adjacency_matrix(cities):

    # return np.matrix([[ 0,  1,  7,  6],
    #                   [ 1,  0,  5,  4],
    #                   [ 7,  5,  0,  4],
    #                   [ 6,  4,  4,  0]])

    G = generate_tsp_instance(cities)
    return nx.adjacency_matrix(G)
    
def get_theta(j, k):
    a = get_adjacency_matrix(4)
    adjacencies = get_complete_adjacencies(4)
    # print(a.item(j, adjacencies[j][k]))
    return a.item(j, adjacencies[j][k])

def cost(constants):
    count = 0
    sum_result = 0
    while count < constants["N"]:
        sum_result += get_theta(count, 1)
    return sum_result

def get_U_j_list(cities):
    U_j_list = []
    for j in range(cities):
        # Size of the unitary, 2^m
        m = 2
        size_Uj = 2 ** m

        # Calculate the theta values according to the equation
        theta_j = [0] * size_Uj
        for k in range(cities - 1):
            theta_j[k] = get_theta(j, k)

        # Exponentiate the theta values to form the diagonal of the unitary matrix
        diagonal_elements = np.exp(1j * np.array(theta_j))

        print(diagonal_elements)
        # Create the diagonal gate
        U_j = Diagonal(diagonal_elements)

        U_j_list.append(U_j)

    return U_j_list

def get_U_j_conj_list(cities):
    U_j_conj_list = []
    for j in range(cities):
        # Size of the unitary, 2^m
        m = 2
        size_Uj = 2 ** m

        # Calculate the theta values according to the equation
        theta_j = [0] * size_Uj
        for k in range(cities - 1):
            theta_j[k] = get_theta(j, k)

        # Exponentiate the theta values to form the diagonal of the unitary matrix
        diagonal_elements = np.exp(-1j * np.array(theta_j))

        # Create the diagonal gate
        U_j = Diagonal(diagonal_elements)

        U_j_conj_list.append(U_j)

    return U_j_conj_list
    # # Create a new quantum circuit or use an existing one
    # qc = QuantumCircuit(m)  # 'm' qubits in the register

    #     # Apply the diagonal gate to the circuit
    # qc.append(U_j, [i for i in range(m)])

    # # Display the circuit
    # print(qc)

def apply_grover_diffusion_operator(circuit, registers, constants):
    """
    Apply diffusion operator to first m * N cities
    """
    grover_oracle = QuantumCircuit(constants["m"] * constants["N"])

    grover_circuit = GroverOperator(grover_oracle, insert_barriers=True)

    circuit.compose(grover_circuit, inplace=True)

    return circuit

# backend = FakeCairoV2()
# estimator = Estimator(backend)
# print(result)
