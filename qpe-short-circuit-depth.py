from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import UnitaryGate
import numpy as np
import scipy
from scipy.optimize import minimize
from controlled_u import get_U_j_short_depth

# Create a Quantum Register with 2 qubits and a Classical Register with 1 bit
qreg = QuantumRegister(2)
creg = ClassicalRegister(1)
circuit = QuantumCircuit(qreg, creg)

# Apply Hadamard gate on qubit 0
circuit.h(qreg[0])

# Apply controlled unitary operation for the Hamiltonian time evolution
# Assuming the Hamiltonian is represented by a matrix 'H_matrix' and time 't'
H_matrix = np.array([[1, 0], [0, -1]])  # Example: Pauli-Z matrix
time = np.pi  # Example: pi
unitary_matrix = scipy.linalg.expm(-1j * time * H_matrix)
circuit.append(UnitaryGate(unitary_matrix).control(), [qreg[0], qreg[1]])

# Apply W gate (Identity or S-dagger) on qubit 0
# For S-dagger
# circuit.sdg(qreg[0])
# If W were to be the Identity, you would use:
# circuit.i(qreg[0])

# Apply Hadamard gate on qubit 0
circuit.h(qreg[0])

# Measurement on qubit 0
circuit.measure(qreg[0], creg[0])

# Draw the circuit
print(circuit)

# Define the loss function L(r, theta)
def loss_function(params, Z):
    r, theta = params
    N = len(Z)
    loss = (1/N) * np.sum(np.abs(Z - r * np.exp(-1j * theta * np.arange(N)))**2)
    return loss

# Example data (Z_n values), replace with actual data
Z = np.random.random(10) + 1j*np.random.random(10)  # Dummy complex data

# Initial guess for r and theta
initial_guess = [1.0, 0.0]

# Perform the minimization
result = minimize(loss_function, initial_guess, args=(Z,), bounds=[(0, None), (None, None)])

# Optimal values
r_star, theta_star = result.x

print(f"The optimal values are r* = {r_star} and theta* = {theta_star}")

def apply_qpe(circuit, registers, constants):
    circuit.h(registers["t"][0])
    U_j_short_depth = get_U_j_short_depth(4, 100)
    for t in range(len(U_j_short_depth)):
        for k in range(constants["N"]):
            circuit.compose(U_j_short_depth[t][k].control(1), qubits = [constants["m"] * constants["N"] + 1, 2*k, 2*k+1], inplace = True)
    circuit.h(registers["t"][0])
