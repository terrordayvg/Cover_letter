#Creator: Vladlen G. 10/19/2023
#Code:  "Cover letter for quantum simulations 101" ==========================================================================================
from qiskit import IBMQ, Aer, transpile, assemble            # Importing Qiskit packages
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.result import marginal_counts
import binascii
import numpy as np
def Non_destr_meas(circ,j,q,Vec):
	aux=np.arange(j*int(q/2),j*int(q/2)+int(q/2))
	Aux=aux.tolist()
	circ.cx(Vec[:int(q/2)],Vec[int(q/2):])
	circ.measure(Vec[int(q/2):],Aux)
	circ.reset(Vec[int(q/2):])
	return circ

def Command_gen():
	#Generation of commands described in "Encoding"
	Dic=[['circ.x(3)'],['circ.x(0)'],['circ.swap(3,4)','circ.swap(0,1)'],['circ.swap(4,0)','circ.swap(1,2)'],[''],['circ.x(3)'],['circ.x(3)']] 
	return Dic

def Circ_generator(Com_vec):
	backend = Aer.get_backend('aer_simulator')
	Nstep=7 											# Number of operations
	q=10												# 5 ancilla 5 target for non destructive measurements
	Vec=np.arange(q)
	circ=QuantumCircuit(10,(q/2) * Nstep) 								# Circuit of size 5 of the total string size 8 (for ASCII presentation) 
	for j in range(Nstep):										#Encoding commands:
		for k in range(len(Com_vec[j])):							#Op 0) init: x (q3) 
			exec(Com_vec[j][k])								#Op 1) x (q0)  
		if(j==4): #Null										#Op 2) Shift left
			aux=np.arange(j*int(q/2),j*int(q/2)+int(q/2))					#Op 3) Shift left
			Aux=aux.tolist()								#Op 4) Skip 
			circ.measure(Vec[int(q/2):],Aux)						#Op 5) x (q3) 
		else:											#Op 6) x (q3) 
			Non_destr_meas(circ,j,q,Vec)					

	t_qpe2 = transpile(circ, backend,seed_transpiler=42)
	results = backend.run(t_qpe2,shots=1,seed_simulator=42).result()
	Fstring=''  											#Final string
	for i in range(Nstep):
		aux=np.arange(i*int(q/2),i*int(q/2)+int(q/2))
		Aux=aux.tolist()
		partial = list(marginal_counts(results, indices=Aux).get_counts())[0]
		if(i==4): 										#Null
			Cstring='001'+ partial
		else:
			Cstring='011'+ partial
		Fstring=Fstring+Cstring 								#Prefix of ASCII to fill 8 bits : prefix= 3 bits + partial= 5 bits defining alphabet	
	return Fstring

def Ascii_Decoder(Bin_str):
	n = int(Bin_str, 2)
	Text=str(binascii.unhexlify('%x' % n))
	print(Text[1:])

if __name__ == '__main__':
	Com_vec=Command_gen()                                   #Generation of commands in a vector of strings
	Bin_str=Circ_generator(Com_vec)                         #Generation of multiple quantum circuits based on the commands
	Ascii_Decoder(Bin_str)                                  #Decoder of the classical result into Ascii notation
