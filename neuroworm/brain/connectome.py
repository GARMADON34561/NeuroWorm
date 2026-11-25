from brain.neuron import Neuron


neurons = {

    # sensory neurons

    "PLML": Neuron(threshold=1),
    "PLMR": Neuron(threshold=1),

    "ALML": Neuron(threshold=1),
    "ALMR": Neuron(threshold=1),

    "AVM": Neuron(threshold=1),

    # intermediary neurons

    "PVCL": Neuron(threshold=1),
    "PVCR": Neuron(threshold=1),

    # reverse command neurons

    "AVAL": Neuron(threshold=1),
    "AVAR": Neuron(threshold=1),

    # forward command neurons

    "AVBL": Neuron(threshold=1),
    "AVBR": Neuron(threshold=1),

    # keep escape neuron for now

    "RIM": Neuron(threshold=1)
}


connections = [

    {
        "from": "ALML",
        "to": "PVCL",
        "weight": 2
    },

    {
        "from": "AVM",
        "to": "PVCL",
        "weight": 1
    },

    {
        "from": "PVCL",
        "to": "AVAL",
        "weight": 2
    },

    {
        "from": "PVCL",
        "to": "RIM",
        "weight": 2
    },

    {
        "from": "PLML",
        "to": "AVBL",
        "weight": 1
    }
]


def explore():

    if neurons["AVBL"].stimulate():

        print("AVBL FIRED")

        return "EXPLORE"

    return "WAIT"


def investigate():

    if neurons["AVM"].stimulate():

        print("AVM FIRED")

        return "INVESTIGATE"

    return "WAIT"


def avoid():

    if neurons["ALML"].stimulate():

        print("ALML FIRED")

        if neurons["PVCL"].stimulate(2):

            print("PVCL FIRED")

            if neurons["AVAL"].stimulate(2):

                print("AVAL FIRED")

                return "AVOID"

    return "WAIT"


def escape():

    if neurons["PVCL"].stimulate(2):

        if neurons["RIM"].stimulate(2):

            print("RIM FIRED")

            return "ESCAPE"

    return "WAIT"