from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit.circuit.library import ZGate
# from qiskit.circuit.library import cz
from qiskit.circuit.library import IntegerComparator
import numpy as np
from controlled_u import get_U_j_list, get_U_j_conj_list

def apply_clc(circuit: QuantumCircuit, registers, constants, tsp_instance) -> QuantumCircuit:
    # Apply H gates to each qubit in the t register
    circuit.h(registers["t"])

    U_j_list = get_U_j_list(constants["N"], tsp_instance)
    U_j_conj_list = get_U_j_conj_list(constants["N"], tsp_instance)

    count = 0
    while count < constants["t"]:
        for j in range(int(2**count)):
            circuit.compose(U_j_list[0].control(1), qubits = [8+count, 0, 1], inplace = True)
            circuit.compose(U_j_list[1].control(1), qubits = [8+count, 2, 3], inplace = True)
            circuit.compose(U_j_list[2].control(1), qubits = [8+count, 4, 5], inplace = True)
            circuit.compose(U_j_list[3].control(1), qubits = [8+count, 6, 7], inplace = True)
        count += 1


    # Apply the inverse Quantum Fourier Transform on t qubits
    circuit.append(QFT(num_qubits=constants["t"], inverse=True), registers["t"])

    # <Cth
    int_comp_val = (2 ** (constants["t"] + 1))/(constants["p"] * (constants["N"] - 1))
    comparator = IntegerComparator(num_state_qubits=constants["t"], value=int_comp_val, geq=False)
    circuit.compose(comparator, qubits = [x for x in range(int(constants["m"] * constants["N"]), int(constants["m"] * constants["N"] + 2 * constants["t"]))], inplace=True)

    # Apply the Quantum Fourier Transform on t qubits
    circuit.append(QFT(num_qubits=constants["t"]), registers["t"])

    count = 0
    while count < constants["t"]:
        for j in range(int(2**count)):
            circuit.compose(U_j_conj_list[0].control(1), qubits = [8+count, 0, 1], inplace = True)
            circuit.compose(U_j_conj_list[1].control(1), qubits = [8+count, 2, 3], inplace = True)
            circuit.compose(U_j_conj_list[2].control(1), qubits = [8+count, 4, 5], inplace = True)
            circuit.compose(U_j_conj_list[3].control(1), qubits = [8+count, 6, 7], inplace = True)
        count += 1

    # Apply H gates to each qubit in the t register again
    circuit.h(registers["t"])

    # Draw the circuit
    return circuit
