from neuron import Neuron
from synapse import Synapse

sensory = Neuron(threshold=3)

interneuron = Neuron(threshold=4)

strong_synapse = Synapse(weight=2)

print("Testing Synapse\n")

for i in range(10):

    print(f"Stimulus {i+1}")

    if sensory.stimulate():

        print("Sensory neuron fired")

        signal = strong_synapse.transmit()

        print(
            f"Synapse transmitted {signal}"
        )

        if interneuron.stimulate(signal):

            print("INTERNEURON FIRED")

    print()