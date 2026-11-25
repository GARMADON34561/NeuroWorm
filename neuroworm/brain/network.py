from neuroworm.brain.neuron import Neuron
from neuroworm.brain.synapse import Synapse

class SimpleNetwork:

    def __init__(self):

        self.sensory = Neuron(threshold=3)

        self.interneuron = Neuron(threshold=4)

        self.synapse = Synapse(weight=2)

    def stimulate(self):

        if self.sensory.stimulate():

            signal = self.synapse.transmit()

            if self.interneuron.stimulate(signal):

                return True

        return False