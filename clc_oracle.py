from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit.circuit.library import ZGate
# from qiskit.circuit.library import cz
from qiskit.circuit.library import IntegerComparator
import numpy as np
from controlled_u import get_U_j_list

def apply_clc(circuit: QuantumCircuit, registers, constants) -> QuantumCircuit:
    # Apply H gates to each qubit in the t register
    circuit.h(registers["t"])

    U_j_list = get_U_j_list(constants["N"])
    
    count = 0
    while count < constants["t"]:
        for j in range(int(2**count)):
            for i in range(constants["m"] * constants["N"]):
                circuit.compose(U_j_list[0], qubits = [0,1], inplace = True)
                # circuit.cz(registers["t"][count], registers["C"][i])  # Controlled on target qubits
        count += 1


    # Apply the inverse Quantum Fourier Transform on t qubits
    circuit.append(QFT(num_qubits=constants["t"], inverse=True), registers["t"])

    # <Cth
    comparator = IntegerComparator(num_state_qubits=constants["t"], value=1, geq=False)
    circuit.compose(comparator, qubits = [x for x in range(int(constants["m"] * constants["N"]), int(constants["m"] * constants["N"] + 2 * constants["t"]))], inplace=True)

    # Apply the Quantum Fourier Transform on t qubits
    circuit.append(QFT(num_qubits=constants["t"]), registers["t"])

    count = 0
    while count < constants["t"]:
        for j in range(int(2**count)):
            for i in range(constants["m"] * constants["N"]):
                circuit.compose(U_j_list[0], qubits = [0,1], inplace = True)
                #circuit.cz(registers["t"][count], registers["C"][i])  # Controlled on target qubits
        count += 1

    # Apply H gates to each qubit in the t register again
    circuit.h(registers["t"])

    # Draw the circuit
    return circuit
