from neuroworm.brain.connectome import (
    neurons,
    connections
)

print("Testing Data-Driven Connectome\n")


def propagate(source):

    fired = []

    for frm, to, weight in connections:

        if frm == source:

            if neurons[to].stimulate(weight):

                fired.append(to)

    return fired


for i in range(20):

    print(f"\nStimulus {i+1}")

    if neurons["AWA"].stimulate():

        print("AWA FIRED")

        layer1 = propagate("AWA")

        for neuron in layer1:

            print(f"{neuron} FIRED")

            layer2 = propagate(neuron)

            for neuron2 in layer2:

                print(f"{neuron2} FIRED")

                print("MOTOR OUTPUT")