from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT
from qiskit.circuit.library import ZGate
from qiskit.circuit.library import IntegerComparator
from clc_oracle import apply_clc
from controlled_u import apply_grover_diffusion_operator
from qiskit.primitives import Estimator
from qiskit.primitives import StatevectorSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit_aer import Aer
import numpy as np
m = 2
t = 3
N = 4
i = 0
Iopt = np.pi * np.sqrt(2**(m*N)) / 4
constants = {"m":m, "N":N, "t":t, "i":i, "Iopt":Iopt}

qr_C = QuantumRegister(m*N, 'C')
qr_t = QuantumRegister(t, 't')
qr_RCLC = QuantumRegister(t, 'RCLC')
qr_RHCD = QuantumRegister(1, 'RHCD')
qr_R = QuantumRegister(1, 'R')
cr_C = ClassicalRegister(m*N, 'Res')
registers = {"C":qr_C, "t":qr_t, "R":qr_R, "RCLC":qr_RCLC, "RHCD":qr_RHCD}

TSPcircuit = QuantumCircuit(qr_C, qr_t, qr_RCLC, qr_RHCD, qr_R, cr_C)

TSPcircuit.x(qr_R)
TSPcircuit.h(qr_R)

for qubit in range(m*N):
    TSPcircuit.h(qr_C[qubit])

for qubit in range(t):
    TSPcircuit.h(qr_t[qubit])

TSPcircuit = apply_clc(TSPcircuit, registers, constants, True)

TSPcircuit = apply_grover_diffusion_operator(TSPcircuit, registers, constants)

TSPcircuit = apply_clc(TSPcircuit, registers, constants, True)

TSPcircuit.measure(qr_C, cr_C)

# sampler = StatevectorSampler()
# job = sampler.run([TSPcircuit]) 
# pub_result = job.result()[0]
print(TSPcircuit)
# counts = pub_result.meas.get_counts()
# print(f"The counts are: {counts}")
# print(pub_result)
# Display the circuit

# from qiskit import QuantumCircuit
 
# qc = QuantumCircuit(2)
# qc.h(0)
# qc.cx(0,1)
# qc.measure_all()
# qc.draw("mpl", style="iqp")
# from qiskit.quantum_info import SparsePauliOp
# observable = SparsePauliOp(["II", "XX", "YY", "ZZ"], coeffs=[1, 1, -1, 1])

 
# pm = generate_preset_pass_manager(optimization_level=1)
# isa_circuit = pm.run(qc)
# isa_observable = observable.apply_layout(isa_circuit.layout)

# # execute 1 circuit with Sampler V2
# job = sampler.run([isa_circuit]) 
# pub_result = job.result()[0]
# print(f" > Result class: {type(pub_result)}")


sim = Aer.get_backend('qasm_simulator')
new_circuit = transpile(TSPcircuit, backend=sim)
job = sim.run(new_circuit) # Need to determine lower bound on suitable number of shots to take
result = job.result()
paths = result.get_counts()
print(paths)

#   # Transpile circuit
# pm = generate_preset_pass_manager(optimization_level=1)
# isa_circuit = pm.run(TSPcircuit)
# # Run using V2 sampler
# result = sampler.run([TSPcircuit]).result()
# # Access result data for PUB 0
# data_pub = result[0].data
# # Access bitstring for the classical register "meas"
# bitstrings = data_pub.meas.get_bitstrings()
# print(f"The number of bitstrings is: {len(bitstrings)}")
# # Get counts for the classical register "meas"
# counts = data_pub.meas.get_counts()
# print(f"The counts are: {counts}")
