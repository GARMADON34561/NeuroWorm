from neuroworm.brain.connectome import (
    neurons,
    connections
)


class ConnectomeEngine:

    def stimulate(self, neuron_name):

        queue = [neuron_name]

        fired = []

        while queue:

            current = queue.pop(0)

            for conn in connections:

                if conn["from"] == current:

                    target = conn["to"]

                    weight = conn["weight"]

                    if neurons[target].stimulate(weight):

                        fired.append(target)

                        queue.append(target)

        return fired