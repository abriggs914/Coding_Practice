import numpy as np

"""
	Simple neural network to determine the output of a 3 digit
	input number consisting of 1s and 0s. Output is one of
	0 or 1. The network is trained to determine that if the 
	first digit of new input is 1, then the output is 1, otherwise
	output is 0.

	Sept. 27 / 2019
"""

def sigmoid(x) :
	return 1 / (1 + np.exp(-x))
	
def sigmoid_derivative(x) :
	return x * (1 - x)

training_inputs = np.array([[0,0,1],
							[1,1,1],
							[1,0,1],
							[0,1,1]])
							
training_outputs = np.array([[0,1,1,0]]).T

np.random.seed(1)

synaptic_weights = 2 * np.random.random((3,1)) - 1

print("Random starting synaptic weights: ")
print(synaptic_weights)

for iteration in range(20000) :
	
	input_layer = training_inputs
	
	outputs = sigmoid(np.dot(input_layer, synaptic_weights))
	
	error = training_outputs - outputs
	
	adjustments = error * sigmoid_derivative(outputs)
	
	synaptic_weights += np.dot(input_layer.T, adjustments)

print("Synaptic weights after training: ")
print(synaptic_weights)
	
print("Outputs after testing: ")
print(outputs)